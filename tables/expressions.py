### Expression constants to minimize typos and keep everything organized
# Expressions with "official" names from the Sky debug menu
ANGRY = 'angry'
CRYING = 'crying'
DETERMINED = 'determined'
DIZZY = 'dizzy'
GRIN = 'grin'
INSPIRED = 'inspired'
JOYOUS = 'joyous'
PAINED = 'pained'
SAD = 'sad'
SHOUTING = 'shouting'
STANDARD = 'standard'
SURPRISED = 'surprised'
TEARY_EYED = 'teary-eyed'
WORRIED = 'worried'

# Other consistent Sky categories
SIGH = 'sigh'
STUNNED = 'stunned'

# Other consistent Blue categories
HAPPY = 'happy'

# Expressions that appear a few times at most
OTHER_ASLEEP = 'asleep'
OTHER_BLUSHING = 'blushing'
OTHER_BOUND = 'bound'
OTHER_CONTEMPT = 'contempt'
OTHER_DROOLING = 'drooling'
OTHER_EXTREMELY_HAPPY = 'extremely-happy'
OTHER_FAINTED = 'fainted'
OTHER_FURTHER_CONTEMPT = 'further-contempt'
OTHER_HURT = 'hurt'
OTHER_PANIC = 'panic'
OTHER_PROUD = 'proud'
OTHER_SICK = 'sick'
OTHER_TEARY_EYED_2 = 'teary-eyed-2'
OTHER_TEARY_EYED_3 = 'teary-eyed-3'
OTHER_TIRED = 'tired'
OTHER_VERY_HAPPY = 'very-happy'
OTHER_YAWN = 'yawn'

OTHER_UNKNOWN = 'unknown'
CRUFT = None

# Expressions for forms that don't get their own Pokémon ID
# XXX This is kind of hackish; it'll break if we ever want separate delimiters
PURPLE_STANDARD = 'purple'     # These two are only
PURPLE_ANGRY = 'purple-angry'  # necessary in Blue
CHEST_STANDARD = 'chest'

_sky_default = {
    0: STANDARD,
    1: GRIN,
    2: PAINED,
    3: ANGRY,
    4: WORRIED,
    5: SAD,
    6: CRYING,
    7: SHOUTING,
    8: TEARY_EYED,
    9: DETERMINED,
    10: JOYOUS,
    11: INSPIRED,
    12: SURPRISED,
    13: DIZZY,

    16: SIGH,
    17: STUNNED
}

# Sky cruft: Leftovers from Blue and placeholder sprites.  These take care of
# a lot of Sky's special cases.
_sky_cruft_pokemon = [
    '54', '66', '104',  # Retired protagonist Pokémon species

    '6', '9', '10', '23', '56', '65', '94', '189', '209', '248', '271',
    '275', '340', '359', '380', '381',  # Retired NPC Pokémon species

    '38', '144', '145', '146', '178', '384'  # Pokémon with placeholders
]

_sky_special_cases = {
    ('76', 6): OTHER_UNKNOWN,  # Standard expression, but shiny colour scheme?

    ('40', 7): OTHER_FAINTED,
    ('40', 16): OTHER_VERY_HAPPY,
    ('40', 17): OTHER_EXTREMELY_HAPPY,
    ('40', 18): DETERMINED,  # YOOM-TAH

    ('40-mama', 16): OTHER_VERY_HAPPY,
    ('40-mama', 17): OTHER_EXTREMELY_HAPPY,
    ('40-mama', 18): DETERMINED,  # YOOM-TAH

    ('69', 1): PAINED,

    ('93', 16): JOYOUS,

    ('96', 16): SAD,

    ('132', 16): CHEST_STANDARD,

    ('174', 16): ANGRY,  # No background zigzag
    ('174', 17): OTHER_EXTREMELY_HAPPY,
    ('174', 18): DETERMINED,  # YOOM-TAH

    ('183', 16): SAD,

    ('192', 16): OTHER_BLUSHING,
    ('192', 17): OTHER_HURT,

    ('206', 16): OTHER_BLUSHING,
    ('206', 17): STUNNED,

    ('218', 16): OTHER_HURT,

    ('251', 16): OTHER_BLUSHING,

    ('251-shiny', 16): OTHER_BLUSHING,
    ('251-shiny', 17): OTHER_TEARY_EYED_2,  # All nearly identical but distinct
    ('251-shiny', 18): OTHER_TEARY_EYED_3,  # (and with the wrong background)

    ('253', 16): SAD,
    ('253', 17): OTHER_BOUND,
    ('253', 18): OTHER_HURT,

    ('282', 16): PAINED,

    ('294', 16): TEARY_EYED,  # Wrong background
    ('294', 18): OTHER_ASLEEP,

    ('298', 16): CRYING,  # Background like teary-eyed

    ('302', 16): OTHER_PANIC,  # Background like angry, complete with zigzag

    ('303', 16): STUNNED,  # Funky background

    ('308', 16): OTHER_PROUD,

    ('324', 16): SAD,

    ('327', 16): GRIN,  # Flowery background

    ('332', 16): PAINED,

    ('383', 6): OTHER_UNKNOWN,  # Bottom lip slightly different — cruft?

    ('385', 1): OTHER_ASLEEP,

    ('399', 16): OTHER_BLUSHING,
    ('399', 17): OTHER_VERY_HAPPY,
    ('399', 18): STUNNED,

    ('428', 16): STUNNED,

    ('441', 16): TEARY_EYED,  # Background like grin et al
    ('441', 18): CRYING,

    ('442', 16): STUNNED,

    ('446', 18): OTHER_DROOLING,

    ('467', 16): PAINED,  # Pained?  Startled?

    ('477', 16): OTHER_CONTEMPT,
    ('477', 17): OTHER_FURTHER_CONTEMPT,

    ('490', 16): OTHER_YAWN,
    ('490', 17): OTHER_TIRED,
    ('490', 18): OTHER_SICK,

    ('492-land', 14): SIGH,  # Pink background
}

