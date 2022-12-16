import requests
import json


class vcvox():
    def __init__(self):
        self.speaker=3
        self.text=None
        self.query=None
        self.sound=None
    
    def get_query(self):
        self.query=requests.post("http://localhost:50021/audio_query",params=(("text",self.text),("speaker",self.speaker)))



    def get_synthesis(self):
        self.sound=requests.post("http://localhost:50021/synthesis",params={"speaker":self.speaker},data=json.dumps(self.query.json()))
    
    def texttosound(self,text):
        self.text=text
        self.get_query()
        self.get_synthesis()

        return self.sound.content







    