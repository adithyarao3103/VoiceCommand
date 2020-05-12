#code for voice commands

import speech_recognition as sr
import socket
import os
import sys
import tkinter as tk
from tkinter.ttk import *
import wave
import pyaudio
import time
import pyttsx3
import webbrowser
import wikipedia
from playsound import playsound

global win
global ttseng

pypa = __file__
mic = sr.Microphone()
r = sr.Recognizer()

ttseng = pyttsx3.init()
ttseng.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')

REMOTE_SERVER = "one.one.one.one"

def is_connected(hostname):
    try:
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        pass
    return False

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 6
out = "rec.wav"
audio = pyaudio.PyAudio()

def listen():
    global lst
    lst = tk.Text(win, height = 1, width = 50)
    lst.insert(tk.INSERT, "Listening....")
    lst.pack()
    win.update()
    playsound('beg.mp3')
    
    stream = audio.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer= CHUNK, input_device_index = 1)
    frames = []

    for i in range(0, int(RATE/ CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()
 
    waveFile = wave.open(out, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    playsound('end.mp3')

def implement(command):
    srcom = command.partition(' ')[0]
    print(srcom)
    
    if command == "hello" or command == "hey" or command == "hey there":
        mssge = tk.Text(win, height = 2, width = 50)
        mssge.insert(tk.INSERT, "Hey there!!! \nHow can I help you")
        mssge.pack()
        win.update()
        sen = 'Hey there!  How can I help you?'
        ttseng.say(sen)
        ttseng.runAndWait()
        time.sleep(1)
        mssge.pack_forget()      
        
    elif command == "what is the time" or command == "time" or command == "current time" or command == "what is time":
        var = time.ctime()
        mssge = tk.Text(win, height = 1, width = 50)
        mssge.insert(tk.INSERT, "It is " + var)
        mssge.pack()
        win.update()
        sen = 'it is ' + var
        ttseng.say(sen)
        ttseng.runAndWait()
        time.sleep(1)
        mssge.pack_forget()

    elif srcom == "search":
        srch = command.split(' ', 1)[1]
        link = 'https://www.google.com/search?q={}'.format(srch)
        mssge = tk.Text(win, height = 2, width = 50)
        mssge.insert(tk.INSERT, "Searching Google for " + srch)
        mssge.pack()
        win.update()
        sen = 'searching google for ' + srch
        ttseng.say(sen)
        ttseng.runAndWait()
        webbrowser.open(link, new = 2)
        time.sleep(1)
        mssge.pack_forget()

    elif srcom == "calculate":
        inp = command.split(' ',1)[1]
        for entry in inp:
            if entry == 'x':
                inp = inp.replace('x', '*')
            elif entry == 'X':
                inp = inp.replace('X', '*')
            elif entry == 'd':
                inp = inp.replace('d', '')
            elif entry == 'i':
                inp = inp.replace('i', '')
            elif entry == 'v':
                inp = inp.replace('v', '')
            elif entry == 'e':
                inp = inp.replace('e', '')
            elif entry == 'b':
                inp = inp.replace('b', '')
            elif entry == 'y':
                inp = inp.replace('y', '/')
        val = str(eval(inp))
        mssge = tk.Text(win, height = 1, width = 50)
        mssge.insert(tk.INSERT, inp + ' = ' + val)
        mssge.pack()
        win.update()
        sen = inp + ' = ' + val
        ttseng.say(sen)
        ttseng.runAndWait()
        time.sleep(3)
        mssge.pack_forget()   
            
    elif srcom == "wiki" or srcom == "wikipedia":
        topic = command.split(' ', 1)[1]
        try:
            spe = wikipedia.summary(topic, sentences = 2)
            mssge = tk.Text(win, height = 20, width = 50)
            mssge.insert(tk.INSERT, "According to Wikipedia:\n" + spe)
            mssge.pack()
            win.update()
            sen = 'according to wikipedia,  ' + spe
            ttseng.setProperty('rate', 150)
            ttseng.say(sen)
            ttseng.runAndWait()
            time.sleep(1)
            mssge.pack_forget()   
        except wikipedia.exceptions.DisambiguationError:
            mssge = tk.Text(win, height = 1, width = 50)
            mssge.insert(tk.INSERT, "The topic was ambigous")
            mssge.pack()
            win.update()
            sen = 'the topic was ambigous'
            ttseng.say(sen)
            ttseng.runAndWait()
            time.sleep(1)
            mssge.pack_forget()          
                           
    else:
        mssge = tk.Text(win, height = 2, width = 50)
        mssge.insert(tk.INSERT, command+"\ncommand not found")
        mssge.pack()
        win.update()
        sen = command + '  command not found'
        ttseng.say(sen)
        ttseng.runAndWait()
        time.sleep(1)
        mssge.pack_forget()
    
def recognize():
    listen()
    audio = sr.AudioFile('rec.wav')
    with audio as source:
        inaud = r.record(source)

    try:
        command = r.recognize_google(inaud).lower()
    except sr.UnknownValueError:
        mssge = tk.Text(win, height = 1, width = 50)
        mssge.insert(tk.INSERT, "Could not understand what you said")
        mssge.pack()
        win.update()
        sen = 'couldnt understand what you said'
        ttseng.say(sen)
        ttseng.runAndWait()
        time.sleep(3)
        lst.pack_forget()
        mssge.pack_forget()

    command = r.recognize_google(inaud).lower()

    os.remove("rec.wav")

    print(command)

    implement(command)

def butt():
    recognize()
    time.sleep(1)
    lst.pack_forget()

win = tk.Tk()
win.geometry("300x500")
win.title("Voice Command")
path = os.getcwd()
photo = tk.PhotoImage(file = path + r'\voice.png' )
b = tk.Button(win, image = photo, command = butt)
b.pack()
var = tk.StringVar()
var.set("Click on the mic icon..")
mssge = tk.Label(win, textvariable = var)
mssge.pack()


if is_connected(REMOTE_SERVER) == False:
    mssge = tk.Text(win, height = 1, width = 50)
    mssge.insert(tk.INSERT, "Please connect to internet..")
    mssge.pack()
    win.update()
    sen = 'Please connect to the internet'
    ttseng.say(sen)
    ttseng.runAndWait()
    time.sleep(1)
    exit()

win.mainloop()

#code by Adithya A Rao

