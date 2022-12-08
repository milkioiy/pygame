import pygame
import time
import sys

pygame.init()   


TITLE="KNU"
WHITE=(255, 255, 255)

screen_width = 1060 # 가로 크기
screen_height = 795 # 세로 크기

game_result=None
total_time = 20
start_ticks=pygame.time.get_ticks()
elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000


win = pygame.display.set_mode((screen_width, screen_height))


pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('Run (1).png'), pygame.image.load('Run (2).png'), pygame.image.load('Run (3).png'), pygame.image.load('Run (4).png'), pygame.image.load('Run (5).png'), pygame.image.load('Run (6).png'), pygame.image.load('Run (7).png'), pygame.image.load('Run (7).png'), pygame.image.load('Run (1).png')]
walkLeft = [pygame.image.load('Run (1).png'), pygame.image.load('Run (2).png'), pygame.image.load('Run (3).png'), pygame.image.load('Run (4).png'), pygame.image.load('Run (5).png'), pygame.image.load('Run (6).png'), pygame.image.load('Run (7).png'), pygame.image.load('Run (7).png'), pygame.image.load('Run (1).png')]
bg = pygame.image.load('BG.png')
char = pygame.image.load('Run (1).png')

clock = pygame.time.Clock()

#배경음
bulletSound = pygame.mixer.Sound("Game_bullet.mp3")
hitSound = pygame.mixer.Sound("Game_hit.mp3")

music = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

score = 0

#클래스별 함수 정의
class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(self)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False
    
                
def hit(self):
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)


#
class enemy(object):
    walkRight = [pygame.image.load('ene.png'), pygame.image.load('ene.png'), pygame.image.load('ene.png'), pygame.image.load('ene.png'), pygame.image.load('ene.png'), pygame.image.load('ene.png'), pygame.image.load('ene.png'), pygame.image.load('ene.png'), pygame.image.load('ene.png'), pygame.image.load('ene.png'), pygame.image.load('ene.png')]
    walkLeft = [pygame.image.load('ene.png'), pygame.image.load('ene.png'), pygame.image.load('ene.png'), pygame.image.load('ene.png'), pygame.image.load('ene.png'), pygame.image.load('ene.png'), pygame.image.load('ene.png'), pygame.image.load('ene.png'), pygame.image.load('ene.png'), pygame.image.load('ene.png'), pygame.image.load('ene.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')

    

def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (480, 50))
    man.draw(win)
    goblin.draw(win)
    goblin2.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    
    pygame.display.update()
    
BLACK =(0,0,0)

def display_game_over():
    
    game_font = pygame.font.SysFont("arialrounded", 60) # 폰트 사이즈를 조금 더 크게 사용하기 위해서 새로 설정!!
    txt_game_over = game_font.render(game_result, True, BLACK)
    rect_game_over = txt_game_over.get_rect(center = (int(screen_width / 2), int(screen_height / 2))) # 렌더링한 글자의 센터를 스크린의 중앙으로 설정한 좌표값 저장   
    win.blit(txt_game_over, rect_game_over) 
    
    
    # 렌더링한 글자의 센터를 스크린의 중앙으로 하는 좌표값을 이용해서 txt_game_over 출력
    # 위에서 출력하기 위해 사용한 blit와는 다르게 글자의 센터를 맞추고 출력하기 위해 rect_game_over 변수를 생성함!!
    
    
def display_time(time): # 시간을 출력하는 함수
    txt_timer = font.render(f"Time : {time}", True, BLACK) # 매개변수로 받은 시간값을 이용해 만든 텍스트를 txt_timer 변수에 삽입
    win.blit(txt_timer, (900, 50)) # 오른쪽 위에 시간을 출력

def Game_Border():
    Start_Point = [(100,150),(100,150),(100,550),(900,150)]
    End_Point = [(100,550),(900,150),(900,550),(900,550)]
    for index in range(len(Start_Point)):
        pygame.draw.line(win,(255,255,255),Start_Point[index],End_Point[index])



#mainloop



font = pygame.font.SysFont('comicsans', 30, True)
man = player(200, 410, 64,64)
goblin = enemy(100, 410, 64, 64, 450)
goblin2 = enemy(300, 410, 64, 64, 450)
shootLoop = 0
bullets = []
run = True
 # 게임이 진행중인지 확인하기

 #main      
while run:
    

    #이벤트 루프
    
    clock.tick(27)


    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

       
    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                hitSound.play() #음악플레이
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
                
        if bullet.x < 500 and bullet.x > 0: #500이내에서만 총알이 발사되도록
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    
    for bullet in bullets:
        if bullet.y - bullet.radius < goblin2.hitbox[1] + goblin2.hitbox[3] and bullet.y + bullet.radius > goblin2.hitbox[1]:
            if bullet.x + bullet.radius > goblin2.hitbox[0] and bullet.x - bullet.radius < goblin2.hitbox[0] + goblin2.hitbox[2]:
                hitSound.play() #음악플레이
                goblin2.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
                
        if bullet.x < 500 and bullet.x > 0: #500이내에서만 총알이 발사되도록
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))        
            

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
            
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 6, (0,0,0), facing))

        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 1060 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
        
    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ticks의 기본인 ms(밀리초) 단위를 s(초) 단위로 바꿔줌!
    display_time(total_time - int(elapsed_time))   
    goal_score = 40 # 목표 점수  
    
    
    #목표점수
    if total_time - int(elapsed_time)<=0:
        run = False
        if score >= goal_score:  
            game_result = "Mission Complete"
            print("Mission Complete")
            
            
        else:
            game_result = "Game Over"
            print("Game Over")
                 
        display_game_over()
        pygame.display.update()
        time.sleep(2)
        
          
    pygame.display.update() 
    
           
    redrawGameWindow()  
   
pygame.quit()

    
