import time
import xml.etree.ElementTree as ET
import os
from pytube import YouTube
from moviepy.editor import VideoFileClip
import subprocess as sp
from tkinter import filedialog
import re

# To do list
# Choose launch box folder / done
# Choose FFmpeg location (or include it)
# Better game searching /  matching
# make millions

# Bit of Code to check for launchbox folder
brokenlinks = []

# Quality of video ( 1=Highest /  0 = lowest ) (Genrally, lowest is fine for most videos and is faster at downloads/processing )
qulaity = 0

def get_launchbox_location():
    home = os.path.expanduser("~")
    # Try Find the Launchbox folder location before we begin
    if os.path.isdir((home+"\\Launchbox")):
        open_file = home+"\\Launchbox"
        print("LaunchBox Folder found: "+ open_file)
    else:
        # If i cannot find the Launch box folder, ask the user
        open_file = filedialog.askdirectory(title="Please Choose LaunchBox Directory")
        open_file = open_file.replace("/","\\")
    return open_file

def get_mastergame_list(open_file):
    masterGameData = []
    metadata = open_file + r"\Metadata\Metadata.xml"
    # Crawl huge master metadata file once now
    print("Finding all Games in Master MetaData List...")
    MDtree = ET.parse(metadata)
    MDroot = MDtree.getroot()

    #Get all the video URLS and Matching Game names
    for child in MDroot.findall('Game'):
        if len(child.findall('VideoURL')) != 0:
            masterGameData.append([child.findall('VideoURL')[0].text, child.findall('Name')[0].text])

    # Display Result to user
    print("Complete! " + str(len(masterGameData)) + " Games with videos Found!")
    return masterGameData

def get_ffmpeg_bin():
    if os.path.isdir(os.getcwd() + "\\ffmpeg\\bin\\"):
        ffmpeg_dir = os.getcwd() + "\\ffmpeg\\bin\\"
        print("FFMPEG Executable found: "+ ffmpeg_dir)
    else:
        # If i cannot find the Launch box folder, ask the user
        ffmpeg_dir = filedialog.askdirectory(title="Please Choose FFMPEG.exe Dir")
        ffmpeg_dir = ffmpeg_dir.replace("/","\\")
    return ffmpeg_dir


def split_vid_from_path(video_file_path,newfile, start_time, durration,ffmpeg_binary):
    pipe = sp.Popen(
        [ffmpeg_binary, "-ss", start_time, "-i", video_file_path, "-vcodec", "copy", "-acodec", "copy",
         "-to", durration, newfile])
    pipe.wait()
    return True

def match_master_to_games(masterGameData, open_file):
    # Get YT links from Platform Games
    # Find matching link from Master MetaData list
    # Save a list of YT links, Game Title & Platform name
    # Some Cleaning up of files as well.
    platformFolder = open_file + r"\Data\Platforms"
    platformXMLs = (next(os.walk(platformFolder)))[2]
    listofgamesyt = []
    for x in platformXMLs:
        xml = platformFolder + "\\" + x
        tree = ET.parse(xml)
        root = tree.getroot()
        for game1 in root.findall('Game'):
            for item in game1.findall('VideoUrl'):
                # Next Gamelist item here
                if item.text is not None:
                    for Game2 in masterGameData:
                        if Game2[0] == item.text:

                            gamelist = next(os.walk(open_file + "\\Videos\\" + x[:len(x) - 4] + "\\Trailer"))[2]
                            while x in range(0,len(gamelist)):
                                gamelist[x] = re.sub("[\(\[].*?[\)\]]", "", gamelist[x]).replace("-","").replace("  "," ")
                            if Game2[1].replace(":","") + ".mp4" not in next(os.walk( open_file +"\\Videos\\"+x[:len(x)-4]+"\\Trailer"))[2]:
                                listofgamesyt.append([Game2[0],Game2[1],x[:len(x)-4]])
                                continue
                            else:
                                print("You Already have a video for "+ Game2[1] + ".mp4!")
                                continue
                        else:
                            # Lazy coiding... couldnt find matching link... addding it to broken list
                            tmp = game1.findall('ApplicationPath')[0].text
                            gameFile = re.sub("[\(\[].*?[\)\]]", "", tmp[tmp.rfind('\\') + 1:tmp.rfind('.')])
                            brokenlinks.append(gameFile)
                else:
                    # No link available! Lets add it to a broken list of games
                    tmp = game1.findall('ApplicationPath')[0].text
                    gameFile = re.sub("[\(\[].*?[\)\]]", "", tmp[tmp.rfind('\\')+1:tmp.rfind('.')])
                    brokenlinks.append(gameFile)
    return listofgamesyt

def download_vids(listofgamesyt, open_file, ffmpegloc):
    # Downlaod Videos and Trim them if necessary
    for gamevid in listofgamesyt:
        # Download the Videos to the correct folder
        # where to save
        SAVE_PATH =  open_file +"\\Videos\\" + gamevid[2] + "\\Trailer"

        # link of the video to be downloaded
        link = gamevid[0]

        try:
            # object creation using YouTube
            # which was imported in the beginning
            print(link +" "+ gamevid[2] +" "+ gamevid[1])
            if qulaity == 0:
                YouTube(link).streams.get_lowest_resolution().download(SAVE_PATH)
            else:
                YouTube(link).streams.get_highest_resolution().download(SAVE_PATH)
            time.sleep(1)
            filename = YouTube(link).streams.first().default_filename
            print(filename[:len(filename)-4]+"mp4")
            newfile = SAVE_PATH+ "\\" + gamevid[1].replace(":","")+".mp4"
            os.rename(SAVE_PATH+"\\"+filename[:len(filename)-4]+"mp4",newfile)

            # inefficient but easy way to get video length in seconds
            # gets the video length and trims it based on length
            clip = VideoFileClip(newfile)
            duration = clip.duration
            clip.close()
            if duration > 60 and duration < 300:
                print(duration)
                # Change name back
                time.sleep(1)
                os.rename(newfile,SAVE_PATH + "\\(1)" + gamevid[1].replace(":","")+".mp4")
                # Get ready to change name and cut video!
                split_vid_from_path(SAVE_PATH + "\\(1)" + gamevid[1].replace(":","")+".mp4", newfile, "00:00:29", "00:00:59",ffmpegloc)
                os.remove(SAVE_PATH + "\\(1)" + gamevid[1].replace(":","")+".mp4")
                continue
            elif duration > 300:
                print(duration)
                # Change name back
                time.sleep(1)
                os.rename(newfile, SAVE_PATH + "\\(1)" + gamevid[1].replace(":", "") + ".mp4")
                # Get ready to change name and cut video!
                split_vid_from_path(SAVE_PATH + "\\(1)" + gamevid[1].replace(":", "") + ".mp4", newfile, "00:04:00", "00:01:00",ffmpegloc)
                os.remove(SAVE_PATH + "\\(1)" + gamevid[1].replace(":", "") + ".mp4")
                continue

        except Exception as e:
            # Error when trying to download YT video most likey.... not to worry!
            print(e)
            brokenlinks.append(gamevid[1])

# gets the location of launchbox folder
lbloc = get_launchbox_location()
ffmpegloc = get_ffmpeg_bin()
# Gets the master metadata fields
MgameList = get_mastergame_list(lbloc)
# matches your games to master metadata field
mygames = match_master_to_games(MgameList, lbloc)
# Downloads the videos to correct folder
download_vids(mygames, lbloc, ffmpegloc)

# Lastly, lets look at downloading the last few missing videos
# Need to make a simple youtube parser
print("Missed games:"+ len(brokenlinks))





