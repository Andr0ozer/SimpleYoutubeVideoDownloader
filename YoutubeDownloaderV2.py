import requests
import PySimpleGUI as sg
from time import sleep
import threading
from pytube import YouTube
import os

def isvalid(link):
    if len(link) <=8 :
        return False
    
    start = 'https://'
    for i in range(7):
        if link[i] != start[i]:
            return False

    r = requests.get(link)
    if "Video unavailable" in r.text:
        return False
    return True

def removebadchar(name):
    bad = "/\\:*?\"<>|"
    for i in range(8):
        name = name.replace(bad[i], '')
    
    return name


def download_linkmp4(link, folder):
    sleep(0.5)
    if isvalid(link):
        ytlink = YouTube(link)
        ytdownload = ytlink.streams.get_highest_resolution()
        base = ytdownload.title
        base = removebadchar(base)
        new_file = base + '.mp4'
        i = 0
        while(os.path.isfile(folder + "/" + new_file)):
            i = i + 1
            new_file = base + str(i) + '.mp4'
        ytdownload.download(folder, new_file)
        sg.Popup("Downloaded " + new_file)
    else:
        sg.Popup("Invalid URL")

def download_linkmp3(link, folder):
    sleep(0.5)
    if isvalid(link):
        ytlink = YouTube(link)
        ytdownload = ytlink.streams.filter(only_audio = True).first()
        base = ytdownload.title
        base = removebadchar(base)
        new_file = base + '.mp3'
        i = 0
        while(os.path.isfile(folder + "/" +new_file)):
            i = i + 1
            new_file = base + str(i) + '.mp3'
        ytdownload.download(folder, new_file)
        sg.Popup("Downloaded " + new_file)
    else:
        sg.Popup("Invalid URL")

sg.theme('DarkAmber') 

layout = [[sg.Text("YouTube link:")], [sg.In(key="link")], [sg.Button("Download MP4")], [sg.Button("Download MP3")], [sg.Text("Please Select a Folder")], [sg.In(key=("folder")), sg.FolderBrowse()]]

# Create the window
window = sg.Window("YouTube downloader", layout, size=(410, 200))

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break

    if event == "Download MP4":
        if values["link"] != "" and values["folder"] !="":  
            t = threading.Thread(target=download_linkmp4(values["link"], values["folder"]),name="download")
            t.daemon = True
            t.start()
        else:
            sg.Popup("ERROR! PLEASE INPUT BOTH A LINK AND A FOLDER.")
    if event == "Download MP3":
        if values["link"] != "" and values["folder"] !="":  
            t = threading.Thread(target=download_linkmp3(values["link"], values["folder"]),name="download")
            t.daemon = True
            t.start()
        else:
            sg.Popup("ERROR! PLEASE INPUT BOTH A LINK AND A FOLDER.")
    

window.close()