from pydantic import BaseModel

#############################################################################

class ModlePath(BaseModel):
    paraformer: str = "models/paraformer-zh"
    sensevoice: str = "models/SenseVoiceSmall"
    punc: str = "models/ct-punc"

#############################################################################
""" options for inference """
OPTIONS = {
    "language": "auto",
    "itn": True,
    "ban_emo_unk": False,
}

#############################################################################
""" options for contral punc or not """
IS_PUNC = True

#############################################################################

