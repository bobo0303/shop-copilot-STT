# model.py
import os
import gc
import sys
import time
import torch
import logging  

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.constant import ModlePath, OPTIONS, IS_PUNC
from .text_postprocess import extract_sensevoice_result_text
from funasr import AutoModel  

logger = logging.getLogger(__name__)  

class Model:
    def __init__(self):
        """  
        Initialize the Model class with default attributes.  
        """  

        self.model = None
        self.punc_model = None
        self.models_path = ModlePath()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self. model_parameter = {"model": None,
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
                
        print(f"Model '{model_name}' loaded in {end - start:.2f} secomds.")

        if IS_PUNC:
            start = time.time()
            print("Start to loading punch model.")
            self.model_parameter['model'] = self.models_path.punc
            self.punc_model = AutoModel(**self.model_parameter)
            end = time.time()
            print(f"Model \'ct-punc\' loaded in {end - start:.2f} secomds.")

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
            print("Previous model resources have been released.") 

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
        if IS_PUNC:
            ori_pred = self.punc_model.generate(input=ori_pred)
            ori_pred = ori_pred[0]['text']
        end = time.time()
        inference_time = end-start
        start = time.time()
        if self.model_name == 'sensevoice':
            ori_pred = extract_sensevoice_result_text(ori_pred.lower())

        return ori_pred, inference_time
