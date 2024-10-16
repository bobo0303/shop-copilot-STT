from pydantic import BaseModel
import torch

#############################################################################

class ModlePath(BaseModel):
    paraformer: str = "models/paraformer-zh"
    sensevoice: str = "models/SenseVoiceSmall"

#############################################################################
""" options for inference """
OPTIONS = {
    "language": "auto",
    "itn": True,
    "ban_emo_unk": False,
}

#############################################################################

