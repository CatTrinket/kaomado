from collections import defaultdict

### Assign all the expressions to constants to minimize opportunity for typos
# Expressions with "official" names from the Sky debug menu
STANDARD = 'standard'
GRIN = 'grin'
PAINED = 'pained'
ANGRY = 'angry'
WORRIED = 'worried'
SAD = 'sad'
CRYING = 'crying'
SHOUTING = 'shouting'
TEARY_EYED = 'teary-eyed'
DETERMINED = 'determined'
JOYOUS = 'joyous'
INSPIRED = 'inspired'
SURPRISED = 'surprised'
DIZZY = 'dizzy'

# Other consistent Sky categories
SIGH = 'sigh'
SWEATDROP = 'sweatdrop'  # XXX better name?

# Other consistent Blue categories
HAPPY = 'happy'

# Other
OTHER = 'other'

_sky_default = [
    STANDARD,
    GRIN,
    PAINED,
    ANGRY,
    WORRIED,
    SAD,
    CRYING,
    SHOUTING,
    TEARY_EYED,
    DETERMINED,
    JOYOUS,
    INSPIRED,
    SURPRISED,
    DIZZY,
    None,
    None,
    SIGH,
    SWEATDROP,
    OTHER,
    None
]

# XXX very incomplete
_sky_special_cases = {
    ('492-land', 14): SIGH,  # Background is wrong
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

    ('10', 2): (TEARY_EYED, False),

    ('23', 1): (SURPRISED, False),
    ('23', 2): (GRIN, False),  # Background indicates teary-eyed, but no tears

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
    ('308', 3): (GRIN, False),  # Background indicates teary-eyed, but no tears
    ('308', 5): (ANGRY, False),
    ('308', 6): (SAD, False),

    ('327', 1): (SAD, False),
    ('327', 2): (STANDARD, True),
    ('327', 3): (SAD, True),

    ('352', 1): (ANGRY, False),
    ('352', 2): (STANDARD, False),  # XXX Purple
    ('352', 3): (ANGRY, False),  # XXX Purple

    ('359', 1): (STANDARD, True),

    ('385', 1): (OTHER, False),  # Sleeping

    ('446', 1): (OTHER, False),  # Drooling
    ('446', 2): (JOYOUS, False),
    ('446', 3): (HAPPY, False),
    ('446', 4): (GRIN, False),
}

def sky(pokemon, sprite_num):
    """Given a Pokémon and sprite number, return information about the
    corresponding portrait sprite from Explorers of Sky.

    The return value is a tuple consisting of two values:

    - A string identifier for the Pokémon's facial expression

    - A boolean indicating whether the Pokémon is facing to its right
    """

    is_right = sprite_num % 2 == 1
    sprite_num //= 2

    if pokemon.form is not None:
        identifier = '{0}-{1}'.format(pokemon.national_id, pokemon.form)
    else:
        identifier = str(pokemon.national_id)

    key = (identifier, sprite_num)

    if key in _sky_special_cases:
        expression = _sky_special_cases[key]
    else:
        expression = _sky_default[sprite_num]

    return (expression, is_right)

def blue(pokemon, sprite_num):
    """Given a Pokémon and sprite number, return information about the
    corresponding portrait sprite from Blue Rescue Team.

    Return values are as in sky().
    """

    if pokemon.form is not None:
        identifier = '{0}-{1}'.format(pokemon.national_id, pokemon.form)
    else:
        identifier = str(pokemon.national_id)

    key = (identifier, sprite_num)

    if key in _blue_special_cases:
        expression, is_right = _blue_special_cases[key]
    else:
        expression = _blue_default[sprite_num]
        is_right = False

    return (expression, is_right)
