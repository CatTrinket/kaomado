#!/usr/bin/env python3
"""Extract the portrait sprites from Pokémon Mystery Dungeon: Explorers of Sky.
PMD: Blue Rescue Team is also partially supported.

Requires pypng 0.0.13 or later.

This program does not actually rip sprites directly from a ROM.  You'll have to
provide the portrait file yourself.  In a European PMD: Sky ROM, the file is
located at /FONT/kaomado.kao; in an American PMD: Blue ROM, the file this
script requires is /monster.sbin.  I assume these files are the same for other
regions.

/monster.sbin contains at least the portraits for Pokémon with multiple
portraits.  They only take up part of the file, so the others might be in the
same file, but if so, they don't use the same compression scheme.

"kaomado" means "face window", as far as I can tell.

n.b. "left" and "right" are consistently used from the perspective of the
Pokémon in the portrait.  This also means that the "right" sprite is the one
that appears on the right side of the screen in-game.
"""

import errno
import os
import png
from struct import unpack
from sys import argv

import tables

SKY = 'sky'
BLUE = 'blue'
version = None

def build_filename(pokemon, expression, is_right, output_dir):
    """Determine an output filename for a sprite given the Pokémon it
    depicts, an identifier for its facial expression, the direction it's
    facing, and the base output directory.
    """

    filename = [output_dir]

    if pokemon.is_female:
        filename.append('female')

    if is_right:
        filename.append('right')

    if expression != tables.expressions.STANDARD:
        filename.append('{0}-{1}.png'.format(pokemon.identifier, expression))
    else:
        filename.append('{0}.png'.format(pokemon.identifier))

    return os.path.join(*filename)

def decompress(kaomado):
    """Decompress a sprite at the current offset."""

    if kaomado.read(5) != b'AT4PX':
        raise ValueError('wrong magic bytes for compressed sprite')

    kaomado.seek(2, os.SEEK_CUR)  # Compressed length; we don't use this

    # The control codes used for 0-flags vary from sprite to sprite
    controls = list(kaomado.read(9))

    length, = unpack('<H', kaomado.read(2))

    data = bytearray()
    while len(data) < length:
        flags, = kaomado.read(1)
        for flag in range(8):
            if flags & (0x80 >> flag):
                # Flag 1: append one byte as-is
                data.extend(kaomado.read(1))
            else:
                # Flag 0: do one of two fancy things based on the next byte's
                # high and low nybbles
                control, = kaomado.read(1)
                high, low = control >> 4, control & 0xf

                if high in controls:
                    # Append a pattern of four pixels.  The high bits determine
                    # the pattern, and the low bits determine the base pixel.
                    control = controls.index(high)
                    pixels = [low] * 4

                    if control == 0:
                        pass
                    elif 1 <= control <= 4:
                        # Lower a particular pixel
                        if control == 1:
                            pixels = [low + 1] * 4
                        pixels[control - 1] -= 1
                    else:
                        # 5 <= control <= 8; raise a particular pixel
                        if control == 5:
                            pixels = [low - 1] * 4
                        pixels[control - 5] += 1

                    # Pack the pixels into bytes and append them
                    data.extend((pixels[0] << 4 | pixels[1],
                                 pixels[2] << 4 | pixels[3]))
                else:
                   # Append a sequence of bytes previously used in the sprite.
                   # This can overlap with the beginning of the appended bytes!
                   # The high bits determine the length of the sequence, and
                   # the low bits help determine the where the sequence starts.
                   offset = -0x1000
                   offset += (low << 8) | kaomado.read(1)[0]

                   for b in range(high + 3):
                       data.append(data[offset])

            if len(data) == length:
                break

    return data

def makedirs_if_need_be(leaf_directory):
    """Create the given directory and its parents as needed, but don't break if
    it turns out no directories actually need creating.
    """

    try:
        os.makedirs(leaf_directory)
    except OSError as e:
        if e.errno == errno.EEXIST:
            # Leaf directory already exists
            pass
        else:
            raise e

def parse_palette(kaomado):
    """Parse an RGB palette at the current offset: sixteen colors, five bits
    per channel.

    Each channel gets its own byte, for some reason, as opposed to the usual
    NTFP color format which actually fits all three into fifteen bits.

    In PMD: Blue, each palette entry is padded to four bytes with 0x80 and I
    don't know why.
    """

    palette = []
    for color in range(0x10):
        palette.append(tuple(
            channel >> 3 for channel in kaomado.read(3)
        ))

        if version == BLUE:
            kaomado.seek(1, os.SEEK_CUR)

    return palette

