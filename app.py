import re
import time
import os
import random

from selenium import webdriver

# Package for the model speech
import playsound
from gtts import gTTS
# Package for voice input and translating into file format
import openai
import sounddevice as sd
import soundfile as sf

# Representing whether the program is running or not
current_status = 0
# Where we execute this program
driver = webdriver.Chrome('')  # Use own path for testing

# Generating voice responses
def model_speak(voice_data):
    gtts = gTTS(text=voice_data, lang='en')
    r = random.randint(1,100)
    audio_file = 'audio_' +str(r)+'.mp3'
    gtts.save(audio_file)
    print(voice_data)
    playsound.playsound(audio_file)
    os.remove(audio_file)

model_speak("What can I help you?")

# setting for voice input
duration = 3  # recording duration in seconds
sample_rate = 44100  # audio sample rate
channels = 1  # number of audio channels

# Take input(voice) and translate into mp3 format
def user_speak(langdetect=None):
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)
    sd.wait()
    r = random.randint(1, 100)

    # Save audio to MP3 file
    filename = "audio_" +str(r)+".mp3"
    sf.write(filename, audio, sample_rate)

    # Transcribe audio using OpenAI API
    openai.api_key = ""  # Use your own key

    with open(filename, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)
    
    os.remove(filename)
    return transcript['text'].lower()


def respond(voice_data):
    if re.match("open\sgoogle", voice_data):
        driver.get('http://google.com')
        model_speak("Is there anything more I can do for you?")
    elif re.match("open\syoutube", voice_data):
        driver.get('http://youtube.com')
        model_speak("Is there anything more I can do for you?")
    elif re.match("stop", voice_data):
        time.sleep(10)
    elif re.match(r"^search\s+", voice_data):
        model_speak("Identifying speech...")
        words = voice_data.split()
        search_string = ''
        for word in range(1, len(words)):
            search_string += words[word]
            url = 'http://google.com/search?q=' + search_string
        driver.get('http://google.com/search?q=' + search_string)
        model_speak("Is there anything more I can do for you?")
    elif re.match(r"create\snew\stab", voice_data):
        driver.execute_script("window.open('');")
        model_speak("Is there anything more I can do for you?")
    elif re.match(r"switch\stab", voice_data):
        num_of_tabs = len(driver.window_handles)
        current_tab = 0
        for i in range(num_of_tabs):
            if driver.window_handles[i] == driver.current_window_handle:
                if i != num_of_tabs - 1:
                    current_tab = i + 1
                    break
        driver.switch_to.window(driver.window_handles[current_tab])
        model_speak("Is there anything more I can do for you?")
    elif re.match(r"close\stab", voice_data):
        driver.close()
        model_speak("Is there anything more I can do for you?")
    elif re.match(r"go\sback", voice_data):
        driver.back()
        model_speak("Is there anything more I can do for you?")
    elif re.match(r"go\sforward", voice_data):
        driver.forward()
    elif re.match(r"exit", voice_data):
        model_speak("See you next time sir")
        driver.quit()
    else:
        model_speak("Invalid command, please try again")
        exit()


while True:

    voice_data = user_speak()
    print(voice_data)
    respond(voice_data)

