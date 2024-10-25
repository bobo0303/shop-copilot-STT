from pydantic import BaseModel

#############################################################################

class ModlePath(BaseModel):
    paraformer: str = "models/speech_paraformer_asr-en-16k-vocab4199-pytorch"
    sensevoice: str = "models/SenseVoiceSmall"

#############################################################################

""" options for inference """
OPTIONS = {
    "language": "en",
    "hotword": "go, to, setting, page, next, accept, decline, start, checkout, back, previous, page, use, coupon, pay, payment, main, scan, with, card, nfc",
    "itn": True,
    "ban_emo_unk": False,
}

#############################################################################

""" 示例 ACTION 熱詞列表 """
ACTION_HOTWORDS = [  
    "go to setting page",  
    "go to next page",  
    "accept",  
    "decline",  
    "start checkout",  
    "back to previous page",  
    "use coupon",  
    "go to payment",  
    "go to previous page",  
    "back to main page",  
    "back to scan",  
    "pay with card",  
    "pay with nfc",
    "pay with n fc",
]  

#############################################################################

ACTIONS = {
    "go to setting page": 1, "go to next page": 2, "accept": 3, "decline": 4, "start checkout": 5, "back to previous page": 6, "use coupon": 7, 
    "go to payment": 8, "go to previous page": 9, "back to main page": 10, "back to scan": 11, "pay with card": 12, "pay with nfc": 12, "pay with n fc": 12,
}

#############################################################################

""" command  """
COMMAND_DICTIONARY = [
    "go", "to", "pay", "setting", "page", "next", "accept", "decline", "start", "checkout", "back", 
    "previous", "page", "use", "coupon", "payment", "main", "scan", "with", "card", "nfc",
]

#############################################################################
""" options for contral punc or not """
IS_PUNC = False

#############################################################################
