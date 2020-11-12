import pygame 

#initialzize pygame
pygame.init()


FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()
pygame.font.init()

#Display Name
pygame.display.set_caption("First Game")

#Screen width and height
screenWidth = 500
screenHeight = 480

#win = pygame.display.set_mode((screenWidth,screenHeight),pygame.FULLSCREEN)
win = pygame.display.set_mode((screenWidth,screenHeight))

##__SPRITES__##
#Walking right sprites
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
#Walking left sprites
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
#Background
bg = pygame.image.load('bg.jpg')
#Resting Sprite
char = pygame.image.load('standing.png')

#Clock Speed for FPS
clock = pygame.time.Clock()

#Load sounds
bulletSound = pygame.mixer.Sound('bullet.wav')
hitSound = pygame.mixer.Sound('hit.wav')

#Load and play music
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

score = 0;

#Class for Character 
class player(object):
    def __init__(self,x,y,width,height):
        #Attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5 #Velocity
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0 #Used for sprite walking animation
        self.standing = True
        self.hitbox = (self.x + 20, self.y, 28, 60) #Rectange hitbox
    
    #Movement 
    def draw(self,win):
        #Every time the walkcount goes up by 3, we change to the next sprite
        #If it move than the number of images we have (28/3>9) then we need to reset the walkcount
        #Or else we will get an index error
        #Add one as walkCount starts at 3
        if self.walkCount+1>=27:
            self.walkCount = 0
        
        #If moving
        if not(self.standing):        
            if self.left:
                #Integer division to get element of sprite, integer division by 3 as we only have 9 sprites for each direction
                win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            elif self.right:
                win.blit(walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
        else:            
            if self.right :
                #If not moving and facing right (so that the bullet goes in the right direction)
                win.blit(walkRight[0],(self.x,self.y))
            else:
                #If not moving and facing left (so that the bullet goes in the left direction)
                win.blit(walkLeft[0],(self.x,self.y))
        self.hitbox = (self.x + 20, self.y, 28, 60) #Move hitbox to character position
        #pygame.draw.rect(win,(255,0,0), self.hitbox,2) #Draw hitbox
        
    def hit(self):
        #Stop player from loading under floor
        self.isJump = False
        self.jumpCount = 10
        
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans',100)
        text = font1.render('-5',1,(255,0,0))
        win.blit(text,( (screenWidth/2)-(text.get_width()/2),(screenHeight/2)-(text.get_height()/2) ) )
        pygame.display.update()
        #Display message for 3 seconds
        i=0
        while i<300:
            pygame.time.delay(10)
            i+=1
            for event in pygame.event.get():
                #Allos user to exit whilst text is displayed
                if event.type == pygame.QUIT:
                    i=301
                    pygame.quit()


#Class for projectiles
class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
    
    #Drawing the bullet    
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)
        
#Enemy Class
class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]   
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x,self.end] #Furthest point left and right the enemy can move
        self.walkCount = 0 #Used to count sprite
        self.vel = 3
        self.hitbox = (self.x + 17, self.y+2, 31, 57)
        self.health = 10
        self.visible = True
        
    def draw(self,win):
        self.move()
        if self.visible:
            #Every time the walkcount goes up by 3, we change to the next sprite
            #If it move than the number of images we have (34/3>11) then we need to reset the walkcount
            #Or else we will get an index error
            #Add one as walkCount starts at 3
            if self.walkCount + 1 >=33:
                self.walkCount = 0
            
            if self.vel>0:
                win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount+=1
            else:
                win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount+=1
            #Red health bar    
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0],self.hitbox[1]-20,50,10))
            #Green health bar which loses width by a factor of 5 as health decreases
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0],self.hitbox[1]-20,50 - (5*(10 - self.health)),10))
            self.hitbox = (self.x + 17, self.y+2, 31, 57)
    
            #pygame.draw.rect(win,(255,0,0),self.hitbox,2) #Draw hitbox
    

    
    
    #Movement Method
    def move(self):
        if self.vel > 0: #Moving Right
            if self.x + self.vel< self.path[1]: #Lets the enemy move when he is within the RIGHT boundary
                self.x+=self.vel
            else:#Change direction one reaching the right bounary
                self.vel*=-1 #Move in the opposite direction
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]: #If moving left and within the LEFT boundary 
                self.x += self.vel #self.vel<0 here so it will make the x coordinate move towards 0 (so move left)
            else:#Change direction one reaching the LEFT bounary
                self.vel*=-1 #Move in the opposite direction
                self.walkCount = 0
    
    #Method for enemy being hit by projectile 
    def hit(self):
        print("Hit")
        if self.health>0:          
            self.health-=1
        else:
            self.visible=False
        