def pixel_iterator(sprite):
    """Iterate over raw sprite data pixel by pixel."""

    for pixel_pair in sprite:
        yield pixel_pair & 0xf
        yield pixel_pair >> 4

def rip_blue(kaomado, output_dir):
    """Rip portrait sprites from Blue Rescue Team's monster.sbin.  Or at least
    the important ones.
    """

    for pokemon_header in range(0x1a70, 0x1ef0, 0x10):
        # Deliberately skipping the last one because it's a dupe Rayquaza
        kaomado.seek(pokemon_header)

        # Read the label, figure out which Pokémon it means
        label = kaomado.read(8).rstrip(b'\x00').decode('ASCII')
        assert label.startswith('kao')
        pokemon = int(label[3:])
        pokemon = tables.pokemon.blue[pokemon]

        # We only get one offset where all that Pokémon's portraits are packed
        pointer, length = unpack('<2L', kaomado.read(8))
        kaomado.seek(pointer)

        # Find the portrait block, figure out where it ends
        assert kaomado.read(4) == b'SIR0'
        sprites_length, = unpack('<L', kaomado.read(4))
        sprites_end = pointer + sprites_length
        kaomado.seek(8, os.SEEK_CUR)  # I don't know what this is

        sprite_num = 0
        while kaomado.tell() < sprites_end:
            expression, is_right = tables.expressions.blue(pokemon, sprite_num)

            if expression is None:
                # Only Skarmory has a placeholder; second and last in its block
                break

            palette = parse_palette(kaomado)
            sprite = decompress(kaomado)

            # The start/end of each sprite is word-aligned
            word_offset = kaomado.tell() % 4
            if word_offset:
                kaomado.seek(4 - word_offset, os.SEEK_CUR)

            # Save image
            sprite = unscramble(sprite, palette)
            sprite = png.from_array(sprite, mode='RGB;5')

            filename = build_filename(pokemon, expression, is_right, output_dir)
            sprite.save(filename)

            sprite_num += 1


def rip_sky(kaomado, output_dir):
    """Rip portrait sprites from Explorers of Sky's kaomado.kao."""

    for internal_id, pokemon in tables.pokemon.sky.items():
        kaomado.seek(0xa0 * internal_id)

        # Each Pokémon has a sprite pointer for each facial expression and
        # direction, even if they're not all used
        pointers = unpack('<40L', kaomado.read(0xa0))

        for sprite_num, pointer in enumerate(pointers):
            if not 0x2d1e0 <= pointer <= 0x1968c0:
                # Nonexistent sprites have consistent junk pointers, thankfully
                continue

            expression, is_right = tables.expressions.sky(pokemon, sprite_num)

            if expression is None:
                # Some sprites exist, but are junk anyway
                continue

            kaomado.seek(pointer)

            # Get the palette
            palette = parse_palette(kaomado)

            # Extract the actual sprite
            sprite = decompress(kaomado)
            sprite = unscramble(sprite, palette)

            # Save it as a PNG
            sprite = png.from_array(sprite, mode='RGB;5')
            filename = build_filename(pokemon, expression, is_right, output_dir)
            sprite.save(filename)

def unscramble(sprite, palette):
    """Unscramble the raw sprite data into something pypng can swallow."""

    pixels = pixel_iterator(sprite)

    # Untile the sprite and apply the palette.  Each row is a flat list of RGB
    # channels because, at the time of writing, image[y][x][channel] doesn't
    # actually work with png.from_array().
    image = [[None for x_channel in range(120)] for y in range(40)]

    for tile in range(25):
        tile_x = tile % 5
        tile_y = tile // 5

        for pixel in range(64):
            pixel_x = pixel % 8
            pixel_y = pixel // 8

            x = (tile_x * 8 + pixel_x) * 3
            y = tile_y * 8 + pixel_y

            image[y][x:x + 3] = palette[next(pixels)]

    return image


if len(argv) != 3:
    print("Usage: kaomado.py portrait-file output-dir")
    exit(1)

kaomado = open(argv[1], 'rb')
output_dir = argv[2]

magic = kaomado.read(5)

if magic == b'\x00\x00\x00\x00\x00':
    version = SKY
    rip = rip_sky
elif magic == b'ax001':
    version = BLUE
    rip = rip_blue
else:
    print("Unrecognized portrait file")
    exit(1)

# Make the leaves of the required directory tree (parents are taken care of)
makedirs_if_need_be(os.path.join(output_dir, 'right'))
if version == SKY:
    makedirs_if_need_be(os.path.join(output_dir, 'female', 'right'))

rip(kaomado, output_dir)