_blue_default = [
    STANDARD,
    GRIN,
    PAINED,
    ANGRY,
    WORRIED,  # Some of these are different from Sky; they look more annoyed
    SAD,
    CRYING,
    SHOUTING,
    TEARY_EYED,
    HAPPY,
    JOYOUS,
    INSPIRED,
    SURPRISED,
]

_blue_special_cases = {
    ('6', 1): (SURPRISED, False),
    ('6', 2): (GRIN, False),
    ('6', 3): (PAINED, False),
    ('6', 4): (TEARY_EYED, False),

    ('9', 2): (ANGRY, False),
    ('9', 3): (PAINED, False),

    ('10', 1): (INSPIRED, False),
    ('10', 2): (TEARY_EYED, False),

    ('23', 1): (SURPRISED, False),
    ('23', 2): (GRIN, False),  # Pink background—determined?

    ('50', 1): (PAINED, False),

    ('65', 1): (SURPRISED, False),
    ('65', 2): (GRIN, False),

    ('69', 1): (PAINED, False),

    ('81', 1): (JOYOUS, False),

    ('94', 2): (ANGRY, False),
    ('94', 3): (PAINED, False),
    ('94', 5): (CRYING, False),
    ('94', 6): (SURPRISED, False),

    ('189', 1): (SAD, False),

    ('209', 1): (SURPRISED, False),
    ('209', 2): (TEARY_EYED, False),

    ('227', 1): (CRUFT, False),  # Placeholder

    ('248', 1): (SURPRISED, False),

    ('271', 1): (ANGRY, False),
    ('271', 2): (GRIN, False),
    ('271', 3): (TEARY_EYED, False),
    ('271', 4): (STANDARD, True),
    ('271', 5): (ANGRY, True),
    ('271', 6): (GRIN, True),
    ('271', 7): (TEARY_EYED, True),

    ('275', 1): (SURPRISED, False),
    ('275', 2): (GRIN, False),

    ('308', 2): (SURPRISED, False),
    ('308', 3): (OTHER_PROUD, False),
    ('308', 5): (ANGRY, False),
    ('308', 6): (SAD, False),

    ('327', 1): (SAD, False),
    ('327', 2): (STANDARD, True),
    ('327', 3): (SAD, True),

    ('352', 1): (ANGRY, False),
    ('352', 2): (PURPLE_STANDARD, False),
    ('352', 3): (PURPLE_ANGRY, False),

    ('359', 1): (STANDARD, True),

    ('385', 1): (OTHER_ASLEEP, False),

    ('446', 1): (OTHER_DROOLING, False),
    ('446', 2): (JOYOUS, False),
    ('446', 3): (GRIN, False),  # Matches Sky; looks more like Blue's HAPPY
    ('446', 4): (INSPIRED, False),  # Matches Sky; out of place for Blue
}

def sky(pokemon, sprite_num):
    """Given a Pokémon and sprite number, return information about the
    corresponding portrait sprite from Explorers of Sky.

    The return value is a tuple consisting of two values:

    - A string identifier for the Pokémon's facial expression

    - A boolean indicating whether the Pokémon is facing to its right
    """

    if sprite_num > 1 and pokemon.identifier in _sky_cruft_pokemon:
        return (CRUFT, False)

    is_right = sprite_num % 2 == 1
    sprite_num //= 2

    key = (pokemon.identifier, sprite_num)
    if key in _sky_special_cases:
        expression = _sky_special_cases[key]
    else:
        expression = _sky_default[sprite_num]

    return (expression, is_right)

def blue(pokemon, sprite_num):
    """Given a Pokémon identifier and sprite number, return information about the
    corresponding portrait sprite from Blue Rescue Team.

    Return values are as in sky().
    """

    key = (pokemon.identifier, sprite_num)
    if key in _blue_special_cases:
        return _blue_special_cases[key]
    else:
        return (_blue_default[sprite_num], False)
