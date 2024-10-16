目前只使用 paraformer-zh 和 SenseVoiceSmall (默認) 自己下載放在這裡

(Note: ⭐ represents the ModelScope model zoo, 🤗 represents the Huggingface model zoo, 🍀 represents the OpenAI model zoo)


|                                                                                                         Model Name                                                                                                         |                                   Task Details                                   |          Training Data           | Parameters |
|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------:|:--------------------------------:|:----------:|
|                                        SenseVoiceSmall <br> ([⭐](https://www.modelscope.cn/models/iic/SenseVoiceSmall)  [🤗](https://huggingface.co/FunAudioLLM/SenseVoiceSmall) )                                         | multiple speech understanding capabilities, including ASR, ITN, LID, SER, and AED, support languages such as zh, yue, en, ja, ko   |           300000 hours           |    234M    |
|          paraformer-zh <br> ([⭐](https://www.modelscope.cn/models/damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch/summary)  [🤗](https://huggingface.co/funasr/paraformer-zh) )           |                speech recognition, with timestamps, non-streaming                |      60000 hours, Mandarin       |    220M    |


## License
This project is licensed under [The MIT License](https://opensource.org/licenses/MIT). FunASR also contains various third-party components and some code modified from other repos under other open source licenses.
The use of pretraining model is subject to [model license](./MODEL_LICENSE)


## Citations
``` bibtex
@inproceedings{gao2023funasr,
  author={Zhifu Gao and Zerui Li and Jiaming Wang and Haoneng Luo and Xian Shi and Mengzhe Chen and Yabin Li and Lingyun Zuo and Zhihao Du and Zhangyu Xiao and Shiliang Zhang},
  title={FunASR: A Fundamental End-to-End Speech Recognition Toolkit},
  year={2023},
  booktitle={INTERSPEECH},
}
@inproceedings{An2023bat,
  author={Keyu An and Xian Shi and Shiliang Zhang},
  title={BAT: Boundary aware transducer for memory-efficient and low-latency ASR},
  year={2023},
  booktitle={INTERSPEECH},
}
@inproceedings{gao22b_interspeech,
  author={Zhifu Gao and ShiLiang Zhang and Ian McLoughlin and Zhijie Yan},
  title={Paraformer: Fast and Accurate Parallel Transformer for Non-autoregressive End-to-End Speech Recognition},
  year=2022,
  booktitle={Proc. Interspeech 2022},
  pages={2063--2067},
  doi={10.21437/Interspeech.2022-9996}
}
@inproceedings{shi2023seaco,
  author={Xian Shi and Yexin Yang and Zerui Li and Yanni Chen and Zhifu Gao and Shiliang Zhang},
  title={SeACo-Paraformer: A Non-Autoregressive ASR System with Flexible and Effective Hotword Customization Ability},
  year={2023},
  booktitle={ICASSP2024}
}
```
