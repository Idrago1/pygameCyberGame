
# Import and initialize the pygame library
import pygame
from pygame.locals import *
import tkinter as tk
import random 
from pygame import mixer




# Simple pygame program
"""
Functions for the Game 
"""


lava_group = pygame.sprite.Group()
blob_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
sign_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
computer_group = pygame.sprite.Group()
fireBalls_group = pygame.sprite.Group()

gameover = 0
signNum = 0
computerS = False
screen_width = 1366
screen_height = 768

trueHight = int(screen_height-screen_height/7)
trueWidth = int (screen_width-screen_width/15)

class Player():
    def __init__(self, x, y):
       self.reset(x,y)

    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 5
        signStatus = 0
        
        
        global gameover,level,world,change,textPopUp,signNum,computerS
        if gameover == 0 and textPopUp == False:
            #get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                self.vel_y = -15
                self.jumped = True
            #if key[pygame.K_SPACE] == False:
                
                
            if (key[pygame.K_LEFT]):
                dx -= 5
                self.counter += 1
                self.direction = -1
            if (key[pygame.K_RIGHT]):
                dx += 5
                self.counter += 1
               
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

        print(self.direction)
        #handle animation
        if self.counter > walk_cooldown:
            self.counter = 0    
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]


        #add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        #check for collision
        for tile in world.tile_list:
            #check for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                self.jumped = False
            #check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                    
                #check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.jumped = False

        if pygame.sprite.spritecollide(self, lava_group, False):
            print("you dead")
            gameover = 1
        if pygame.sprite.spritecollide(self, blob_group, False):
            print("You dead")
            gameover = 1
        if pygame.sprite.spritecollide(self, portal_group, False):
            level+=1
            blob_group.empty()
            portal_group.empty()
            lava_group.empty()
            sign_group.empty()
            spike_group.empty()
            signStatus = 0
            world_build = levelBuild(level)
            world = World(world_build)
            change = True
            print(level)
        if pygame.sprite.spritecollide(self, sign_group, False):
            textPopUp = True
            signNum = level
           
        
        if pygame.sprite.spritecollide(self, spike_group, False):
            print("You dead")
            gameover = 1
        if pygame.sprite.spritecollide(self, fireBalls_group, False):
            print("You dead")
            gameover = 1
        if pygame.sprite.spritecollide(self, computer_group, False):
           
            computerS = True
            mixer.music.stop()
            mixer.init()
            mixer.music.load("musicTerm.mp3")
            mixer.music.set_volume(0.7)
            mixer.music.play(-1)
            print("Hi this is " + str(computerS))
                
        
        #update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        #draw player onto screen
        ideam.blit(self.image, self.rect)
        #pygame.draw.rect(ideam, (255, 255, 255), self.rect, 2)
    def reset(self,x,y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 6):
            img_right = pygame.image.load('sprite_'+str(num)+".png")
            img_right = pygame.transform.scale(img_right, (tile_size, tile_size*2))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        
