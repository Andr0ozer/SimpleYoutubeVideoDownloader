import requests
import PySimpleGUI as sg
from time import sleep
import threading
from pytube import YouTube

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

def download_link(link, folder):
    sleep(0.5)
    if isvalid(link):
        ytlink = YouTube(link)
        ytdownload = ytlink.streams.get_highest_resolution()
        ytdownload.download(folder)
        print("Done!")
    else:
        sg.Popup("Invalid URL")

sg.theme('DarkAmber') 

layout = [[sg.Text("YouTube link:")], [sg.In(key="link")], [sg.Button("OK")], [sg.Text("Please Select a Folder")], [sg.In(key=("folder")), sg.FolderBrowse()]]

# Create the window
window = sg.Window("YouTube downloader", layout, size=(410, 150))

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break

    if event == "OK":
        if values["link"] != "" and values["folder"] !="":  
            t = threading.Thread(target=download_link(values["link"], values["folder"]),name="download")
            t.daemon = True
            t.start()
        else:
            sg.Popup("ERROR! PLEASE INPUT BOTH A LINK AND A FOLDER.")
    

window.close()