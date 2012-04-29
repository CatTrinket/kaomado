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

# Other Sky categories
SIGH = 'sigh'
SWEATDROP = 'sweatdrop'  # XXX better name?
MISC = 'misc'  # XXX temporary; sort these properly

# Other Blue categories
HAPPY = 'happy'

sky = [
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
    MISC,
    None
]

blue = [
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
