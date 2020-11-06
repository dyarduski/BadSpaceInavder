import pygame,sys
import random

pygame.init()



class Player:
    def __init__(self,Velocity,Image):
        self.Image = Image
        self.CanShoot = True
        self.Lasers = []
        self.x,self.y = Width/2-Image.get_width(),Height-45
        self.mask = pygame.mask.from_surface(Image)
        self.Velocity = Velocity
    @property
    def height(self):
        return self.Image.get_height()
    @property
    def width(self):
        return self.Image.get_width()
    def draw(self):
        window.blit(self.Image,(self.x,self.y))

class Enemy:
    def __init__(self,Velocity,Image):
        self.Image = Image
        self.Velocity = Velocity
        self.x,self.y = random.randrange(2,Width-self.Image.get_width(),1),random.randrange(-5,-75,-1)
        self.mask = pygame.mask.from_surface(Image)
        self.Lasers = []
    @property
    def height(self):
        return self.Image.get_height()
    @property
    def width(self):
        return self.Image.get_width()
    def draw(self):
        self.y += self.Velocity 
        window.blit(self.Image,(self.x,self.y))


class Laser:
    def __init__(self,Velocity,Image,pos):
        self.Velocity = Velocity
        self.Image = Image
        self.x,self.y = pos
        self.mask = pygame.mask.from_surface(Image)
    def draw(self):
        self.y -= self.Velocity 
        window.blit(self.Image,(self.x,self.y))
    def collision(self,obj):
        return collide(self,obj)

Width,Height = 500,600
clock = pygame.time.Clock()
Enemy_Event = pygame.USEREVENT
pygame.time.set_timer(Enemy_Event,3*1000)
window = pygame.display.set_mode((Width,Height))
pygame.display.set_caption("Space Invader")

#Images
dir = "assets\\"
Background = pygame.image.load("{}background-black.png".format(dir)).convert()
Background = pygame.transform.scale(Background,(Width,Height))

PlayerImage = pygame.image.load("{}pixel_ship_yellow.png".format(dir))
PlayerImage = pygame.transform.scale(PlayerImage,(70,70))

sizex,sizey = 65,65
BlueShip = pygame.image.load("{}pixel_ship_blue_small.png".format(dir))
BlueShip = pygame.transform.scale(BlueShip,(sizex,sizey))

RedShip = pygame.image.load("{}pixel_ship_red_small.png".format(dir))
RedShip = pygame.transform.scale(RedShip,(sizex,sizey))

GreenShip = pygame.image.load("{}pixel_ship_green_small.png".format(dir))
GreenShip = pygame.transform.scale(GreenShip,(sizex,sizey))

Ship_list = [BlueShip,RedShip,GreenShip]

yellow_laser = pygame.image.load("{}pixel_laser_yellow.png".format(dir))
red_laser = pygame.image.load("{}pixel_laser_red.png".format(dir))
green_laser = pygame.image.load("{}pixel_laser_green.png".format(dir))
blue_laser = pygame.image.load("{}pixel_laser_blue.png".format(dir))



MainShip = Player(2.7,PlayerImage)
Enemys = []

def collide(obj1, obj2):
    offset_x = round(obj2.x - obj1.x)
    offset_y = round(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def ShipStuff():
    for DumbAss in Enemys:
        DumbAss.draw()
        if DumbAss.y > Height-+15:
            Enemys.remove(DumbAss)
        for Laser in MainShip.Lasers:
            if Laser.collision(DumbAss) == True:   
                Enemys.remove(DumbAss)
                MainShip.Lasers.remove(Laser)
                break
    for Laser in MainShip.Lasers:
        Laser.draw()
        if Laser.y < -15:
            MainShip.Lasers.remove(Laser)

    MainShip.draw()

Timer = 0
while True:
    clock.tick(120)
    Timer += 1
    if Timer >= 120*(1/2):
        Timer = 0
        MainShip.CanShoot = True
    for event in pygame.event.get():
        if event.type == 12:
            sys.exit()
        if event.type == Enemy_Event:
            for i in range(1,6):
                Enemys.append(Enemy(1.35,random.choice(Ship_list)))
                

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and MainShip.y > 1:    MainShip.y -= MainShip.Velocity
    if keys[pygame.K_a] and MainShip.x > 1:    MainShip.x -= MainShip.Velocity
    if keys[pygame.K_d] and MainShip.x < Width-MainShip.width-1:    MainShip.x += MainShip.Velocity
    if keys[pygame.K_s] and MainShip.y < Height-MainShip.height-1:    MainShip.y += MainShip.Velocity
    if keys[pygame.K_SPACE] and MainShip.CanShoot:
        MainShip.CanShoot = False
        L = Laser(2,yellow_laser,(MainShip.x-MainShip.width/2+17,MainShip.y-MainShip.height/2))
        MainShip.Lasers.append(L)

    window.blit(Background,(0,0))
    ShipStuff()

    pygame.display.update()