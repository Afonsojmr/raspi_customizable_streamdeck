import pygame
import RPi.GPIO as GPIO
import socket
from subprocess import call
import os
from timeit import default_timer as timer
import urllib.request
from time import strftime

last_time = timer()

username = 'add your pi's username here'
shelly_on = False #set this to True to be able of controlling the shelly module
shelly_ip = 'add you shelly ip here'

luz = 2

pressed = [0,0,0]

GPIO.setmode(GPIO.BCM)
GPIO.setup(luz, GPIO.OUT)
GPIO.output(luz, GPIO.LOW)

connected = False

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)
screen = pygame.display.set_mode((1024, 600), pygame.FULLSCREEN)

album_1 = [f for f in os.listdir('/home/' + username + '/Desktop/files/album_1')]
music = 0
paused = False
playing = False
converter = False
resistor = False
energy = False
calculator = False
music_ = False
shelly_state = 0

pos_x = [30, 30, 30, 30, 30, 30, 30, 150, 150, 150, 150, 150, 150, 150]
pos_y = [40, 90, 140, 190, 240, 290, 340, 40, 90, 140, 190, 240, 290,340]

pos_x_out = [270, 270, 270, 270, 270, 270, 270, 390, 390, 390, 390, 390, 390, 390]
pos_y_out = [40, 90, 140, 190, 240, 290, 340, 40, 90, 140, 190, 240, 290, 340]

SI = {'mm': 0.001,'cm': 0.01,'dm': 0.1, 'm': 1.0,'hm': 100.0,'dam': 10.0, 'km': 1000.0, 'mi': 1600, 'y': 0.914, 'ft': 0.3, 'in': 0.025, 'kg': 1000,'g': 1, 'lb': 450}

font = pygame.font.SysFont(None, 70)

def Draw(text, x, y):
    img = font.render(text, True, (255,255,255))
    screen.blit(img,(x,y))

def Actions(input):
    global pressed
    global paused
    global music
    global album_1
    global connected
    global clientsocket
    global shelly_state

    if input == 1 and connected == False:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 5000))
        s.listen(5)
        clientsocket, address = s.accept()
        print("connected")
        connected = True
            
    elif input == 4:
        if pressed[2] == 0:
            GPIO.output(luz, GPIO.HIGH)
            pressed[2] = 1
            print('ligou 3')
        else:
            GPIO.output(luz, GPIO.LOW)
            pressed[2] = 0
            print('desligou 3')
    
    if connected == True:
        try: 
            if input == 5:
                clientsocket.send(bytes('/', "utf-8"))
            elif input == 6:
                clientsocket.send(bytes('8', "utf-8"))
            elif input == 7:
                clientsocket.send(bytes('5', "utf-8"))
            elif input == 8:
                clientsocket.send(bytes('2', "utf-8"))
            elif input == 9:
                clientsocket.send(bytes('.', "utf-8"))
            elif input == 10:
                clientsocket.send(bytes('0', "utf-8"))
            elif input == 13:
                clientsocket.send(bytes('1', "utf-8"))
        except ValueError:
            print('erro')
    
    elif input == 15:
        call("sudo shutdown -h now", shell=True)

    if input == 16:
        if paused == False:
            pygame.mixer.music.load('/home/' + username + '/Desktop/files/album_1/' + album_1[music])
            pygame.mixer.music.play()
        elif paused == True:
            pygame.mixer.music.unpause()
            
    elif input == 17:
        if music == int(len(album_1) - 1):
            music = 0
            paused = False
        else:
            music = music + 1
            paused = False
        
        if paused == False:
            pygame.mixer.music.load('/home/' + username + '/Desktop/files/album_1/' + album_1[music])
            pygame.mixer.music.play()

    elif input == 18:
        if music == 0:
            music = int(len(album_1) - 1)
            paused = False
        else:
            music = music - 1
            paused = False

        if paused == False:
            pygame.mixer.music.load('/home/' + username + '/Desktop/files/album_1/' + album_1[music])
            pygame.mixer.music.play()

    elif input == 19:
        if shelly_state == 0 and shelly_on:
            urllib.request.urlopen('http://' + shelly_ip + '/relay/0?turn=on')
            shelly_state = 1
        elif shelly_state == 1 and shelly_on:
            urllib.request.urlopen('http://' + shelly_ip + '/relay/0?turn=off')
            shelly_state = 0

raw = pygame.image.load('/home/' + username + '/Desktop/files/bg_buttons.png').convert()
image = pygame.transform.scale(raw, (180,100))

raw1 = pygame.image.load('/home/' + username + '/Desktop/files/triangle.png').convert()
triangle = pygame.transform.scale(raw1, (180,100))
raw2 = pygame.image.load('/home/' + username + '/Desktop/files/pause_button.png').convert()
resume_pause = pygame.transform.scale(raw2, (300,200))
previous = pygame.transform.rotate(triangle, -90)
next = pygame.transform.rotate(triangle, 90)
        