class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        dirt_img = pygame.image.load('dirt.png')
        grass_img = pygame.image.load('grass.png')
        mettal_img = pygame.image.load('metalBlock.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size// 2))
                    lava_group.add(lava)
                if tile == 4:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15,'sprite_00.png')
                    blob_group.add(blob)
                if tile == 5:
                    port = portal(col_count * tile_size, row_count * tile_size-tile_size)
                    portal_group.add(port)
                if tile == 6:
                    sign1 = sign(col_count * tile_size, row_count * tile_size-tile_size)
                    sign_group.add(sign1)
                if tile == 7:
                    spike1 = spike(col_count * tile_size, row_count * tile_size + (tile_size// 2))
                    spike_group.add(spike1)
                if tile == 8:
                    comp = computer(col_count * tile_size, row_count * tile_size-tile_size)
                    computer_group.add(comp)
                if tile == 9:
                    img = pygame.transform.scale(mettal_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == "f":
                    fire = fireBall(col_count * tile_size, row_count * tile_size + 15)
                    fireBalls_group.add(fire)
                if tile == "r":
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15,'person.png')
                    blob_group.add(blob)
                    
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            ideam.blit(tile[0], tile[1])
            #pygame.draw.rect(ideam, (255, 255, 255), tile[1], 2)
            

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('lavaBlock.png')
        img = pygame.transform.scale(img, (tile_size, tile_size))
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('spike.png')
        img = pygame.transform.scale(img, (tile_size, tile_size))
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y        
        

class portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('portal.png')
        img = pygame.transform.scale(img, (tile_size, tile_size))
        self.image = pygame.transform.scale(img, (tile_size, tile_size*2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class sign(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('sign.png')
        img = pygame.transform.scale(img, (tile_size, tile_size))
        self.image = pygame.transform.scale(img, (tile_size, tile_size*2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > tile_size*2:
            
            self.move_direction *= -1
            self.move_counter *= -1


class fireBall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('fireBall.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        

    def update(self):
        
        self.rect.y += self.move_direction * 1
        self.move_counter += 1
        if abs(self.move_counter) > tile_size*3:
            self.image = pygame.image.load('fireBall.png')
            self.image = pygame.transform.flip(self.image, True, True)
            self.move_direction *= -1
            self.move_counter *= -1
        



class computer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('computer.png')
        img = pygame.transform.scale(img, (tile_size, tile_size))
        self.image = pygame.transform.scale(img, (tile_size, tile_size*2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        #draw button
        ideam.blit(self.image, self.rect)
        return action

def levelChanger(level):
    return pygame.image.load(levelBack[level])

def restartLevel(x,y):
    global level,actualLevel,skip
    print("This is the restart one ")
    if (x >= y):
        print("This is the restart one ")
        
        level +=1; 
        
        skip = True
        actualLevel=pygame.transform.scale(pygame.image.load(levelBack[level]), (trueWidth, trueHight))
        return 50;
    else:
         return x

    
        


def draw_grid():
    for line in range(0, 48):
        pygame.draw.line(ideam, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(ideam, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))
        
def levelBuild(lev):
    doc = "world" + str(lev)
    with open(doc+".txt") as f:
        thing = f.read()
    listThing = thing.split("\n")
    realList = []
    temp = []

    for j in range(len(listThing)):
        for i in range (len(listThing[j])):
            try:
                temp.append(int(listThing[j][i]))
            except ValueError:
                temp.append(str(listThing[j][i]))
            
            if i >= len(listThing[j])-1:
                realList.append(temp)
                temp = []
    return realList
    
def ButtonImg(img,w,h):
    
    temp = pygame.image.load(img);
    temp=pygame.transform.scale(temp, (w, h))
    return temp

def messageStuff(lev):
    for i in range(lev+1):
        doc = "message" + str(i)
        with open(doc+".txt") as f:
            thing = f.read()
        print("hi momomo")
        termM.append(thing)
def messagePop (text,s,x= trueWidth // 2,y= trueHight / 3):
        
        font = pygame.font.Font('freesansbold.ttf', s)
        text = font.render(text, True, (0, 0, 128), (255, 255, 255))
        
        textRect = text.get_rect()
        print(text)
        textRect.center = (x, y)
        print(textRect)
        ideam.blit(text, textRect)
        
def restartT():
        global level
        
        switch = False
        mixer.music.stop()
        level+=1
        computer_group.empty()
        world_build = levelBuild(level)
        world = World(world_build)
        player.reset(trueWidth/2, screen_height - 130)


    
#varibles 
vel = 10
stage = 0
run = True
starter = True
change = False
textPopUp = False
switch = False
tempB = False
thing = False

term1A = False


    

teminalLevel = 0 
termM = []
messageStuff(2)

why = ["The reason why we are doing this is to stop all the hackers from taking your info. The only people that should be here are bob,jim,and cat","Complexity is 8 or more charicters and you must have 1 number,1 speceahl chericter, 1 uppercase letter, and you could do what ever with the rest","Wire shark looks super shady btw"]
    
    
root = tk.Tk()


x = 50
y = 2*(trueHight -trueHight/8)
ground = y
width = 40
height = 60
clock = pygame.time.Clock()



level = 0;
levelBack = ["FOREST.jpg","background2.jpg"] 
signText = ["You could move using the arrow keys and jump using the spacebar" ,"be carfull not ot touch the bad things","You could wall jump btws"]

actualLevel = pygame.transform.scale(pygame.image.load(levelBack[level]), (trueWidth, trueHight))

tile_size = 40;

world_build = levelBuild(level)
world = World(world_build)

pygame.init()
print(str(screen_width) +" , "+ str(screen_height))
ideam = pygame.display.set_mode((trueWidth,trueHight))
pygame.display.set_caption("this is my first game")
pygame.time.delay(50)
player = Player(x, screen_height - 130)


okImg = ButtonImg("okButton.jpg",tile_size*2,tile_size*2)

bobImg = ButtonImg("bobNameTag.png",tile_size*2,tile_size*2)
catImg = ButtonImg("catNameTag.png",tile_size*2,tile_size*2)
jimImg = ButtonImg("jimNameTag.png",tile_size*2,tile_size*2)
jimmyImg = ButtonImg("samNameTag.png",tile_size*2,tile_size*2)




secondStage = ButtonImg("clocktower.jpg",trueWidth,trueHight)

terminalImg = ButtonImg("terminal.jpg",tile_size*2,tile_size*2)
terminalEmptyImg = ButtonImg("emptyTerminal.jpg",tile_size*20,tile_size*10)
reImg = ButtonImg("restartButton.jpg",tile_size*10,tile_size*2)
imgStart = ButtonImg("Logo.png",trueWidth,trueHight)
terminalExitimg = ButtonImg("exitButton.jpg",tile_size*5,tile_size*2)
imgWindow = ButtonImg("windows.jpg",trueWidth,trueHight)

xB = ButtonImg("xBtn.png",tile_size*2,tile_size*2)
imgStartB = ButtonImg("startButton.jpg",tile_size*5,tile_size*2)
messImg =  ButtonImg("sign.png",tile_size*2,tile_size*2)

writingS = ButtonImg("note.png",tile_size*2,tile_size*2)
game = ButtonImg("Logo.png",tile_size*2,tile_size*2)
shark = ButtonImg("sharkFin.png",tile_size*2,tile_size*2)

imageExit = ButtonImg("restartButton.jpg",tile_size*5,tile_size*2)

# Buttons


restartB = Button(trueWidth/3 , trueHight//2 + 100,reImg)
exitB = Button(3*(trueWidth//5)  , trueHight/2 + 100,terminalExitimg)
okB = Button(trueWidth//2 , trueHight/8,okImg)

restartB = Button(trueWidth/3 , trueHight//2 + 100,reImg)
restartB2 = Button(tile_size , tile_size,imageExit)
StartB = Button(trueWidth/4 , trueHight//2 + 100,imgStartB)
xBu = Button((trueWidth/8)*6 , trueHight/8,xB)
terminalExit = Button(trueWidth-terminalExitimg.get_width()-tile_size ,tile_size ,terminalExitimg)


terminal = Button(0 ,terminalImg.get_height() ,terminalImg)

extraMess = Button(0 ,terminalImg.get_height()*4 ,messImg)
mess = Button(0 ,terminalImg.get_height()*2 ,messImg)
whyB = Button(0 ,terminalImg.get_height()*3 ,messImg)

person1 = Button(trueWidth/8, (trueHight/5)*2 ,bobImg)
person2 = Button(trueWidth/8, (trueHight/5)* 3,catImg)
person3 = Button(trueWidth/8 * 2, (trueHight/5)*2 ,jimmyImg)
person3m = Button(trueWidth/8 , (trueHight/5)*4 ,jimmyImg)
person4 = Button(trueWidth/8 *2, (trueHight/5)* 3,jimImg)

icon = Button(trueWidth/8, (trueHight/5)*2 ,writingS)
icon2 = Button(trueWidth/8, (trueHight/5)* 3,shark)
icon3 = Button(trueWidth/8, (trueHight/5)*4 ,game)
icon4 = Button(trueWidth/8 , (trueHight/5)*4 ,jimmyImg)


mixer.init()
mixer.music.load("mainSong.mp3")
mixer.music.set_volume(0.7)
mixer.music.play(-1)



mainText = ""
while(run):

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
			
    # This will give us a dictonary where each key has a value of 1 or 0. Where 1 is pressed and 0 is not pressed.
        
    
    
    if computerS == True:
        
        
        
        
        
        if mess.draw():
            switch = True
            textPopUp = False
            
            messagePop (termM[teminalLevel],15)
        if whyB.draw():
            switch = True
            textPopUp = False
            
            messagePop (why[teminalLevel],15,y=(trueHight / 7)*2)
        if teminalLevel == 1:
            if extraMess.draw():
                switch = True
                textPopUp = False
                
                messagePop ("You have to find the people who do have complexities in their password",20,x =trueHight /8 *6, y=(trueHight / 7)*1)
                
        if xBu.draw():
                switch = False
                textPopUp = False
                tempB =False
                
        
        if teminalLevel == 0:
            if person1.draw():
                print("this is not it")
                mixer.music.load("error.mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play()
                
                
            if person2.draw():
                print("this is not it")
                mixer.music.load("error.mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play()
                
            if person3.draw():
                restartT()
                computerS = False
                switch = False
                tempB = False
                mixer.music.load("mainSong.mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play(-1)

                teminalLevel+=1
            if person4.draw():
                print("this is not it")
                mixer.music.load("error.mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play()
                
        
        if teminalLevel ==1:
            messagePop ("fewgreA!1",24,x= 2*(trueWidth/8),y= (trueHight/5)*2)
            messagePop ("fewfew",24,x= 2*(trueWidth/8),y=(trueHight/5)*3)
            messagePop ("132Fe",24,x= 2*(trueWidth/8),y= (trueHight/5)*4)
            
            
            
            if person1.draw():
                restartT()
                computerS = False
                switch = False
                tempB = False
                mixer.music.load("mainSong.mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play(-1)
                teminalLevel+=1
                stage+=1
            if person2.draw():
                print("this is not it")
                mixer.music.load("error.mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play()
                
            if person3m.draw():
                print("Meh")
                mixer.music.load("error.mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play()
                
        
        if teminalLevel ==2:
            messagePop ("Notes",24,x= 2*(trueWidth/8),y= (trueHight/5)*2)
            messagePop ("Cyber Force",24,x= 2*(trueWidth/8),y=(trueHight/5)*3)
            messagePop ("WireShark",24,x= 2*(trueWidth/8),y= (trueHight/5)*4)
            
            
            if icon.draw():
                print("this is not it")
                mixer.music.load("error.mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play()
                
            if icon2.draw():
                
                restartT()
                computerS = False
                switch = False
                tempB = False
                mixer.music.load("mainSong.mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play(-1)
                teminalLevel+=1
                stage+=1
            if icon3.draw():
                print("Meh")
                mixer.music.load("error.mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play()
                
        
        
        if switch == False:
            ideam.blit(imgWindow, (0, 0))
            
        
            
        if terminalExit.draw()==True:
            computerS = False
            switch = False
            mixer.music.stop()
            player.reset(trueWidth/2, screen_height - 130)
        if terminal.draw() == True:
            switch = True
            
            if (tempB == False):
                ideam.blit(terminalEmptyImg, (trueWidth/8, trueHight/5))
                tempB = True
                thing == True
            
            
                    
                
            
        

    else:
        
        
        
        if starter == True:
            print("hi")
            
            ideam.blit(imgStart, (0, 0))
            
            if StartB.draw()==True:
                starter = False
            if exitB.draw()==True:
                run = False
            
        else:
            
            
            if stage == 0:
                ideam.blit(actualLevel, (0, 0))
            if stage == 1:
                ideam.blit(secondStage, (0, 0))
            fireBalls_group.update()
            blob_group.update()
            #skiper
            if terminalExit.draw():
                run = False
            
            if level == 14:
                messagePop ("Congrats You Beet The Game",30,x= 2*(trueWidth/8),y= (trueHight/5)*2)
                mixer.music.load("happy.mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play(-1)
                
                
            if restartB2.draw():
                player.reset(x, screen_height - 130)
            if gameover==1:
                if restartB.draw()== True:
                    player.reset(x, screen_height - 130)
                    gameover = 0
            if change == True:
                
                player.reset(x, screen_height - 130)
                change = False;
            if textPopUp == True:
                
                messagePop (signText[signNum],36)
                if okB.draw():
                    sign_group.empty()
                    textPopUp = False
            
            world.draw()
            
            computer_group.draw(ideam)
            lava_group.draw(ideam)
            spike_group.draw(ideam)
            portal_group.draw(ideam)
            fireBalls_group.draw(ideam)
            blob_group.draw(ideam)
            sign_group.draw(ideam)
            
            
            
            player.update()
    pygame.display.update() 

pygame.quit()

