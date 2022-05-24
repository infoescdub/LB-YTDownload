# LB-YTDownload
Launchbox / BigBox Youtube Video Downloader 

This is a simple Python application i made that will download youtube videos that are linked in the Launch box / Big box meta data fields.

App was written quickly and not effiecntly, but is definitly better than downloading videos yourself 1 by 1. definitly using the "Fail Fast" method of programming.

the app then places the download into the correct folder and trims the video down to either a 1 min segment or a 30 second segment based on the video length

The following packages are needed for the pyhton script to work. Some of these you may already have on your system

  - pip install xml
  - pip install pytube
  - pip install moviepy
  - pip install tkinter 
  - pip install subporcess
  - pip install re
 
 
  How it works: 
  
  Application works by going to your Luanch box directory and extracting the following file: 
  - ~/Launchbox/Metadata/Metadata.xml
  
Within this file there is a huge database of games that contains lots of information. what we are interested in is the following 2 items:
- Game Title
- VideoURL

[in the code, this is the get_mastergame_list() function]

we can then compare the above list to a list of games that we have installed in the following directory:
  - ~/LaunchBox/Data/Platforms/[Insert Platform].xml
 
 Any games that do not have a VideoURL [or mismatched ones] get added to a brokenlinks[] list.
 
 [in the code, this is the  match_master_to_games() function] 
 

Note: As i could not find any fields that linked the two files correctly (foreign key) i ended up matching the fileds on the Youtube link itself when comparing the two lists. [if someone knows a better way, please add it in!]

Finally, i attempt to download the videos from YouTube using pytube into the correct folders. if the download is successful, i will rename the file to the title of the game and check the video length.  

- If it is longer than 60 seconds but less than 5 mins (300 seconds), i will trim the video down to a 30 second clip starting at the 29 second mark.  

- If it is longer than 5 mins (300 seconds), I will trim the video down to a 60 second clip starting at the 4 min  mark.  

in my brief testing, this seemed to work for most games as it skipped the intro to most videos (logos, channel shoutouts etc.) and the gameplay already began

the shorter vdieos are usually jammed packed full of content regardless. 

Notes & To-Dos: 
- Change the quality of the videos downloaded by setting the value "quality" to 1 or 0. (0  = Low Qulaity, 1 = High Qulaity)
- Might have a stab at manually searching youtube videos and downlaoding them for games that have no VideoURL link. currently the titles of these games are saved in the brokenlinks[] list. A better forign key will be needed for this to work 100%
- Im sure there are some very easy and simple ways to make this code more efficent. My day job is not programming and this was a easy/hacky solution for me to use personally. That said im open to all your additions and changes! (but bare with me as this is my first time using my github account) 


  
