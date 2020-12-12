import pygame,sys
import random

pygame.init()



class Player:
    def __init__(self,Velocity,Image):
        self.Image = Image
        self.CanShoot = True
        self.Timer = 0
        self.Health = 100
        self.score = 0
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
    def collision(self,obj):
        return collide(self,obj)
    def MoveLasers(self):
        for Laser in self.Lasers:
            Laser.y -= Laser.Velocity
            Laser.draw()
            if Laser.y < -2-self.height:
                self.Lasers.remove(Laser)
    def draw_health(self):
        pygame.draw.rect(window,(166, 169, 171),(self.x ,self.y+self.height+5 ,self.width , 10))
        pygame.draw.rect(window,(23 , 130, 237),(self.x ,self.y+self.height+5 ,self.Health/1.428571428571429 , 10))
    def draw(self):
        window.blit(self.Image,(self.x,self.y))

class Enemy:
    def __init__(self,Velocity,TypeA):
        self.Image,self.LaserImage = Type[TypeA]
        self.Velocity = Velocity
        self.x,self.y = random.randrange(2,Width-self.Image.get_width(),1),random.randrange(-5,-125,-1)
        self.mask = pygame.mask.from_surface(self.Image)
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
        self.damage = 15
        self.Image = Image
        self.x,self.y = pos
        self.mask = pygame.mask.from_surface(Image)
    @property
    def height(self):
        return self.Image.get_height()
    @property
    def width(self):
        return self.Image.get_width()
    def draw(self):
        window.blit(self.Image,(self.x,self.y))
    def collision(self,obj):
        return collide(self,obj)

Width,Height = 500,600
Wave = 1
NextwaveTimer = 0
EnemyNum = 2
EnemySpawnTimer = 0
EnemyEv = 3.8
Alive = True
clock = pygame.time.Clock()
Font1 = pygame.font.Font("CosmicAlien-V4Ax.ttf",25)
EnemyLaserShoot = pygame.USEREVENT
pygame.time.set_timer(EnemyLaserShoot,3*1200)

window = pygame.display.set_mode((Width,Height))
pygame.display.set_caption("Space Invader")

#Images
dir = "assets\\"
Background = pygame.image.load("{}background-black.png".format(dir)).convert()
Background = pygame.transform.scale(Background,(Width,Height))

PlayerImage = pygame.image.load("{}pixel_ship_yellow.png".format(dir))
PlayerImage = pygame.transform.scale(PlayerImage,(70,70))

sizex,sizey = 62,62
BlueShip = pygame.image.load("{}pixel_ship_blue_small.png".format(dir))
BlueShip = pygame.transform.scale(BlueShip,(sizex,sizey))

RedShip = pygame.image.load("{}pixel_ship_red_small.png".format(dir))
RedShip = pygame.transform.scale(RedShip,(sizex,sizey))

GreenShip = pygame.image.load("{}pixel_ship_green_small.png".format(dir))
GreenShip = pygame.transform.scale(GreenShip,(sizex,sizey))

Equation = (round(sizex/1.5),round(sizey/1.5))
yellow_laser = pygame.image.load("{}pixel_laser_yellow.png".format(dir))
red_laser = pygame.image.load("{}pixel_laser_red.png".format(dir))
red_laser = pygame.transform.scale(red_laser,Equation)
green_laser = pygame.image.load("{}pixel_laser_green.png".format(dir))
green_laser = pygame.transform.scale(green_laser,Equation)
blue_laser = pygame.image.load("{}pixel_laser_blue.png".format(dir))
blue_laser = pygame.transform.scale(blue_laser,Equation)

Ship_list = ["red","blue","green"]
Type = {'red':(RedShip,red_laser),
        'blue':(BlueShip,blue_laser),
        'green':(GreenShip,green_laser)}


MainShip = Player(2.7,PlayerImage)
Enemys = [Enemy(1.15,random.choice(Ship_list)),Enemy(1.15,random.choice(Ship_list))]

def reset_game():
    global EnemySpawnTimer,Wave,NextwaveTimer,Alive,EnemyEv
    MainShip.__init__(2.7,PlayerImage)
    EnemySpawnTimer = 0
    Wave = 1
    EnemyEv = 3.75
    NextwaveTimer = 0
    Enemys.clear()
    Alive = True

