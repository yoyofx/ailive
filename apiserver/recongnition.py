"""
实时语音识别测试
"""
import speech_recognition as sr
import logging
import torch
logging.basicConfig(level=logging.DEBUG)

print(torch.cuda.is_available())
print(torch.__version__)

class AudioRecognizer():
    loopFlag = 0
    def __init__(self,name,phrase_time_limit=5,model='base',language='Chinese'):
        self.name = name
        self.phrase_time_limit = phrase_time_limit
        self.model = model
        self.language = language

    def StartAways(self):
        logging.info('start')
        self.loopFlag = 1
        while self.loopFlag == 1:
            r = sr.Recognizer()
            # 麦克风
            mic = sr.Microphone()

            logging.info('录音中...')
            with mic as source:
                # r.adjust_for_ambient_noise(source)
                audio = r.listen(source,timeout=3,phrase_time_limit= self.phrase_time_limit)
            logging.info('录音结束，识别中...')
            test = r.recognize_whisper(audio,model=self.model, language=self.language)
            print(test)
            logging.info('end')

    def StopAways(self):
        self.loopFlag = 0


    def ListenRecognize(self):
        logging.info('start')
        r = sr.Recognizer()
        # 麦克风
        mic = sr.Microphone()
        logging.info('录音中...')
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source,phrase_time_limit= self.phrase_time_limit)
        logging.info('录音结束，识别中...')
        text = r.recognize_whisper(audio,model=self.model, language=self.language)
        return text

audioRecognizer = AudioRecognizer(name='小东')
audioRecognizer.StartAways()