import discord
import pyvcroid2
import asyncio
import pyvcvox
from discord.ext import tasks

class control(pyvcroid2.VcRoid2,pyvcvox.vcvox):
    def __init__(self):
        self.speakertype="roid"
        self.ch=None
        pyvcroid2.VcRoid2.__init__(self)
        pyvcvox.vcvox.__init__(self)


    def speak(self,text):
        if self.speakertype=="roid":
            lang_list = ctrl.listLanguages()
            if "standard" in lang_list:
                ctrl.loadLanguage("standard")
            elif 0 < len(lang_list):
                ctrl.loadLanguage(lang_list[0])
            self.param.volume = 1.00
            self.param.speed = 1.2
            self.param.pitch = 1.1
            self.param.emphasis = 0.95
            self.param.pauseMiddle = 80
            self.param.pauseLong = 100
            self.param.pauseSentence = 100
            self.param.masterVolume = 1.123
            filename = "temp.wav"
            speech, tts_events = self.textToSpeech(text)

            with open(filename, mode="wb") as f:
                f.write(speech)
        elif self.speakertype=="vox":
            with open("temp.wav", mode="wb") as f:
                f.write(self.texttosound(text))
        
        return "temp.wav"


with control() as ctrl: 
    TOKEN = ''
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    #起動
    async def on_ready():
        print('ログインしました')
        await client.change_presence(activity=discord.Game(name="読み上げ"))
        ctrl.loadVoice(ctrl.listVoices()[0])

    @client.event
    async def on_message(message):
        #botは無視
        if message.author.bot:
            return
        #ボイスチャンネルに参加
        if message.content == "!join":
            if message.author.voice is None:
                await message.channel.send("ボイスチャンネルに接続してください")
                return

            await message.author.voice.channel.connect()
            await message.channel.send("接続しました")
            
            ctrl.ch=message.channel

        #呼ばれたチャンネル以外は無視
        elif message.channel==ctrl.ch:
            #退出
            if message.content == "!leave":
                if message.guild.voice_client is None:
                    await message.channel.send("接続していません")
                    return

                await message.guild.voice_client.disconnect()

                await message.channel.send("切断しました。")



            #ソフトの切り替え
            elif message.content=="!vcchange":
                if ctrl.speakertype=="roid":
                    ctrl.speakertype="vox"
                else:
                    ctrl.speakertype="roid"
            
            #話者IDの表示
            elif "!vclist" in message.content:
                if ctrl.speakertype=="roid":
                    voice_list = ctrl.listVoices()
                    if 0 < len(voice_list):
                        for i,j in enumerate(voice_list):
                            await message.channel.send("{}:{}".format(i,j))
                    else:
                        raise Exception("No voice library")
                
                else:
                    await message.channel.send("2:四国めたん\n3:ずんだもん\n8:春日つむぎ")
            #話者の切り替え
            elif "!vcset" in message.content:
                    
                if ctrl.speakertype=="roid":
                    voice_list = ctrl.listVoices()
                    if 0 < len(voice_list):
                        number=message.content.split()
                        number=number[1]
                        ctrl.loadVoice(voice_list[int(number)])
                    else:
                        raise Exception("No voice library")

                else:
                    number=message.content.split()
                    number=number[1]
                    ctrl.speaker=number
            #テキストは読み上げる
            else:
                while message.guild.voice_client.is_playing():
                            await asyncio.sleep(0.1)
                
                source=discord.FFmpegPCMAudio(ctrl.speak(message.content))
                message.guild.voice_client.play(source)

    client.run(TOKEN)