def collide(obj1, obj2):
    offset_x = round(obj2.x - obj1.x)
    offset_y = round(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def display_text():
    Score = Font1.render(f"Score: {MainShip.score}",True,(255,255,255))
    WaveText = Font1.render(f"Wave: {Wave}",True,(255,255,255))
    window.blit(WaveText,(0,30))
    window.blit(Score,(0,0))
    if not Alive:
        Over = Font1.render("Gameover Trash",True,(255,0,0))
        window.blit(Over,(Width/2-38,Height/2-28))

def MakeEnemy(Num):
    for _ in range(1,Num+1):
       Enemys.append(Enemy(random.choice((0.9,0.85,1)),random.choice(Ship_list)))

def ShootEnemyLaser():
    if len(Enemys) >= 2:
        for _ in range(1,4):
            ToShoot = random.choice(Enemys)
            L = Laser(random.choice((0.9*1.5,0.85*1.5,1*1.5)),ToShoot.LaserImage,(ToShoot.x+(ToShoot.width/2-22),ToShoot.y+(ToShoot.height/2+20)))
            ToShoot.Lasers.append(L)

def MoveEnemyLaser():
    for DumbAss in Enemys:
        for Bullet in DumbAss.Lasers:
            Bullet.y += Bullet.Velocity
            if Bullet.collision(MainShip) == True:
                MainShip.Health -= Bullet.damage
                DumbAss.Lasers.remove(Bullet)
            if Bullet.y > Height+Bullet.height:
                DumbAss.Lasers.remove(Bullet)
    for DumbAss in Enemys:
        for Bullet in DumbAss.Lasers:
            Bullet.draw()

def ShipStuff():
    global Alive
    for DumbAss in Enemys.copy():
        if DumbAss.y < -5:
            continue
        if DumbAss.y > Height-15:
            Enemys.remove(DumbAss)
        if MainShip.collision(DumbAss) == True:
            Enemys.remove(DumbAss)
            MainShip.Health -= 5
            MainShip.score += 1
        for Laser in MainShip.Lasers:
            if Laser.collision(DumbAss) == True:   
                Enemys.remove(DumbAss)
                MainShip.Lasers.remove(Laser)
                MainShip.score += 1
                break
    for DumbAss in Enemys:
        DumbAss.draw()
    MainShip.MoveLasers()
    if MainShip.Health <= 0:
        Alive = False
    MainShip.draw()
    MainShip.draw_health()

while True:
    clock.tick(120)
    if Alive:
        EnemySpawnTimer +=1
        if EnemySpawnTimer >= 120*(EnemyEv/2):
            EnemySpawnTimer = 0
            MakeEnemy(EnemyNum)
            print(EnemyEv)
        MainShip.Timer += 1
        if MainShip.Timer >= 120*(1/2):
            MainShip.Timer = 0
            MainShip.CanShoot = True
        NextwaveTimer +=1
        if NextwaveTimer >= 120*(25/2):
            Wave += 1
            EnemyEv -= 0.2
            NextwaveTimer = 0
    # Getting events        
    for event in pygame.event.get():
        if event.type == 12:
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == 32 and not Alive:
                reset_game()
        if event.type == EnemyLaserShoot and Alive:
            ShootEnemyLaser()

    keys = pygame.key.get_pressed()
    if Alive and keys[pygame.K_w] and MainShip.y > 1:    MainShip.y -= MainShip.Velocity
    if Alive and keys[pygame.K_a] and MainShip.x > 1:    MainShip.x -= MainShip.Velocity
    if Alive and keys[pygame.K_d] and MainShip.x < Width-MainShip.width-1:    MainShip.x += MainShip.Velocity
    if Alive and keys[pygame.K_s] and MainShip.y < Height-MainShip.height-1:    MainShip.y += MainShip.Velocity
    if Alive and keys[pygame.K_SPACE] and MainShip.CanShoot:
        MainShip.CanShoot = False
        L = Laser(2,yellow_laser,(MainShip.x-MainShip.width/2+17,MainShip.y-MainShip.height/2))
        MainShip.Lasers.append(L)

    window.blit(Background,(0,0))
    if Alive:
        MoveEnemyLaser()
        ShipStuff()
        
    display_text()
    pygame.display.update()
