import os
from struct import unpack

from tables import expressions, pokemon_ids, Pokemon

emotions = ['', 'grin', 'pained', 'angry', 'worried', 'sad', 'crying',
            'shouting', 'teary-eyed', 'determined', 'joyous', 'inspired',
            'surprised', 'dizzy', 'sweatdrop1', 'sweatdrop2']

kaomado = open('/var/tmp/kaomado.kao', 'br')

for pokemon in range(1155):
    kaomado.seek(0xa0 * pokemon)

    try:
        pokemon = pokemon_ids[pokemon]
    except KeyError:
        pokemon = Pokemon(pokemon, 'other', None, False)

    pointers = unpack('<40L', kaomado.read(0xa0))

    for n, pointer in enumerate(pointers):
        if not 0x2d1e0 <= pointer <= 0x1968c0:
            # Junk
            continue

        kaomado.seek(pointer)

        palette = []
        for colour in range(0x10):
            palette.append(tuple(channel >> 3 for channel in kaomado.read(3)))

        kaomado.seek(0x7, 1)  # AT4PX + compressed length
        controls = list(kaomado.read(9))
        kaomado.seek(2, 1)  # Little-endian uncompressed length (always 0x320)

        sprite = bytearray()

        while len(sprite) < 0x320:
            flags, = kaomado.read(1)
            for flag in range(8):
                if len(sprite) == 0x320:
                    break
                if flags & 0x80 >> flag:
                    sprite += kaomado.read(1)
                else:
                    control, = kaomado.read(1)
                    high, low = control >> 4, control & 0xf

                    if high in controls:
                        pixels = [low] * 4  # 2 1 4 3
                        control = controls.index(high)

                        if 1 <= control <= 4:
                            if control == 1:
                                pixels = [low + 1] * 4

                            pixels[control - 1] -= 1
                        elif 5 <= control <= 8:
                            if control == 5:
                                pixels = [low - 1] * 4
                            pixels[control - 5] += 1

                        sprite.extend((pixels[0] << 4 | pixels[1],
                                       pixels[2] << 4 | pixels[3]))
                    else:
                       offset, = kaomado.read(1)
                       offset -= 0x100 * (0x10 - low)

                       for b in range(high + 3):
                           sprite.append(sprite[offset])

        filename = ['/var/tmp/kaomado']

        if pokemon.species == 'other':
            filename.append('other')

        if pokemon.female:
            filename.append('female')

        if n // 2 != 0:
            filename.append(expressions[n // 2])

        if n % 2 != 0:
            filename.append('right')  # Their right, not ours

        if pokemon.form is not None:
            filename.append('{0}-{1}.ppm'.format(
                pokemon.national_id, pokemon.form))
        else:
            filename.append('{0}.ppm'.format(pokemon.national_id))

        filename = os.path.join(*filename)
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as e:
            if e.errno == 17:
                # Leaf already exists
                pass
            else:
                raise e

        output = open(filename, 'w')

        output.write('P3\n40 40\n31\n')

        for y in range(40):
            for x in range(0, 40, 2):
                # Tile rows before this + row tiles before this + rows + in-row
                pair = sprite[160 * (y // 8) + 32 * (x // 8) +
                              4 * (y % 8) + x % 8 // 2]
                output.write(''.join('{0} {1} {2} '.format(*palette[pixel]) for
                    pixel in (pair & 0xf, pair >> 4)))

            output.write('\n')

        output.close()