while True:    
    screen.fill((0,0,0))
    
    time_now = timer()

    unit_in_pos = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    unit_out_pos = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    unit_in = ''
    unit_out = ''
    val = ''

    weight_1 = False 
    weight_2 = False

    volts_in = ''
    volts_out = ''
    amps = ''

    v_in = True
    v_out = False
    amps_ = False
    
    mode = [0,0,0]
    text= ['', '', '']

    equation = ''
    solution = 0

    Connect = screen.blit(image, (0,0)) 

    if connected == False:
        img = font.render('Conect', True, (0,0,0))
        screen.blit(img,(5,30))
    elif connected == True:
        Draw('Conect', 5,30)
    
    Twitch = screen.blit(image, (210,0))
    Draw('Twitch', 225,30)
    
    Whatsapp = screen.blit(image, (420,0))
    Draw('Whats', 440,30)

    Youtube = screen.blit(image, (630,0))
    Draw('Yout', 665,30)

    Chrome = screen.blit(image, (840,0))
    Draw('Chrome', 838,30)

    Warthunder = screen.blit(image, (0,120))
    Draw('WT', 50,150)
    
    Task_manager = screen.blit(image, (210,120))
    Draw('TaskM', 225,150)

    Shutdown = screen.blit(image, (420, 120))
    Draw('Desliga', 425,150)

    Shutdown_full = screen.blit(image, (630,120))
    Draw('Desl Pc ', 630,150)

    Lights = screen.blit(image, (840,120))
    Draw('Luz', 880,150)

    Music = screen.blit(image, (0, 240))
    Draw('Musica', 5,270)

    Energy = screen.blit(image, (210,240))
    Draw('Energia', 210,270)

    Calculator = screen.blit(image, (420,240))
    Draw('Calcula', 420,270)

    Resistance = screen.blit(image, (630,240))
    Draw('Resiste', 635,270)

    Converter = screen.blit(image, (840,240))
    Draw('Conve', 855,270)

    font_2 = pygame.font.SysFont(None, 60)
    img = font_2.render(strftime("%d-%m-%y %I:%M%p"), True, (255,255,255))
    Fechar = screen.blit(img,(670, 530))

    font_2 = pygame.font.SysFont(None, 60)
    img = font_2.render('Fechar', True, (255,255,255))
    Fechar = screen.blit(img,(0, 530))

    time_elapsed = time_now - last_time
    if time_elapsed > 60:
        last_time = time_now
        if connected:
            try:
                clientsocket.send(bytes('123', "utf-8"))
            except ValueError:
                print('erro')
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            if Connect.collidepoint(event.pos):
                Actions(1)
            elif Task_manager.collidepoint(event.pos):
                Actions(5)
            elif Chrome.collidepoint(event.pos):
                Actions(6)
            elif Warthunder.collidepoint(event.pos):
                Actions(7)
            elif Twitch.collidepoint(event.pos):
                Actions(8)
            elif Youtube.collidepoint(event.pos):
                Actions(9)
            elif Whatsapp.collidepoint(event.pos):
                Actions(10)
            elif Shutdown_full.collidepoint(event.pos):
                Actions(13)
            elif Shutdown.collidepoint(event.pos):
                Actions(15)
            elif Lights.collidepoint(event.pos):
                Actions(19)

            if Converter.collidepoint(event.pos):
                converter = True
            if Resistance.collidepoint(event.pos):
                resistor = True
            if Energy.collidepoint(event.pos):
                energy = True
            if Calculator.collidepoint(event.pos):
                calculator = True
            if Music.collidepoint(event.pos):
                music_ = True

            if Fechar.collidepoint(event.pos):
                pygame.quit()

    while music_:
        screen.fill((0,0,0))

        raw_2 = pygame.image.load('/home/' + username + '/Desktop/files/bg_buttons.png').convert()

        font_2 = pygame.font.SysFont(None, 60)

        img = font_2.render('Fechar', True, (255,255,255))
        Fechar = screen.blit(img,(870, 530))

        img = font_2.render('Sair', True, (255,255,255))
        Close = screen.blit(img,(0, 530))      

        img = font_2.render('Nome:', True, (255,255,255))
        screen.blit(img,(60, 20))  

        img = font_2.render('Autor:', True, (255,255,255))
        screen.blit(img,(60, 140))  

        img = font_2.render('Album:', True, (255,255,255))
        screen.blit(img,(60, 260))  

        Pause_resume = screen.blit(resume_pause, (385, 365))
        Next = screen.blit(previous, (700, 375))
        Previous = screen.blit(next, (250, 375))

        playing = True

        time_now = timer()
        time_elapsed = time_now - last_time
        if time_elapsed > 60:
            last_time = time_now
            if connected:
                try:
                    clientsocket.send(bytes('123', "utf-8"))
                except ValueError:
                    print('erro')

        with open("/home/" + username + "/Desktop/files/info.csv") as log:
            data = log.readlines()
            for i in range(0, len(data)):
                if str(data[i].split('?')[0]) == album_1[music]:
                    img = font_2.render(str(data[i].split('?')[1]), True, (255,255,255))
                    screen.blit(img,(60, 80))  
                    img = font_2.render(str(data[i].split('?')[2]), True, (255,255,255))
                    screen.blit(img,(60, 200))  
                    img = font_2.render(str(data[i].split('?')[3])[:-1], True, (255,255,255))
                    screen.blit(img,(60, 320))  
                    break


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if Close.collidepoint(event.pos):
                    music_ = False
                    pygame.mixer.music.pause()
                    paused = True
                    playing = False
                    break
                if Fechar.collidepoint(event.pos):
                    pygame.quit()

                elif Pause_resume.collidepoint(event.pos):
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                        paused = True
                        playing = False
                        break
                    else:
                        Actions(16)
                        
                elif Next.collidepoint(event.pos):
                    Actions(17)
                elif Previous.collidepoint(event.pos):
                    Actions(18)


        pygame.display.update()

    while calculator:
        screen.fill((0,0,0))

        raw_2 = pygame.image.load('/home/' + username + '/Desktop/files/bg_buttons.png').convert()

        font_2 = pygame.font.SysFont(None, 60)

        img = font_2.render('Fechar', True, (255,255,255))
        Fechar = screen.blit(img,(870, 530))

        img = font_2.render('Sair', True, (255,255,255))
        Close = screen.blit(img,(0, 530))

        #keys

        font_3 = pygame.font.SysFont(None, 130)

        img = font_3.render('1', True, (255,255,255))
        key_1 = pygame.draw.rect(screen,(0),pygame.Rect(700,30,70,80))
        screen.blit(img,(700, 30))

        img = font_3.render('2', True, (255,255,255))
        key_2 = pygame.draw.rect(screen,(0),pygame.Rect(780,30,70,80))
        screen.blit(img,(780, 30))

        img = font_3.render('3', True, (255,255,255))
        key_3 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(860,30,70,80))
        screen.blit(img,(860, 30))

        img = font_3.render('4', True, (255,255,255))
        key_4 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(700,130,70,80))
        screen.blit(img,(700, 130))

        img = font_3.render('5', True, (255,255,255))
        key_5 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(780,130,70,80))
        screen.blit(img,(780, 130))

        img = font_3.render('6', True, (255,255,255))
        key_6 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(860,130,70,80))
        screen.blit(img,(860, 130))

        img = font_3.render('7', True, (255,255,255))
        key_7 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(700,230,70,80))
        screen.blit(img,(700, 230))

        img = font_3.render('8', True, (255,255,255))
        key_8 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(780,230,70,80))
        screen.blit(img,(780, 230))

        img = font_3.render('9', True, (255,255,255))
        key_9 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(860,230,70,80))
        screen.blit(img,(860, 230))

        img = font_3.render('0', True, (255,255,255))
        key_10 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(700,330,70,80))
        screen.blit(img,(700, 330))

        img = font_3.render('.', True, (255,255,255))
        key_11 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(780,330,70,80))
        screen.blit(img,(780, 330))

        img = font_3.render('-', True, (255,255,255))
        key_12 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(860,330,70,80))
        screen.blit(img,(860, 330))
        
        img = font_3.render('+', True, (255,255,255))
        key_13 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(620,30,70,80))
        screen.blit(img,(620, 30))
        
        img = font_3.render('-', True, (255,255,255))
        key_14 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(620,130,70,80))
        screen.blit(img,(620, 130))

        img = font_3.render('*', True, (255,255,255))
        key_15 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(620,230,70,80))
        screen.blit(img,(620, 245))

        img = font_3.render('/', True, (255,255,255))
        key_16 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(620,330,70,80))
        screen.blit(img,(620, 330))

        img = font_3.render('= ', True, (255,255,255))
        key_17 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(620,430,70,80))
        screen.blit(img,(620, 430))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if Close.collidepoint(event.pos):
                    calculator = False
                if Fechar.collidepoint(event.pos):
                    pygame.quit()

                if key_1.collidepoint(event.pos):
                    equation = equation + '1'
                if key_2.collidepoint(event.pos):
                    equation = equation + '2'
                if key_3.collidepoint(event.pos):
                    equation = equation + '3'
                if key_4.collidepoint(event.pos):
                    equation = equation + '4'
                if key_5.collidepoint(event.pos):
                    equation = equation + '5'
                if key_6.collidepoint(event.pos):
                    equation = equation + '6'
                if key_7.collidepoint(event.pos):
                    equation = equation + '7'
                if key_8.collidepoint(event.pos):
                    equation = equation + '8'
                if key_9.collidepoint(event.pos):
                    equation = equation + '9'
                if key_10.collidepoint(event.pos):
                    equation = equation + '0'
                if key_11.collidepoint(event.pos):
                    equation = equation + '.'
                if key_12.collidepoint(event.pos):
                    equation = equation[:-1]
                if key_13.collidepoint(event.pos):
                    equation = equation + '+'
                if key_14.collidepoint(event.pos):
                    equation = equation + '-'
                if key_15.collidepoint(event.pos):
                    equation = equation + '*'
                if key_16.collidepoint(event.pos):
                    equation = equation + '/'
                if key_17.collidepoint(event.pos):
                    if equation != '' and equation[-2] != equation[-1] and equation[-1] != '+' and equation[-1] != '-' and equation[-1] != '*' and equation[-1] != '/':
                        solution = round(eval(equation), 5)

        Draw(equation, 100,50) 
        Draw('= ' + str(solution), 110,125) 
        
        pygame.display.update()

    while energy:
        screen.fill((0,0,0))

        raw_2 = pygame.image.load('/home/' + username + '/Desktop/files/bg_buttons.png').convert()

        font_2 = pygame.font.SysFont(None, 60)

        img = font_2.render('Fechar', True, (255,255,255))
        Fechar = screen.blit(img,(870, 530))

        img = font_2.render('Sair', True, (255,255,255))
        Close = screen.blit(img,(0, 530))

        #keys

        font_3 = pygame.font.SysFont(None, 130)

        img = font_3.render('1', True, (255,255,255))
        key_1 = pygame.draw.rect(screen,(0),pygame.Rect(800,30,70,80))
        screen.blit(img,(800, 30))

        img = font_3.render('2', True, (255,255,255))
        key_2 = pygame.draw.rect(screen,(0),pygame.Rect(880,30,70,80))
        screen.blit(img,(880, 30))

        img = font_3.render('3', True, (255,255,255))
        key_3 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(960,30,70,80))
        screen.blit(img,(960, 30))

        img = font_3.render('4', True, (255,255,255))
        key_4 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(800,130,70,80))
        screen.blit(img,(800, 130))

        img = font_3.render('5', True, (255,255,255))
        key_5 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(880,130,70,80))
        screen.blit(img,(880, 130))

        img = font_3.render('6', True, (255,255,255))
        key_6 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(960,130,70,80))
        screen.blit(img,(960, 130))

        img = font_3.render('7', True, (255,255,255))
        key_7 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(800,230,70,80))
        screen.blit(img,(800, 230))

        img = font_3.render('8', True, (255,255,255))
        key_8 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(880,230,70,80))
        screen.blit(img,(880, 230))

        img = font_3.render('9', True, (255,255,255))
        key_9 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(960,230,70,80))
        screen.blit(img,(960, 230))

        img = font_3.render('0', True, (255,255,255))
        key_10 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(800,330,70,80))
        screen.blit(img,(800, 330))

        img = font_3.render('.', True, (255,255,255))
        key_11 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(880,330,70,80))
        screen.blit(img,(880, 330))

        img = font_3.render('-', True, (255,255,255))
        key_12 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(960,330,70,80))
        screen.blit(img,(960, 330))

        if mode[0] == 1:
            screen.blit(pygame.transform.scale(raw_2, (125,50)),(40,120))
        elif mode[1] == 1:
            screen.blit(pygame.transform.scale(raw_2, (145,50)),(390,125))
        elif mode[2] == 1:
            screen.blit(pygame.transform.scale(raw_2, (145,50)),(40,40))

        img = font_2.render('Watts: ', True, (255,255,255))
        Watts = screen.blit(img,(50, 50))

        img = font_2.render('Volts: ', True, (255,255,255))
        Volts = screen.blit(img,(50, 125))

        img = font_2.render('Amps: ', True, (255,255,255))
        Amps = screen.blit(img,(400, 125))

        raw_5 = pygame.image.load('/home/' + username + '/Desktop/files/bg_buttons.png').convert()
        screen.blit(pygame.transform.scale(raw_5, (175,50)),(45,245))
        img = font_2.render('Calcular', True, (255,255,255))
        Calculate = screen.blit(img,(50, 250))

        Draw(text[0], 175,125) 
        Draw(text[1], 550,125) 
        Draw(text[2], 190,50) 

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if Close.collidepoint(event.pos):
                    energy = False
                if Fechar.collidepoint(event.pos):
                    pygame.quit()

                if Calculate.collidepoint(event.pos):
                    if text[0] != '' and text[1] != '':
                        try:
                            text[2] = str(round(float(text[0]) * float(text[1]), 2))
                        except ValueError:
                            print('erro')
                    elif text[1] != '' and text[2] != '':
                        try:
                            text[0] = str(round(float(text[2]) / float(text[1]), 2))
                        except ValueError:
                            print('erro')
                    elif text[0] != '' and text[2] != '':
                        try:
                            text[1] = str(round(float(text[2]) / float(text[0]), 2))
                        except ValueError:
                            print('erro')

                if Volts.collidepoint(event.pos):
                    for i in range(0, len(mode)):
                        mode[i] = 0
                    mode[0] = 1
                if Amps.collidepoint(event.pos):
                    for i in range(0, len(mode)):
                        mode[i] = 0
                    mode[1] = 1
                if Watts.collidepoint(event.pos):
                    for i in range(0, len(mode)):
                        mode[i] = 0
                    mode[2] = 1


                for i in range(0, len(mode)):
                    if mode[i] == 1:
                        write = i
                        break

                if key_1.collidepoint(event.pos):
                    text[write] = text[write] + '1'
                if key_2.collidepoint(event.pos):
                    text[write] = text[write] + '2'
                if key_3.collidepoint(event.pos):
                    text[write] = text[write] + '3'
                if key_4.collidepoint(event.pos):
                    text[write] = text[write] + '4'
                if key_5.collidepoint(event.pos):
                    text[write] = text[write] + '5'
                if key_6.collidepoint(event.pos):
                    text[write] = text[write] + '6'
                if key_7.collidepoint(event.pos):
                    text[write] = text[write] + '7'
                if key_8.collidepoint(event.pos):
                    text[write] = text[write] + '8'
                if key_9.collidepoint(event.pos):
                    text[write] = text[write] + '9'
                if key_10.collidepoint(event.pos):
                    text[write] = text[write] + '0'
                if key_11.collidepoint(event.pos):
                    text[write] = text[write] + '.'
                if key_12.collidepoint(event.pos):
                    text[write] = text[write][:-1]

        pygame.display.update()

    while resistor:
        screen.fill((0,0,0))

        raw_2 = pygame.image.load('/home/' + username + '/Desktop/files/bg_buttons.png').convert()

        font_2 = pygame.font.SysFont(None, 60)

        img = font_2.render('Fechar', True, (255,255,255))
        Fechar = screen.blit(img,(870, 530))

        img = font_2.render('Sair', True, (255,255,255))
        Close = screen.blit(img,(0, 530))

        if v_in:
            screen.blit(pygame.transform.scale(raw_2, (180,60)),(40,40))
        if v_out:
            screen.blit(pygame.transform.scale(raw_2, (140,60)),(40,115))
        if amps_:
            screen.blit(pygame.transform.scale(raw_2, (140,60)),(40,190))

        img = font_2.render('V Inicio: ', True, (255,255,255))
        Vin = screen.blit(img,(50, 50))

        img = font_2.render('V Fim: ', True, (255,255,255))
        Vout = screen.blit(img,(50, 125))

        img = font_2.render('Amps: ', True, (255,255,255))
        Amps = screen.blit(img,(50, 200))
        #keys

        font_3 = pygame.font.SysFont(None, 130)

        img = font_3.render('1', True, (255,255,255))
        key_1 = pygame.draw.rect(screen,(0),pygame.Rect(600,30,70,80))
        screen.blit(img,(600, 30))

        img = font_3.render('2', True, (255,255,255))
        key_2 = pygame.draw.rect(screen,(0),pygame.Rect(680,30,70,80))
        screen.blit(img,(680, 30))

        img = font_3.render('3', True, (255,255,255))
        key_3 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(760,30,70,80))
        screen.blit(img,(760, 30))

        img = font_3.render('4', True, (255,255,255))
        key_4 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(600,130,70,80))
        screen.blit(img,(600, 130))

        img = font_3.render('5', True, (255,255,255))
        key_5 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(680,130,70,80))
        screen.blit(img,(680, 130))

        img = font_3.render('6', True, (255,255,255))
        key_6 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(760,130,70,80))
        screen.blit(img,(760, 130))

        img = font_3.render('7', True, (255,255,255))
        key_7 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(600,230,70,80))
        screen.blit(img,(600, 230))

        img = font_3.render('8', True, (255,255,255))
        key_8 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(680,230,70,80))
        screen.blit(img,(680, 230))

        img = font_3.render('9', True, (255,255,255))
        key_9 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(760,230,70,80))
        screen.blit(img,(760, 230))

        img = font_3.render('0', True, (255,255,255))
        key_10 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(600,330,70,80))
        screen.blit(img,(600, 330))

        img = font_3.render('.', True, (255,255,255))
        key_11 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(680,330,70,80))
        screen.blit(img,(680, 330))

        img = font_3.render('-', True, (255,255,255))
        key_12 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(760,330,70,80))
        screen.blit(img,(760, 330))

        img = font_3.render('-------->', True, (255,255,255))
        img = pygame.transform.rotate(img, -90)
        key_13 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(840,40,70,350))
        screen.blit(img,(840, 60))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if Close.collidepoint(event.pos):
                    resistor = False
                if Fechar.collidepoint(event.pos):
                    pygame.quit()
                
                if Vin.collidepoint(event.pos):
                    if v_in == False:
                        volts_in = ''
                    v_in = True
                    v_out = False
                    amps_ = False
                if Vout.collidepoint(event.pos):
                    if v_out == False:
                        volts_out = ''
                    v_in = False
                    v_out = True
                    amps_ = False
                if Amps.collidepoint(event.pos):
                    if amps_ == False:
                        amps = ''
                    v_in = False
                    v_out = False
                    amps_ = True

                if key_13.collidepoint(event.pos):
                    if v_in:
                        if v_out == False:
                            volts_out = ''
                        v_in = False
                        v_out = True
                        amps_ = False
                    elif v_out:
                        if amps_ == False:
                            amps = ''
                        v_in = False
                        v_out = False
                        amps_ = True
                    elif amps_:
                        if v_in == False:
                            volts_in = ''
                        v_in = True
                        v_out = False
                        amps_ = False

                if v_in:
                    if key_1.collidepoint(event.pos):
                        volts_in = volts_in + '1'
                    if key_2.collidepoint(event.pos):
                        volts_in = volts_in + '2'
                    if key_3.collidepoint(event.pos):
                        volts_in = volts_in + '3'
                    if key_4.collidepoint(event.pos):
                        volts_in = volts_in + '4'
                    if key_5.collidepoint(event.pos):
                        volts_in = volts_in + '5'
                    if key_6.collidepoint(event.pos):
                        volts_in = volts_in + '6'
                    if key_7.collidepoint(event.pos):
                        volts_in = volts_in + '7'
                    if key_8.collidepoint(event.pos):
                        volts_in = volts_in + '8'
                    if key_9.collidepoint(event.pos):
                        volts_in = volts_in + '9'
                    if key_10.collidepoint(event.pos):
                        volts_in = volts_in + '0'
                    if key_11.collidepoint(event.pos):
                        volts_in = volts_in + '.'
                    if key_12.collidepoint(event.pos):
                        volts_in = volts_in[:-1]
                elif v_out:
                    if key_1.collidepoint(event.pos):
                        volts_out = volts_out + '1'
                    if key_2.collidepoint(event.pos):
                        volts_out = volts_out + '2'
                    if key_3.collidepoint(event.pos):
                        volts_out = volts_out + '3'
                    if key_4.collidepoint(event.pos):
                        volts_out = volts_out + '4'
                    if key_5.collidepoint(event.pos):
                        volts_out = volts_out + '5'
                    if key_6.collidepoint(event.pos):
                        volts_out = volts_out + '6'
                    if key_7.collidepoint(event.pos):
                        volts_out = volts_out + '7'
                    if key_8.collidepoint(event.pos):
                        volts_out = volts_out + '8'
                    if key_9.collidepoint(event.pos):
                        volts_out = volts_out + '9'
                    if key_10.collidepoint(event.pos):
                        volts_out = volts_out + '0'
                    if key_11.collidepoint(event.pos):
                        volts_out = volts_out + '.'
                    if key_12.collidepoint(event.pos):
                        volts_out = volts_out[:-1]
                elif amps_:
                    if key_1.collidepoint(event.pos):
                        amps = amps + '1'
                    if key_2.collidepoint(event.pos):
                        amps = amps + '2'
                    if key_3.collidepoint(event.pos):
                        amps = amps + '3'
                    if key_4.collidepoint(event.pos):
                        amps = amps + '4'
                    if key_5.collidepoint(event.pos):
                        amps = amps + '5'
                    if key_6.collidepoint(event.pos):
                        amps = amps + '6'
                    if key_7.collidepoint(event.pos):
                        amps = amps + '7'
                    if key_8.collidepoint(event.pos):
                        amps = amps + '8'
                    if key_9.collidepoint(event.pos):
                        amps = amps + '9'
                    if key_10.collidepoint(event.pos):
                        amps = amps + '0'
                    if key_11.collidepoint(event.pos):
                        amps = amps + '.'
                    if key_12.collidepoint(event.pos):
                        amps = amps[:-1]

        if volts_in != '':
            if volts_in[0] == '.':
                volts_in = '0' + volts_in
        if volts_out != '':
            if volts_out[0] == '.':
                volts_out = '0' + volts_out
        if amps != '':
            if amps[0] == '.':
                amps = '0' + amps

        if volts_in == '':
            Draw('-', 250,50)
        else:
            Draw(volts_in, 250,50)  

        if volts_out == '':
            Draw('-', 250,125)
        else:
            Draw(volts_out, 250,125)  

        if amps == '':
            Draw('-', 250,200)
        else:
            Draw(amps, 250,200)  
        
        if volts_in != '' and volts_out != '' and amps != '' and amps != '0' and amps != '0.':
            if volts_in > volts_out:
                try:
                    result_v = round(float((float(volts_in) - float(volts_out)) / float(amps)), 1)
                    Draw(str(result_v) + ' Kohms', 50,300) 
                    Draw(str(int(result_v * 1000)) + ' ohms', 50,370) 
                except ValueError:
                    Draw('erro', 50,300)
            else: 
                Draw('erro', 50,300)
        else:
            result_v = 0 
            Draw('- Kohms', 50,300) 
            Draw('- ohms', 50,370) 

        pygame.display.update()

    while converter:
        screen.fill((0,0,0))

        font_2 = pygame.font.SysFont(None, 60)
        img = font_2.render('Sair', True, (255,255,255))
        Close = screen.blit(img,(0, 530))

        font_3 = pygame.font.SysFont(None, 130)

        raw_ = pygame.image.load('/home/' + username + '/Desktop/files/bg_buttons.png').convert()
        image_ = pygame.transform.scale(raw_, (80,40))

        Mm = pygame.draw.rect(screen,(0),pygame.Rect(pos_x[0], pos_y[0],70,40))
        Cm = pygame.draw.rect(screen,(0),pygame.Rect(pos_x[1], pos_y[1],70,40))
        Dm = pygame.draw.rect(screen,(0),pygame.Rect(pos_x[2], pos_y[2],70,40))
        M = pygame.draw.rect(screen,(0),pygame.Rect(pos_x[3], pos_y[3],70,40))
        Dam = pygame.draw.rect(screen,(0),pygame.Rect(pos_x[4], pos_y[4],90,40))
        Hm = pygame.draw.rect(screen,(0),pygame.Rect(pos_x[5], pos_y[5],70,40))
        Km = pygame.draw.rect(screen,(0),pygame.Rect(pos_x[6], pos_y[6],70,40))
        In = pygame.draw.rect(screen,(0),pygame.Rect(pos_x[7], pos_y[7],70,40))
        Ft = pygame.draw.rect(screen,(0),pygame.Rect(pos_x[8], pos_y[8],70,40))
        Y = pygame.draw.rect(screen,(0),pygame.Rect(pos_x[9], pos_y[9],70,40))
        Mi = pygame.draw.rect(screen,(0),pygame.Rect(pos_x[10], pos_y[10],70,40))
        Kg = pygame.draw.rect(screen,(0),pygame.Rect(pos_x[11], pos_y[11],70,40))
        G = pygame.draw.rect(screen,(0),pygame.Rect(pos_x[12], pos_y[12],70,40))
        Lb = pygame.draw.rect(screen,(0),pygame.Rect(pos_x[13], pos_y[13],70,40))
        #out
        Mm_out = pygame.draw.rect(screen,(0),pygame.Rect(pos_x_out[0], pos_y_out[0],70,40))
        Cm_out = pygame.draw.rect(screen,(0),pygame.Rect(pos_x_out[1], pos_y_out[1],70,40))
        Dm_out = pygame.draw.rect(screen,(0),pygame.Rect(pos_x_out[2], pos_y_out[2],70,40))
        M_out = pygame.draw.rect(screen,(0),pygame.Rect(pos_x_out[3], pos_y_out[3],70,40))
        Dam_out = pygame.draw.rect(screen,(0),pygame.Rect(pos_x_out[4], pos_y_out[4],90,40))
        Hm_out = pygame.draw.rect(screen,(0),pygame.Rect(pos_x_out[5], pos_y_out[5],70,40))
        Km_out = pygame.draw.rect(screen,(0),pygame.Rect(pos_x_out[6], pos_y_out[6],70,40))
        In_out = pygame.draw.rect(screen,(0),pygame.Rect(pos_x_out[7], pos_y_out[7],70,40))
        Ft_out = pygame.draw.rect(screen,(0),pygame.Rect(pos_x_out[8], pos_y_out[8],70,40))
        Y_out = pygame.draw.rect(screen,(0),pygame.Rect(pos_x_out[9], pos_y_out[9],70,40))
        Mi_out = pygame.draw.rect(screen,(0),pygame.Rect(pos_x_out[10], pos_y_out[10],70,40))
        Kg_out = pygame.draw.rect(screen,(0),pygame.Rect(pos_x_out[11], pos_y_out[11],70,40))
        G_out = pygame.draw.rect(screen,(0),pygame.Rect(pos_x_out[12], pos_y_out[12],70,40))
        Lb_out = pygame.draw.rect(screen,(0),pygame.Rect(pos_x_out[13], pos_y_out[13],70,40))

        for x in range(0,len(unit_in_pos)):
            if unit_in_pos[x] == 1:
                screen.blit(image_, ((pos_x[x] - 5) , pos_y[x]))
                break

        for x in range(0,len(unit_out_pos)):
            if unit_out_pos[x] == 1:
                screen.blit(image_, ((pos_x_out[x] - 5) , pos_y_out[x]))
                break
        
        img = font_2.render('mm', True, (255,255,255))
        screen.blit(img,(pos_x[0], pos_y[0]))
        img = font_2.render('cm', True, (255,255,255))
        screen.blit(img,(pos_x[1], pos_y[1]))
        img = font_2.render('dm', True, (255,255,255))
        screen.blit(img,(pos_x[2], pos_y[2]))
        img = font_2.render('m', True, (255,255,255))
        screen.blit(img,(pos_x[3], pos_y[3]))
        img = font_2.render('dam', True, (255,255,255))
        screen.blit(img,(pos_x[4], pos_y[4]))
        img = font_2.render('hm', True, (255,255,255))
        screen.blit(img,(pos_x[5], pos_y[5]))
        img = font_2.render('km', True, (255,255,255))
        screen.blit(img,(pos_x[6], pos_y[6]))
        img = font_2.render('in', True, (255,255,255))
        screen.blit(img,(pos_x[7], pos_y[7]))
        img = font_2.render('ft', True, (255,255,255))
        screen.blit(img,(pos_x[8], pos_y[8]))
        img = font_2.render('y', True, (255,255,255))
        screen.blit(img,(pos_x[9], pos_y[9]))
        img = font_2.render('mi', True, (255,255,255))
        screen.blit(img,(pos_x[10], pos_y[10]))
        img = font_2.render('kg', True, (255,255,255))
        screen.blit(img,(pos_x[11], pos_y[11]))
        img = font_2.render('g', True, (255,255,255))  
        screen.blit(img,(pos_x[12], pos_y[12]))
        img = font_2.render('lb', True, (255,255,255))
        screen.blit(img,(pos_x[13], pos_y[13]))
        
        img = font_2.render('mm', True, (255,255,255))
        screen.blit(img,(pos_x_out[0], pos_y_out[0]))
        img = font_2.render('cm', True, (255,255,255))
        screen.blit(img,(pos_x_out[1], pos_y_out[1]))
        img = font_2.render('dm', True, (255,255,255))
        screen.blit(img,(pos_x_out[2], pos_y_out[2]))
        img = font_2.render('m', True, (255,255,255))
        screen.blit(img,(pos_x_out[3], pos_y_out[3]))
        img = font_2.render('dam', True, (255,255,255))
        screen.blit(img,(pos_x_out[4], pos_y_out[4]))
        img = font_2.render('hm', True, (255,255,255))
        screen.blit(img,(pos_x_out[5], pos_y_out[5]))
        img = font_2.render('km', True, (255,255,255))
        screen.blit(img,(pos_x_out[6], pos_y_out[6]))
        img = font_2.render('in', True, (255,255,255))
        screen.blit(img,(pos_x_out[7], pos_y_out[7]))
        img = font_2.render('ft', True, (255,255,255))
        screen.blit(img,(pos_x_out[8], pos_y_out[8]))
        img = font_2.render('y', True, (255,255,255))
        screen.blit(img,(pos_x_out[9], pos_y_out[9]))
        img = font_2.render('mi', True, (255,255,255))
        screen.blit(img,(pos_x_out[10], pos_y_out[10]))
        img = font_2.render('kg', True, (255,255,255))
        screen.blit(img,(pos_x_out[11], pos_y_out[11]))
        img = font_2.render('g', True, (255,255,255))
        screen.blit(img,(pos_x_out[12], pos_y_out[12]))
        img = font_2.render('lb', True, (255,255,255))
        screen.blit(img,(pos_x_out[13], pos_y_out[13]))

        #keys

        img = font_3.render('1', True, (255,255,255))
        key_1 = pygame.draw.rect(screen,(0),pygame.Rect(600,30,70,80))
        screen.blit(img,(600, 30))

        img = font_3.render('2', True, (255,255,255))
        key_2 = pygame.draw.rect(screen,(0),pygame.Rect(680,30,70,80))
        screen.blit(img,(680, 30))

        img = font_3.render('3', True, (255,255,255))
        key_3 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(760,30,70,80))
        screen.blit(img,(760, 30))

        img = font_3.render('4', True, (255,255,255))
        key_4 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(600,130,70,80))
        screen.blit(img,(600, 130))

        img = font_3.render('5', True, (255,255,255))
        key_5 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(680,130,70,80))
        screen.blit(img,(680, 130))

        img = font_3.render('6', True, (255,255,255))
        key_6 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(760,130,70,80))
        screen.blit(img,(760, 130))

        img = font_3.render('7', True, (255,255,255))
        key_7 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(600,230,70,80))
        screen.blit(img,(600, 230))

        img = font_3.render('8', True, (255,255,255))
        key_8 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(680,230,70,80))
        screen.blit(img,(680, 230))

        img = font_3.render('9', True, (255,255,255))
        key_9 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(760,230,70,80))
        screen.blit(img,(760, 230))

        img = font_3.render('0', True, (255,255,255))
        key_10 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(600,330,70,80))
        screen.blit(img,(600, 330))

        img = font_3.render('.', True, (255,255,255))
        key_11 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(680,330,70,80))
        screen.blit(img,(680, 330))

        img = font_3.render('-', True, (255,255,255))
        key_12 = pygame.draw.rect(screen,(0,0,0),pygame.Rect(760,330,70,80))
        screen.blit(img,(760, 330))

        font_2 = pygame.font.SysFont(None, 60)
        img = font_2.render('Fechar', True, (255,255,255))
        Fechar = screen.blit(img,(870, 530))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if Close.collidepoint(event.pos):
                    converter = False
                
                if Fechar.collidepoint(event.pos):
                    pygame.quit()
                
                if weight_1 and weight_2 or weight_1 == False and weight_2 == False:
                    if key_1.collidepoint(event.pos):
                        val = val + '1'
                    if key_2.collidepoint(event.pos):
                        val = val + '2'
                    if key_3.collidepoint(event.pos):
                        val = val + '3'
                    if key_4.collidepoint(event.pos):
                        val = val + '4'
                    if key_5.collidepoint(event.pos):
                        val = val + '5'
                    if key_6.collidepoint(event.pos):
                        val = val + '6'
                    if key_7.collidepoint(event.pos):
                        val = val + '7'
                    if key_8.collidepoint(event.pos):
                        val = val + '8'
                    if key_9.collidepoint(event.pos):
                        val = val + '9'
                    if key_10.collidepoint(event.pos):
                        val = val + '0'
                    if key_11.collidepoint(event.pos):
                        val = val + '.'
                    if key_12.collidepoint(event.pos):
                        val = val[:-1]


                if Mm.collidepoint(event.pos):
                    for x in range(0,len(unit_in_pos)):
                        unit_in_pos[x] = 0
                    unit_in_pos[0] = 1
                    unit_in = 'mm'
                elif Cm.collidepoint(event.pos):
                    for x in range(0,len(unit_in_pos)):
                        unit_in_pos[x] = 0
                    unit_in_pos[1] = 1
                    unit_in = 'cm'
                elif Dm.collidepoint(event.pos):
                    for x in range(0,len(unit_in_pos)):
                        unit_in_pos[x] = 0
                    unit_in_pos[2] = 1
                    unit_in = 'dm'
                elif M.collidepoint(event.pos):
                    for x in range(0,len(unit_in_pos)):
                        unit_in_pos[x] = 0
                    unit_in_pos[3] = 1
                    unit_in = 'm'
                elif Dam.collidepoint(event.pos):
                    for x in range(0,len(unit_in_pos)):
                        unit_in_pos[x] = 0
                    unit_in_pos[4] = 1
                    unit_in = 'dam'
                elif Hm.collidepoint(event.pos):
                    for x in range(0,len(unit_in_pos)):
                        unit_in_pos[x] = 0
                    unit_in_pos[5] = 1
                    unit_in = 'hm'
                elif Km.collidepoint(event.pos):
                    for x in range(0,len(unit_in_pos)):
                        unit_in_pos[x] = 0
                    unit_in_pos[6] = 1
                    unit_in = 'km'
                elif In.collidepoint(event.pos):
                    for x in range(0,len(unit_in_pos)):
                        unit_in_pos[x] = 0
                    unit_in_pos[7] = 1
                    unit_in = 'in'
                elif Ft.collidepoint(event.pos):
                    for x in range(0,len(unit_in_pos)):
                        unit_in_pos[x] = 0
                    unit_in_pos[8] = 1
                    unit_in = 'ft'
                elif Y.collidepoint(event.pos):
                    for x in range(0,len(unit_in_pos)):
                        unit_in_pos[x] = 0
                    unit_in_pos[9] = 1
                    unit_in = 'y'
                elif Mi.collidepoint(event.pos):
                    for x in range(0,len(unit_in_pos)):
                        unit_in_pos[x] = 0
                    unit_in_pos[10] = 1
                    unit_in = 'mi'
                elif Kg.collidepoint(event.pos):
                    for x in range(0,len(unit_in_pos)):
                        unit_in_pos[x] = 0
                    unit_in_pos[11] = 1
                    unit_in = 'kg'
                elif G.collidepoint(event.pos):
                    for x in range(0,len(unit_in_pos)):
                        unit_in_pos[x] = 0
                    unit_in_pos[12] = 1
                    unit_in = 'g'
                elif Lb.collidepoint(event.pos):
                    for x in range(0,len(unit_in_pos)):
                        unit_in_pos[x] = 0
                    unit_in_pos[13] = 1
                    unit_in = 'lb'

                #out
                if Mm_out.collidepoint(event.pos):
                    for i in range(0, len(unit_out_pos)):
                        unit_out_pos[x] = 0
                    unit_out_pos[0] = 1
                    unit_out = 'mm'
                elif Cm_out.collidepoint(event.pos):
                    for i in range(0, len(unit_out_pos)):
                        unit_out_pos[x] = 0
                    unit_out_pos[1] = 1
                    unit_out = 'cm'
                elif Dm_out.collidepoint(event.pos):
                    for i in range(0, len(unit_out_pos)):
                        unit_out_pos[x] = 0
                    unit_out_pos[2] = 1
                    unit_out = 'dm'
                elif M_out.collidepoint(event.pos):
                    for i in range(0, len(unit_out_pos)):
                        unit_out_pos[x] = 0
                    unit_out_pos[3] = 1
                    unit_out = 'm'
                elif Dam_out.collidepoint(event.pos):
                    for i in range(0, len(unit_out_pos)):
                        unit_out_pos[x] = 0
                    unit_out_pos[4] = 1
                    unit_out = 'dam'
                elif Hm_out.collidepoint(event.pos):
                    for i in range(0, len(unit_out_pos)):
                        unit_out_pos[x] = 0
                    unit_out_pos[5] = 1
                    unit_out = 'hm'
                elif Km_out.collidepoint(event.pos):
                    for i in range(0, len(unit_out_pos)):
                        unit_out_pos[x] = 0
                    unit_out_pos[6] = 1
                    unit_out = 'km'
                elif In_out.collidepoint(event.pos):
                    for i in range(0, len(unit_out_pos)):
                        unit_out_pos[x] = 0
                    unit_out_pos[7] = 1
                    unit_out = 'in'
                elif Ft_out.collidepoint(event.pos):
                    for i in range(0, len(unit_out_pos)):
                        unit_in_pos[x] = 0
                    unit_out_pos[8] = 1
                    unit_out = 'ft'
                elif Y_out.collidepoint(event.pos):
                    for i in range(0, len(unit_out_pos)):
                        unit_out_pos[x] = 0
                    unit_out_pos[9] = 1
                    unit_out = 'y'
                elif Mi_out.collidepoint(event.pos):
                    for i in range(0, len(unit_out_pos)):
                        unit_out_pos[x] = 0
                    unit_out_pos[10] = 1
                    unit_out = 'mi'
                elif Kg_out.collidepoint(event.pos):
                    for i in range(0, len(unit_out_pos)):
                        unit_out_pos[x] = 0
                    unit_out_pos[11] = 1
                    unit_out = 'kg'
                elif G_out.collidepoint(event.pos):
                    for i in range(0, len(unit_out_pos)):
                        unit_out_pos[x] = 0
                    unit_out_pos[12] = 1
                    unit_out = 'g'
                elif Lb_out.collidepoint(event.pos):
                    for i in range(0, len(unit_out_pos)):
                        unit_out_pos[x] = 0
                    unit_out_pos[13] = 1
                    unit_out = 'lb'

        if val != '':
            if val[0] == '.':
                val = '0' + val

        if unit_in == 'kg' or unit_in == 'g' or unit_in == 'lb':
            weight_1 = True
        else:
            weight_1 = False

        if unit_out == 'kg' or unit_out == 'g' or unit_out == 'lb':
            weight_2 = True
        else:
            weight_2 = False

        if unit_in != '' and unit_out != '':
            if weight_1 and weight_2 or weight_1 == False and weight_2 == False:
                if val != '':
                    try:
                        result = float(f"{float(val) * (SI[unit_in] / SI[unit_out]):.6f}")
                        Draw(val + ' -> ' + str(result), 30,450)
                    except ValueError:
                        Draw('erro', 30,450)
                else:
                    Draw('/', 30,450)
            else:
                Draw('erro', 30,450)
        
        elif val == '':
            Draw('/', 30,450)
        else:
            Draw('/' + val, 30,450)  

        pygame.display.update()

    if playing == True:
        Actions(17)

    pygame.display.update()