#Drawing to the screen    
def redrawGameWindow():
    #Draw Background
    win.blit(bg,(0,0))
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text,(350,10))
    #Draw man
    man.draw(win)
    #Draw enemy
    goblin.draw(win)
    #Drawing bullets 
    for bullet in bullets:
        bullet.draw(win)
      
        
    #Apply changes
    pygame.display.update()

#MainLoop
#font variable    
font = pygame.font.SysFont('comicsans',30,True)     
#Initialize character
man = player(300,410,64,64)
#Initialize Enemy
goblin = enemy(100,410,64,64,450)
shootLoop = 0 
#List for bullets 
bullets = []
run = True
while run :
    #FPS to 27 
    clock.tick(27)
    
    #Stops player from colliding when goblin is no longer alive/visible
    if goblin.visible == True:
        #Checks for enemy and player collision
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0]+ goblin.hitbox[2]:
                man.hit()
                score-=5
    
    if shootLoop > 0 :
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    
    #Exiting Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    for bullet in bullets:
        #Check to see if the top of the bullet is above the bottom of the goblin hitbox
        #And check to see if the bottom of the bullet is below the top of the goblin hitbox  
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            #Check to see if the bullet is within the left side of the hitbox ==> [?is the bullet here?(goblin)]
            #AND Check to see if the bullet is within the right side of the hitbox ==> [(goblin)?is the bullet here?]
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x-bullet.radius < goblin.hitbox[0]+ goblin.hitbox[2]:
                hitSound.play()
                goblin.hit()
                score+=1
                bullets.pop(bullets.index(bullet)) #Remove bullet from screen
        
        
        #If the bullet is on the screen
        if bullet.x < 500 and bullet.x>0:
            bullet.x += bullet.vel
        else:
            #Delete the bullet once off the screen
            bullets.pop(bullets.index(bullet))
            
    
    #List to store key presses        
    keys = pygame.key.get_pressed() 

    #Determine the direction to shoot the bullet depending on the direction of the man
    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        #Adding new bullet to bullets list, bullet comes from centre of the man due to adding x and y to HALF of the width and height respectively
        if len(bullets)<5:
           bullets.append(projectile(round(man.x+man.width//2), round(man.y+man.height//2), 6, (0,0,0) , facing)) 
        
        shootLoop = 1
    
    #Moving LEFT
    if keys[pygame.K_LEFT] and man.x >man.vel:
       man.x -= man.vel
       man.left=True 
       man.right=False #Doing this stops the program getting confused
       man.standing = False
    #Moving RIGHT
    elif keys[pygame.K_RIGHT] and man.x<screenWidth - man.width - man.vel :
        man.x += man.vel
        man.right=True
        man.left=False
        man.standing = False
    #STATIONARY
    else:
        man.standing = True
        man.walkCount = 0
    
    #JUMPING
    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right=False
            man.left = False
            man.walkCount = 0
    else:
        #Jump physics, man.jumpCount initially is 10. Man is moving up until jumpCount is 0 then moves down
        if man.jumpCount >= -10: #
            neg = 1 #Makes the man go up
            if man.jumpCount <0: #Turining point
                neg = -1 #Makes the man go down
            #When neg=1, the y is decreasing (moving towards the origin) so the man moves up
            #When neg=-1, the calculation results y increasing(negative of the calculation cancels out when minusing from man.y) so the man moves back down
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump=False
            man.jumpCount = 10
    
    
    #Drawing the game window 
    redrawGameWindow()

#Quit the game when the user closes tab                
pygame.quit()
    