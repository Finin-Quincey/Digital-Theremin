"""
Scales

Module for computing musical note frequencies and scales.
"""
import re

# Constants
TWELFTH_ROOT_OF_TWO = 2 ** (1/12) # Multiply frequency by this number to move up one semitone
A4 = 440 # Frequency of note A4 in Hz. All other notes are defined relative to this.

NOTE_REGEX = re.compile(r"([A-Ga-g])([#b]?)(-?\d+)$")

# Scales
# Note in key C     C  C# D  Eb E  F  F# G  Ab A  Bb  B
CHROMATIC        = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
MAJOR            = [0,    2,    4, 5,    7,    9,     11]
MINOR            = [0,    2, 3,    5,    7, 8,    10    ]
BLUES            = [0,       3,    5, 6, 7,       10    ]
MAJOR_PENTATONIC = [0,    2,    4,       7,    9        ]
MINOR_PENTATONIC = [0,       3,    5,    7,       10    ]
EASTERN          = [0, 1,       4, 5,    7, 8,        11]
JAPANESE         = [0, 1,          5,    7, 8           ]

SCALES = [
    CHROMATIC        ,
    MAJOR            ,
    MINOR            ,
    BLUES            ,
    MAJOR_PENTATONIC ,
    MINOR_PENTATONIC ,
    EASTERN          ,
    JAPANESE         
]

NOTES = {
    "C" : 0,
    "B#": 0,
    "C#": 1,
    "Db": 1,
    "D" : 2,
    "D#": 3,
    "Eb": 3,
    "E" : 4,
    "Fb": 4,
    "F" : 5,
    "E#": 5,
    "F#": 6,
    "Gb": 6,
    "G" : 7,
    "G#": 8,
    "Ab": 8,
    "A" : 9,
    "A#": 10,
    "Bb": 10,
    "B" : 11,
    "Cb": 11
}


def compute_note_freq(octave, note):
    """
    Computes the freqency of the given note, defined by the octave (as per the standard convention, where middle C is C4*)
    and the note within it (where C is 0, C# is 1, and so on).

    * N.B. Yamaha convention has octaves numbered one lower than usual, i.e. middle C is C3. Just to confuse everyone.
    """
    if note < 0 or note >= 12: raise ValueError("Note must be at least zero and less than 12")
    dist_from_A4 = (note - 9) + (octave - 4) * 12 # Distance from A4 in semitones
    return A4 * TWELFTH_ROOT_OF_TWO ** dist_from_A4


def get_note_freq(note):
    """
    Computes the frequency of the given note, expressed as a string in scientific notation e.g. "A4", "C#3", "Bb4", etc.
    Case-insensitive. Supports negative octaves. Alternative note names may be used (Eb or D#, C or B#, etc.), but
    double-sharps and double-flats are not supported (because they're stupid and unnecessary - this is a micropython library,
    not a jazz book)
    """
    match = NOTE_REGEX.match(note)
    if not match: raise ValueError(f"Invalid note format: {note}")

    note_name = match.group(1).upper() + match.group(2)
    octave = int(match.group(3))

    return compute_note_freq(octave, NOTES[note_name])