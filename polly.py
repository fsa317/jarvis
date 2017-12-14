import boto3
import pygame
import os
import time
import io
import hashlib
import sys
import os.path

class Polly():
    OUTPUT_FORMAT='mp3'
    DIRECTORY='/home/pi/tts/ttscache'

    def __init__(self, voiceId):
        self.polly = boto3.client('polly') #access amazon web service
        self.VOICE_ID = voiceId

    def processText(self, text):
        ssml = "<speak> "+text+"</speak>"
        fname = self.getFileName(ssml)
        if not os.path.isfile(fname):
            self.saveToFile(ssml,fname)
        self.playMp3(fname)
        return fname

    def getFileName(self,text):
        hash = hashlib.md5(text.encode()).hexdigest()
        fname = self.DIRECTORY + "/tts_"+hash+".mp3"
        return fname

    def saveToFile(self, textToSpeech, fileName): #get polly response and save to file
        print("Calling polly")
        pollyResponse = self.polly.synthesize_speech(Text=textToSpeech, OutputFormat=self.OUTPUT_FORMAT, VoiceId=self.VOICE_ID, TextType="ssml")
        print("Polly Response")
        with open(fileName, 'wb') as f:
            f.write(pollyResponse['AudioStream'].read())
            f.close()

    def playMp3(self, fileName):
        #cmd = 'omxplayer -o local '+fileName;
        cmd = 'mpg321 -g 100 '+fileName
        print("CMD: "+cmd)
        os.system(cmd)

    def cleanup(self):
        now = time.time()
        cutoff = now - (3 * 86400)
        cachedir = self.DIRECTORY
        files = os.listdir(cachedir)
        for xfile in files:
                if os.path.isfile(cachedir+"/" + xfile ):
                        t = os.stat(cachedir+"/" + xfile )
                        c = t.st_ctime
                        # delete file if older than a week
                        if c < cutoff:
                                os.remove(cachedir+"/" + xfile)

    def say(self, textToSpeech): #get polly response and play directly
        pollyResponse = self.polly.synthesize_speech(Text=textToSpeech, OutputFormat=self.OUTPUT_FORMAT, VoiceId=self.VOICE_ID)

        pygame.mixer.init()
        pygame.init()  # this is needed for pygame.event.* and needs to be called after mixer.init() otherwise no sound is played

        if os.name != 'nt':
            pygame.display.set_mode((1, 1)) #doesn't work on windows, required on linux

        with io.BytesIO() as f: # use a memory stream
            f.write(pollyResponse['AudioStream'].read()) #read audiostream from polly
            f.seek(0)
            pygame.mixer.music.load(f)
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            pygame.event.set_allowed(pygame.USEREVENT)
            pygame.mixer.music.play()
            pygame.event.wait() # play() is asynchronous. This wait forces the speaking to be finished before closing

        while pygame.mixer.music.get_busy() == True:
            pass
