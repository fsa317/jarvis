from polly import Polly

print("Starting TTS")
tts = Polly('Brian')
#tts.say('Hi there, I\'m very glad you\'re reading my article. Leave a comment if you find it useful.')
fname = tts.processText('Test from laptop, with some more text')
print(fname)
