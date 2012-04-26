#!/usr/bin/env python3
"""Extract the portrait sprites from Pokémon Mystery Dungeon: Explorers of Sky.

This program does not actually rip sprites directly from a ROM.  You'll have to
provide the portrait file yourself.  In a PMD: Sky ROM (or at least a European
multilingual one) the file can be found at /FONT/kaomado.kao.

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

from tables import expressions, pokemon_ids, Pokemon

def build_filename(pokemon, sprite_num, output_dir):
    """Determine an output filename for a sprite given the Pokémon it
    depicts, the sprite's index in that Pokémon's list of sprite pointers,
    and the base output directory.
    """

    # Start with the main output directory
    filename = [output_dir]

    # Stick various junk sprites in other/ for potential debug purposes
    if pokemon.species == 'other':
        filename.append('other')

    if pokemon.female:
        filename.append('female')

    # Sprite pointers come in pairs of two: facing left and (sometimes) right
    # for a given facial expression.
    expression = expressions[sprite_num // 2]
    if expression != 'standard':
        filename.append(expression)

    if sprite_num % 2 != 0:
        filename.append('right')

    # Figure out the base filename
    if pokemon.form is not None:
        filename.append('{0}-{1}.png'.format(pokemon.national_id, pokemon.form))
    else:
        filename.append('{0}.png'.format(pokemon.national_id))

    return os.path.join(*filename)

def decompress(kaomado):
    """Decompress a sprite at the current offset."""

    if kaomado.read(5) != b'AT4PX':
        raise ValueError('wrong magic bytes')

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

def makedirs_if_need_be(filename):
    """Create directories as needed to house the given filename, but don't
    break if it turns out no directories actually need creating.
    """

    try:
        os.makedirs(os.path.dirname(filename))
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
    """

    palette = []
    for color in range(0x10):
        palette.append(tuple(
            channel >> 3 for channel in kaomado.read(3)
        ))

    return palette

def pixel_iterator(sprite):
    """Iterate over raw sprite data pixel by pixel."""

    for pixel_pair in sprite:
        yield pixel_pair & 0xf
        yield pixel_pair >> 4

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
    print("Usage: kaomado.py /path/to/kaomado.kao output-dir")
    exit(1)

kaomado = open(argv[1], 'br')
output_dir = argv[2]

for pokemon in range(1, 1155):
    kaomado.seek(0xa0 * pokemon)

    try:
        pokemon = pokemon_ids[pokemon]
    except KeyError:
        pokemon = Pokemon(pokemon, 'other', None, False)

    # Each Pokémon has a sprite pointer for each facial expression and
    # direction, even if they're not all used
    pointers = unpack('<40L', kaomado.read(0xa0))

    for sprite_num, pointer in enumerate(pointers):
        if not 0x2d1e0 <= pointer <= 0x1968c0:
            # Nonexistent sprites have consistent junk pointers, thankfully
            continue

        kaomado.seek(pointer)

        # Get the palette
        palette = parse_palette(kaomado)

        # Extract the actual sprite
        sprite = decompress(kaomado)
        sprite = unscramble(sprite, palette)

        # Save it as a PNG
        sprite = png.from_array(sprite, mode='RGB;5')
        filename = build_filename(pokemon, sprite_num, output_dir)
        makedirs_if_need_be(filename)
        sprite.save(filename)
