# model.py
import os
import gc
import sys
import time
import torch
import logging  

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.constant import ModlePath, OPTIONS
from .text_postprocess import separate_alphanumeric, hotword_extract, encode_command, extract_sensevoice_result_text
from .typos_postprocess import correct_sentence
from funasr import AutoModel  

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Model:
    def __init__(self):
        """  
        Initialize the Model class with default attributes.  
        """  

        self.model = None
        self.punc_model = None
        self.models_path = ModlePath()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_parameter = {"model": None,
                                 "disable_update": True,
                                 "disable_pbar": True,
                                 "device": self.device,            
                                 }

    def load_model(self, model_name):
        """  Load the specified model based on the model's name.  
          
        :param  
            ----------  
            model_name: str  
                The name of the model to be loaded.  
          
        :rtype  
            ----------  
            None: The function does not return any value.  
          
        :logs  
            ----------  
            Loading status and time.  
        """

        # 實現模型載入的邏輯
        self.model_name = model_name
        start = time.time()

        self._release_model()
        
        if model_name == "paraformer":
            self.model_parameter['model'] = self.models_path.paraformer
        elif model_name == "sensevoice":
            self.model_parameter['model'] = self.models_path.sensevoice
        self.model = AutoModel(**self.model_parameter)
        end = time.time()
                
        logger.info(f"Model '{model_name}' loaded in {end - start:.2f} secomds.")

        if IS_PUNC:
            start = time.time()
            logger.info("Start to loading punch model.")
            self.model_parameter['model'] = self.models_path.punc
            self.punc_model = AutoModel(**self.model_parameter)
            end = time.time()
            logger.info(f"Model \'ct-punc\' loaded in {end - start:.2f} secomds.")

    def _release_model(self):  
        """    
        Release the resources occupied by the current model.  
          
        :param  
        ----------  
        None: The function does not take any parameters.  
          
        :rtype  
        ----------  
        None: The function does not return any value.  
          
        :logs  
        ----------  
        Model release status.  
        """  
        if self.model is not None:  
            del self.model  
            gc.collect()  
            torch.cuda.empty_cache()  
            logger.info("Previous model resources have been released.") 

    def transcribe(self, audio_file_path):
        """  Perform transcription on the given audio file.  
          
        :param  
            ----------  
            audio_file_path: str  
                The path to the audio file to be transcribed.  
          
        :rtype  
            ----------  
            tuple:   
                A tuple containing a dictionary with hotwords, transcription, command number, and the inference time.  
          
        :logs  
            ----------  
            Inference status and time.  
        """  

        # 實現推論的邏輯
        start = time.time()
        result = self.model.generate(audio_file_path, **OPTIONS)
        ori_pred = result[0]['text']
        end = time.time()
        inference_time = end-start
        start = time.time()
        if self.model_name == 'sensevoice':
            ori_pred = extract_sensevoice_result_text(ori_pred.lower())
            
        pred = separate_alphanumeric(ori_pred.lower())
        corrected_pred = correct_sentence(pred)
        hotword, pred = hotword_extract(corrected_pred )
        
        if IS_PUNC:
            pred = self.punc_model.generate(input=pred)
            pred = pred[0]['text']
        
        command_number = encode_command(hotword)
        end = time.time()
        post_process_time = end-start
        logger.debug(f"inference time {inference_time} secomds.")
        logger.debug(f"post process time {post_process_time} secomds.")

        return {"hotword": hotword, "transcription": pred, "command number": command_number}, inference_time
