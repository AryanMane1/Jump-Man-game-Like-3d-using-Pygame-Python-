import pygame.event
import pygame.display
import pygame.draw
import pygame.time
import pygame.image
import pygame.transform
import pygame.key
import pygame.mixer
import pygame,sys,random
import pygame.locals 

# Pre Initialize
pygame.init()
pygame.mixer.init()
pygame.display.init()
HEIGHT = 480
WIDTH = 1200
surface = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Adventure with Aryan")
CLOCK = pygame.time.Clock()


# Globle Variables
FPS = 50
SPEED = 8
counter = 0
All_Objects = []
obj_height = 180
color = {"red":(255,0,0),"blue":(0,0,255),"green":(0,255,0),"white":(255,255,255),"black":(0,0,0)}
player_Y_vel = 0
Player_X = 100
Player_Y = 250
next_img = 1
per_loop = 5
Player_Y_Stop = False
object_timer = 0
up_key_pressed = False
page_num = 0
passed_object = 0


#Images
BOX1 = pygame.image.load("images/box1.png").convert_alpha()
GameOver = pygame.image.load("images/game_over.png").convert_alpha()
BgImg = pygame.image.load("images/bg_img.jpg").convert_alpha()
StandImg = pygame.image.load("images/stand.png").convert_alpha()
All_players = {}
for i in range(1,5):
    All_players[f'{i}'] = pygame.image.load(f"images/image{i}.png").convert_alpha()
current_player = All_players['1']

# Sounds
Run = pygame.mixer.Sound('Sounds/run.mp3')
BgSound = pygame.mixer.Sound("Sounds/bg_sound.mp3")
JumpSound = pygame.mixer.Sound("Sounds/jump.mp3")
# BgSound.set_volume(0.4)


# Functions

def Blit_user():
    global next_img,current_player,Player_X,Player_Y
    if next_img==1:
        current_player = All_players['1']
        surface.blit(All_players["1"],(Player_X,Player_Y))
        if counter%per_loop==0:
            next_img=2
            return

    elif next_img==2:
        current_player = All_players['2']
        surface.blit(All_players['2'],(Player_X,Player_Y))
        if counter%per_loop==0:
            next_img=3
            return

    elif next_img==3:
        current_player = All_players['3']
        surface.blit(All_players['3'],(Player_X,Player_Y))
        if counter%per_loop==0:
            next_img=4
            return

    elif next_img==4:
        current_player = All_players['4']
        surface.blit(All_players['4'],(Player_X,Player_Y))
        if counter%per_loop==0:
            next_img=5
            return

    elif next_img==5:
        current_player = All_players['3']
        surface.blit(All_players['3'],(Player_X,Player_Y))
        if counter%per_loop==0:
            next_img=6
            return

    elif next_img==6:
        current_player = All_players['2']
        surface.blit(All_players['2'],(Player_X,Player_Y))
        if counter%per_loop==0:
            next_img=7
            return

    elif next_img==7:
        current_player = All_players['1']
        surface.blit(All_players['1'],(Player_X,Player_Y))
        if counter%per_loop==0:
            next_img=1
            return

