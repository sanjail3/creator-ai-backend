import enum
class Operation(enum.Enum):
    tts = "tts"
    asr = "asr"
    translation = "translation"
    transliteration = "transliteration"


class Language(enum.Enum):
    english = "en"
    hindi = "hi"
    tamil = "ta"
    telugu = "te"
    kannada = "kn"
    malayalam = "ml"
    bengali = "bn"
    gujarati = "gu"
    marathi = "mr"
    punjabi = "pa"
    urdu = "ur"

class pipelineId(enum.Enum):
    MeitY = "64392f96daac500b55c543cd"
    AI4Bharat = "643930aa521a4b1ba0f4c41d"
