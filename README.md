# raspi_customizable_streamdeck
A Raspberry pi project that allows you to make a custom UI in the Raspberry pi platform, which allows you to automate virtually anything and make custom tools to fit your needs.

Requirements:

A Raspberry Pi (i used a Raspi 4, but most version should work)
A 1024x600p screen (not necessary)
Pi Os Full
basic Raspi things, like a power supply and micro sd card
python installed (preferably python3, use "sudo apt-get install python3" to get python3 on the pi, and follow microsoft's instructions to install it on windows)

How to setup:

Dowload the folder "raspi_custom_streamdeck". Open the file called "screen.py".
Change the usernam to your pi's username, save the file and close.
Go to the folder "pc" and open the file "pc_receive", change the ip to your pi's ip. 
Go to the file explorer and find the chrome.exe file, drag it into the cmd propmt and copy the path. Paste the path onto the "pc_recive" file.
Download all the musics/songs you want as a mp3, and put them in the albun_1 folder.

Open the notepad and write the name of all the songs, followed by: question mark, author, question mark, album, it should look something like this:
(file name)?(song name)?(author)?(album)
dontstopmenow.mp3?Don't Stop Me Now?Queen?Jazz

Save it as info.csv in the files folder (make sure that its info.csv not info.csv.txt or anything other than info.csv).

Put the files inside the raspi folder in your raspi's Desktop (if you want to save it elsewhere, you'll have to modify the code).

If you're using a screen follow the next steps, if not skip them:
Go to the pi's file explorer, click on "edit" then "preferences" then on "open files with a single click". Close the explorer.
Go to the "screen.py" file, right click it and select "open with", select "open with" once again, and then click on "custom command line".
On the "comand line to execute" box, write: "sudo /usr/bin/python %f", write "Sudo Python" on the Application Name and check the box "set selected application as default action for tis file type", click on "ok"

Click on the Raspberry pi icon, select "preferences", then "Screen Configuration", right click, select "resolution", set it to 1024x600 (or the closest option) (if you want to use a different resolution, you'll have to modify the code)

If you have any problem with the libraries, just go to the terminal (cmd for windows) and write "pip install" followed by the library name (pip3 for python3)

It should be up and running now!

Note: this project was made in portuguese, so here is the abreviations used, full words and translation to english (part of the code is also in portuguse, put the words in google translator and it will tell you their meaning, or just figure it out yourself :) ):

(abreviation) - (full word) = (translation)/(other info)
Desliga - Desliga = turn off/turn off the pi
Energia - Energia = Power/menu to calculate watts, amps or volts
Calcula - Calculadora = Calculator
Resiste - Resistencia = Resistor/menu to calculate the ohms for a resistor
Conve - Converter = Convert/convert various units
Musica - Musica = Music/play songs
Fechar - Fechar = Close
Sair - Sair = Close/close the menus
Calcular - Calcular = Calculate/efectuates the calculations
Nome - Nome = Name/name of the song
Autor - Autor = author of the song
Album - Album = song's album
V Inicio = starting volts
V Fim = ending volts
