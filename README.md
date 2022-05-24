# LB-YTDownload
Launchbox / BigBox Youtube Video Downloader 

This is a simple Python application i made that will download YouTube videos that are linked in the Launch box / Big box metadata fields.

The app was written quickly and not efficiently, but is definitely better than downloading videos yourself 1 by 1. Definitely using the "Fail Fast" method of programming.

The app then places the download into the correct folder and trims the video down to either a 1-min segment or a 30-second segment based on the video length

The following packages are needed for the python script to work. Some of these you may already have on your system

  - pip install xml
  - pip install pytube
  - pip install moviepy
  - pip install tkinter 
  - pip install subprocess
  - pip install re
  - FFmpeg downloaded to your machine (placed in the same directory as the python script, or choose the location manually) 
 
 
  How it works: 
  
  Application works by going to your Launch box directory and extracting the following file: 
  - ~/Launchbox/Metadata/Metadata.xml
  
Within this file there is a huge database of games that contains lots of information. What we are interested in is the following 2 items:
- Game Title
- VideoURL

[in the code, this is the get_mastergame_list() function]

we can then compare the above list to a list of games that we have installed in the following directory:
  - ~/LaunchBox/Data/Platforms/[Insert Platform].xml
 
 Any games that do not have a VideoURL [or mismatched ones] get added to a brokenlinks[] list.
 
 [in the code, this is the  match_master_to_games() function] 
 

Note: As I could not find any fields that linked the two files correctly (foreign key) I ended up matching the fields on the YouTube link itself when comparing the two lists. [if someone knows a better way, please add it in!]

Finally, i attempt to download the videos from YouTube using pytube into the correct folders. If the download is successful, i will rename the file to the title of the game and check the video length.  

- If it is longer than 60 seconds but less than 5 mins (300 seconds), I will trim the video down to a 30-second clip starting at the 29-second mark.  

- If it is longer than 5 mins (300 seconds), I will trim the video down to a 60-second clip starting at the 4-min  mark.  

In my brief testing, this seemed to work for most games as it skipped the intro to most videos (logos, channel shout-outs etc.) and the gameplay already began

the shorter videos are usually jammed packed full of content regardless. 

Notes & To-Dos: 
- Change the quality of the videos downloaded by setting the value "quality" to 1 or 0. (0  = Low Quality, 1 = High Quality)
- Might have a stab at manually searching YouTube videos and downloading them for games that have no VideoURL link. currently, the titles of these games are saved in the brokenlinks[] list. A better foreign key will be needed for this to work 100%
- I did not use Moviepy to trim the videos as the first 5 seconds of the video kept getting corrupted/glitched 
- I'm sure there are some very easy and simple ways to make this code more efficient. My day job is not programming and this was a easy/hacky solution for me to use personally. That said, I'm open to all your additions and changes! (but bear with me as this is my first time using my GitHub account) 
- USE THIS AT YOUR OWN RISK: Program downloads, renames, deletes & trims videos. Though this works well on my system, i have not tested it on any other machine. (currently running Windows 10, python version 3.10.0, launchbox version 12.11).
