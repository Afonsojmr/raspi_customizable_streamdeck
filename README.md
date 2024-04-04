# raspi_customizable_streamdeck
A Raspberry pi project that allows you to make a custom UI in the Raspberry pi platform, which allows you to automate virtually anything and make custom tools to fit your needs.

Requirements:

A Raspberry Pi (i used a Raspi 4, but most version should work);
 A 1024x600p screen (not necessary);
 Pi Os Full;
 Basic Raspi things, like a power supply and micro sd card;
 Python installed (preferably python3, use "sudo apt-get install python3" to get python3 on the pi, and follow microsoft's instructions to install it on windows);

How to setup:

Dowload the folder "raspi_custom_streamdeck". Open the file called "screen.py".
Change the usernam to your pi's username, save the file and close.
Go to the folder "pc" and open the file "pc_receive", change the ip to your pi's ip. 
Go to the file explorer and find the chrome.exe file, drag it into the cmd propmt and copy the path. Paste the path onto the "pc_recive" file.
Download all the musics/songs you want as a mp3, and put them in the albun_1 folder.

Open the notepad and write the name of all the songs, followed by: question mark, author, question mark, album, it should look something like this:
(file name)?(song name)?(author)?(album) - 
dontstopmenow.mp3?Don't Stop Me Now?Queen?Jazz

Save it as info.csv in the files folder (make sure that its info.csv not info.csv.txt or anything other than info.csv).

Put the files inside the raspi folder in your raspi's Desktop (if you want to save it elsewhere, you'll have to modify the code).

If you're using a screen follow the next steps, if not skip them:
Go to the pi's file explorer, click on "edit" then "preferences" then on "open files with a single click". Close the explorer.
Go to the "screen.py" file, right click it and select "open with", select "open with" once again, and then click on "custom command line".
On the "comand line to execute" box, write: "sudo /usr/bin/python %f", write "Sudo Python" on the Application Name and check the box "set selected application as default action for tis file type", click on "ok"

Click on the Raspberry pi icon, select "preferences", then "Screen Configuration", right click, select "resolution", set it to 1024x600 (or the closest option) (if you want to use a different resolution, you'll have to modify the code)

Open the notepad and write "python " then open file explorer and drag your "pc_receive" file onto cmd, paste the path to notepad and save as "connect.bat" (you can choose any name as long as it is a .bat file, so "code.bat" would work, but "code.bat.txt" wouldnt, since its a txt(text) file, not a .bat file).

To control your shelly module just open the "screen.py" file and put your shelly's ip and set "shelly_on" to True. (Note: i used a shelly plug s, compatibility with other shelly modules is not verified).

If you have any problem with the libraries, just go to the terminal (cmd for windows) and write "pip install" followed by the library name (pip3 for python3)

It should be up and running now! Execute the "screen.py" file/code on the pi, by clicking on it or on the terminal. To connect to the pc, just click on "conect" and execute the .bat file on your pc.

Note: this project was made in portuguese, so if there's any word you don't understand, just put it on google translator.