def Add_blit_objects(timer,counter):
    global object_timer,passed_object
    if timer%random.randint(40,60-(counter//500))==0:
        All_Objects.append([WIDTH,HEIGHT-obj_height])
        object_timer = 0

    for i in range(len(All_Objects)):
        try:
            X_pos = All_Objects[i][0]
            Y_pos = All_Objects[i][1]
            if X_pos < -100:
                passed_object+=1
                All_Objects.remove(All_Objects[i])
            else:
                surface.blit(resize(BOX1,100,100),(X_pos,Y_pos))
                All_Objects[i][0]-=SPEED

        except:pass

def check_collide():
    global page_num
    for i in range(len(All_Objects)):
        try:
            obj_X_pos = All_Objects[i][0]
            obj_Y_pos = All_Objects[i][1]
            if Player_X < obj_X_pos < Player_X+current_player.get_width()-50 and Player_Y < obj_Y_pos < Player_Y+current_player.get_height():
                page_num =2    

        except:
            pass

def resize(image,width,height):
    return pygame.transform.scale( image ,(width,height))

def screen_text(text,font_size,colour,x,y):
    '''
    text,font_size,colour,x,y
    '''
    font = pygame.font.SysFont(None, font_size-5,bold=True)
    # font = pygame.font.get_fonts()[1]
    TEXT = font.render(text,True,colour)
    surface.blit(TEXT,[x,y])


# Next Globle variables
player_vel = 0
sec = 0
min = 0
over_Y=0
up,down = False,True

backgrounds = [[0,0],[WIDTH,0]]
NEW_bg_img = resize(BgImg,WIDTH,HEIGHT)
# pygame.mixer.Channel(1).play(Run,loops=-1)
pygame.mixer.Channel(1).play(BgSound,loops=-1)
while True:
    i = 0
    Key = pygame.key.get_pressed()

    for env in pygame.event.get():
        if env.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  

    if page_num == 0:
        surface.blit(resize(BgImg,WIDTH,HEIGHT),(0,0))
        surface.blit(StandImg,(Player_X,Player_Y))
        screen_text("Hello I am Aryan, I am very exited for this Adventure",55,(0,0,255),100,50)

        for env in pygame.event.get():
                if env.type == pygame.locals.MOUSEBUTTONDOWN:
                    page_num = 1

        screen_text("!! Tap here to Start game !!",46,(0,0,0),300,over_Y+330)
        if up:over_Y-=1
        elif down:over_Y+=1

        if over_Y>=100:
            down=False
            up = True
        if over_Y<=50:
            down=True
            up = False

    if page_num == 1:
        for i in range(len(backgrounds)):
            surface.blit(resize(BgImg,WIDTH,HEIGHT),(backgrounds[i][0],backgrounds[i][1]))
            backgrounds[i][0]-=SPEED

            if backgrounds[i][0]<=(0-WIDTH):backgrounds = [[0,0],[WIDTH,0]]
        if counter%1000==0 and counter!=0:FPS+=1

        screen_text(f"{str(min).zfill(2)}:{str(sec).zfill(2)}",50,(0,0,0),WIDTH-100,10)
        screen_text(f"Object passed : {passed_object}",40,(0,0,0),10,10)


        if (Key[pygame.locals.K_UP] or Key[pygame.locals.K_SPACE]) and Player_Y>=250 and Player_X==100 and not up_key_pressed:
            pygame.mixer.Channel(2).play(JumpSound)
            up_key_pressed = True

        if up_key_pressed:
            player_vel+=3
            if Player_Y > 50:
                Player_Y-=player_vel
            else:
                up_key_pressed = False

        if not up_key_pressed and Player_Y!=250:
            if player_vel >=0:
                player_vel = 0
            player_vel+=7
            if Player_Y < 250:
                Player_Y+=player_vel
            else:
                Player_Y = 250
                up_key_pressed = False

                
        # Objects
        Add_blit_objects(object_timer,counter)
        
        # Blit User
        Blit_user()

        #collide
        check_collide()

        if sec == 60:
            min+=1
            sec=0

        if counter%37==0:sec+=1

    if page_num == 2:
        surface.blit(GameOver,(400,50))
        screen_text("!! Tap here to Start New Game !!",50,(0,0,0),350,400)

        for env in pygame.event.get():
                if env.type == pygame.locals.MOUSEBUTTONDOWN:
                    counter=0
                    object_timer=0
                    sec,min=0,0
                    page_num = 1
                    FPS = 50
                    All_Objects = []
                    player_Y_vel = 0
                    next_img = 1
                    per_loop = 5
                    Player_Y_Stop = False
                    object_timer = 0
                    up_key_pressed = False
                    passed_object = 0
                    player_vel = 0
                    over_Y=0
                    up,down = False,True
                    backgrounds = [[0,0],[WIDTH,0]]


    pygame.display.update()
    CLOCK.tick(FPS)
    counter+=1
    object_timer+=1
