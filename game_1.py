"""
README - Game Engine developed 22/05/2023

Variable names: CAMEL_CASE
Constants: CAPITALS

"""

############################################################################################################

#IMPORTS
import pygame,os,sys,math,random,time
import test
from HIMUServer import HIMUServer
from threading import Thread
from faker import Faker
fake=Faker()
pygame.init()
clock=pygame.time.Clock()
info = pygame.display.Info()
width=info.current_w
height=info.current_h
window = pygame.display.set_mode((width,height),pygame.FULLSCREEN)#pygame.FULLSCREEN
cwidth=1920
cheight=1280
canvas = pygame.Surface((1920,1280))#pygame.FULLSCREEN
pygame.mouse.set_visible(True)
pygame.display.set_caption('Game Name')
bigFont=pygame.font.SysFont(None, 90)
font = pygame.font.SysFont(None, 60)
smallFont = pygame.font.SysFont(None, 30)

cyclers=[pygame.image.load("cycler.png").convert_alpha(),
pygame.image.load("cycler2.png").convert_alpha(),
pygame.image.load("cycler.png").convert_alpha(),
pygame.image.load("cycler3.png").convert_alpha()]

cyclerWinIMG=pygame.image.load("cyclerWin.png").convert_alpha()

bushIMG=pygame.image.load("bush.png").convert_alpha()
grassIMG=pygame.image.load("grass.jpg").convert()
barIMG=pygame.image.load("bar.png").convert_alpha()

img_height=0
mousex,mousey=0,0

#Use dictionaries here
#LOADING FONTS

#LOAD GAME IMAGES
path = '/'
filenames = [f for f in os.listdir(path) if f.endswith('.png')]
images = {}
for name in filenames:
    imagename = os.path.splitext(name)[0] 
    images[imagename] = pygame.image.load(os.path.join(path, name)).convert_alpha()

#LOADING SOUNDS
pygame.mixer.init()
path = '/'
filenames = [f for f in os.listdir(path) if f.endswith('.wav')]
sounds = {}
for name in filenames:
    soundname = os.path.splitext(name)[0] 
    sounds[soundname] = pygame.mixer.Sound(os.path.join(path, name))

#GLOBALS 
fps=60
PI=math.pi



#DISTANCE OF THE RACE!!!########################################################
START=10000
################################################################################

REMAINING=START
CURRENT=1
SPEED_ARRAY=[]
MULTIPLIER=2
ANIMATION=0
CYCLE_IMG=0

AI_SPEEDS={"500":[10,80],"2000":[5,50],"5000":[4,40],"10000":[4,35],"20000":[6,35],"50000":[4,30]}
AISPEED=AI_SPEEDS[str(START)]

worldx,worldy=0,0

#OBJECTS ####################################################################################################

class ParticleEmitter:
    def __init__(self,x,y,direction,angle,output,colour,size,speed,circle,fade,randomness):
        self.array=[]
        self.x=x
        self.y=y
        self.direction=direction
        self.angle=angle
        self.output=output#p per second
        self.colour=colour
        self.size=size
        self.speed=speed
        self.circle=circle
        self.fade=fade
        self.rand=randomness
    def increment(self):
        new_p = int(self.speed)
        if random.random()>0.8:
            for i in range(new_p):
                angle=self.direction+random.uniform(-self.angle,self.angle)
                vx=math.cos(angle)*self.speed*random.uniform(1,self.rand)

                vy=math.sin(angle)*self.speed*random.uniform(1,self.rand)
                self.array.append(Particle(self.x,self.y,vx,vy,self.colour,self.size,self.circle,self.fade))

        for p in self.array:
            p.increment()
            if abs(p.vx)<2 and abs(p.vy)<2:
                self.array.remove(p)
    def draw(self):
        for p in self.array:
            p.draw()
        
class Particle:
    def __init__(self,x,y,vx,vy,colour,size,circle,fade):
        self.x=x-worldx
        self.y=y-worldy
        self.vx=vx
        self.vy=vy
        self.colour=colour
        self.size=size
        self.circle=circle
        self.fade=fade
    def increment(self):
        self.x+=self.vx
        self.y+=self.vy
        self.vx=self.vx*self.fade
        self.vy=self.vy*self.fade
    def draw(self):
        if self.circle:
            pygame.draw.circle(canvas,self.colour,(self.x+worldx,self.y+worldy),self.size)
        else:
            pygame.draw.rect(canvas,self.colour,(self.x+worldx,self.y+worldy,self.size,self.size),0)



class Rider():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.speed=0
        self.maxSpeed=random.randint(AISPEED[0],AISPEED[1])
        self.current=1
        self.angle=1.5
        self.cos=math.cos(self.angle)
        self.sin=math.sin(self.angle)
        self.img=pygame.transform.rotate(cyclers[0], -90)
        self.name=fake.name()
        #RANDOM NAME!



        self.text=smallFont.render(self.name, True, (255,255,255))
    def move(self):
        if self.current<len(pointArray)-1:
            if abs(self.x-(pointArray[self.current][0]))<500 and abs(self.y-(pointArray[self.current][1]))<500:
                #CLOSE TO CURRENT POINT
                self.current+=1
                #Move towards the current one, also angle cycler
                self.angle=math.atan2((self.y-(pointArray[self.current][1])),self.x-(pointArray[self.current][0]))
                self.cos=math.cos(self.angle)
                self.sin=math.sin(self.angle)
                self.img = pygame.transform.rotate(cyclers[0], -math.degrees(self.angle))

            self.x-=self.cos*self.speed
            self.y-=self.sin*self.speed

            #CHANGE SPEED HERE!!!!
            self.speed+=random.uniform(-self.speed/10,(self.maxSpeed-self.speed)/5)

    def draw(self):
        if worldx+self.x>-200 and worldx+self.x<2100 and worldy+self.y>-500 and worldy+self.y<2000:
            if self.current<len(pointArray)-1:
                #blitRotateCenter(canvas,cyclers[CYCLE_IMG],(worldx+self.x-236,worldy+self.y),-math.degrees(self.angle))
                rotated_image_rect = self.img.get_rect(center = (worldx+self.x,worldy+self.y))
                canvas.blit(self.img, rotated_image_rect)

    def drawName(self):
        if worldx+self.x>-200 and worldx+self.x<2100 and worldy+self.y>-500 and worldy+self.y<2000:
            if self.current<len(pointArray)-1:
                canvas.blit(self.text, (worldx+self.x-self.text.get_width()/2, worldy+self.y))
#FUNCTIONS ##################################################################################################





currentx=cwidth/2
currenty=2000
pointArray=[[currentx,currenty]]
bushArray=[]
angle=0
for i in range(int(START/10)):
    currentx=currentx+angle*50
    currenty=currenty-2000
    pointArray.append([currentx,currenty])
    angle=max(min(angle+random.randint(-3,3),30),-30)

def connectPoints():
    start=max(0,CURRENT-2)
    end=min(len(pointArray)-1,start+10)
    ps=[]
    for p in pointArray[start:end]:
        ps.append([p[0]+worldx,p[1]+worldy])
    pygame.draw.lines(canvas,(50,50,50),False,ps,800)
    pygame.draw.lines(canvas,(70,70,70),False,ps,750)



#CREATE RIDERS
riderArray=[Rider(cwidth/2,cheight/2)]
for i in range(20):
    riderArray.append(Rider(cwidth/2+random.randint(-300,300),cheight/2+random.randint(0,500)))
def processRiders():
    for r in riderArray:
        if started:
            r.move()
        r.draw()
    for r in riderArray:
        r.drawName()

#ROUND TO NEAREST MULTIPLE OF NUMBER PROVIDED
def rounder(number,multiple):
    return multiple*round(number/multiple)


#############################################SERVER

def server():
    #Change the timeout (in seconds) :
    myHIMUServer.timeout = 20
    myHIMUServer.start("TCP", 2055)
    print("done")
    server()

myHIMUServer = HIMUServer()
myListener = test.SimplePrintListener(myHIMUServer)
myHIMUServer.addListener(myListener)
thread=Thread(target=server)
thread.start()

###################################################






def blitRotateCenter(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect)

def rot_center(image, angle, x, y):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect


def moveCycler():
    global CURRENT,worldx,worldy,cyclerAngle,REMAINING,slip
    if CURRENT<len(pointArray)-1:
        if abs(cwidth/2-(worldx+pointArray[CURRENT][0]))<500 and abs(cheight/2-(worldy+pointArray[CURRENT][1]))<500:
            #CLOSE TO CURRENT POINT
            CURRENT+=1
            REMAINING-=10


        #Move towards the current one, also angle cycler
        cyclerAngle=math.atan2((cheight/2-(worldy+pointArray[CURRENT][1])),cwidth/2-(worldx+pointArray[CURRENT][0]))

        #SLIP STREAM
        slip=1
        for i in riderArray:
            if worldy+i.y>-100 and worldy+i.y<400:
                #SLIPSTREAM!!!!
                slip+=0.4 
                pygame.draw.rect(canvas,(255,255,255),(0,cheight-40,cwidth,40))
                p.colour=(200,200,200)
        if slip==1:
            p.colour=(40,40,40)

        

        worldx+=math.cos(cyclerAngle)*SPEED
        worldy+=math.sin(cyclerAngle)*SPEED
        #Aim at next point
        #Move world towadrs next point based on speed

    


def drawGrass():
    #500x300
    for x in range(5):
        for y in range(6):
            canvas.blit(grassIMG,(worldx%500+x*500-500,worldy%300+y*300-300))



def drawUI():
    global place,endTime,total

    canvas.blit(barIMG,(460,cheight-100))

    img = font.render(str(REMAINING)+"m/"+str(START)+"m", True, (30,144,255))
    canvas.blit(img, (500, cheight-90))
    img = font.render('FPS: '+str(int(fps)), True, (0,0,0))
    canvas.blit(img, (1700, 20))
    img = bigFont.render("{:.1f}".format(SPEED)+" km/h", True, (255,140,0))
    canvas.blit(img, (cwidth/2-img.get_width()/2, cheight-80))
    if disconnected:
        img = font.render('Disconnected', True, (255,0,0))
        canvas.blit(img, (cwidth/2-100, cheight/2))

    
    if CURRENT<len(pointArray)-1:
        endTime=int(time.time()-startTime)
        #GET PLACE
        total=1
        for i in riderArray:
            if worldy+i.y<cwidth/2:
                total+=1

    img = font.render(str(int(endTime/60))+"m "+str(endTime%60)+"s", True, (34,139,34))
    canvas.blit(img, (500, cheight-45))
    img = font.render(str(int(CURRENT*0.3))+" Kcal", True, (200,34,50))
    canvas.blit(img, (1200, cheight-70))

    img = font.render(str(total), True, (255,255,255))
    canvas.blit(img, (20, 140))

    #Progress bar
    pygame.draw.rect(canvas,(20,20,20),(20,200,6,1000))
    for i in riderArray:
        pygame.draw.circle(canvas,(170,20,20),(23,1200-int(1000*i.current/(START/10))),12)
    pygame.draw.circle(canvas,(20,170,20),(23,1200-int(1000*CURRENT/(START/10))),16)

#TESTS
#self,x,y,direction,angle,output,colour,size,speed,circle,fade,randomness
p=ParticleEmitter(cwidth/2,cheight/2,PI*0.5,0.1*PI,0.1,(40,40,40),5,5,True,0.9,2)
#p2=ParticleEmitter(500,500,0,2*PI,1,(20,0,255),10,20,False,0.8,3)
startTime=time.time()
endTime=0
place=1
cyclerAngle=1.5
started=False
slip=1
disconnected=False
total=0
#MAIN GAME LOOP #############################################################################################
while True:#Run until closed
    canvas.fill((34,139,34))#Fills background blue
    SPEED_ARRAY.append(myListener.total*MULTIPLIER*slip)
    if len(SPEED_ARRAY)>100:
        SPEED_ARRAY.pop(0)
        if SPEED_ARRAY[-1]==SPEED_ARRAY[-10] and SPEED_ARRAY[-2]==SPEED_ARRAY[-20] and SPEED_ARRAY[-1]>2:
            disconnected=True
        else:
            disconnected=False
    else:
        disconnected=True

    SPEED=sum(SPEED_ARRAY)/len(SPEED_ARRAY)


    drawGrass()
    connectPoints()
    if started:
        moveCycler()
        ANIMATION+=SPEED
        if ANIMATION>=600:
            CYCLE_IMG+=1
            ANIMATION=0
            if CYCLE_IMG>=4:
                CYCLE_IMG=0
    
    p.increment()
    p.draw()
    processRiders()
    if total==1:
        blitRotateCenter(canvas,cyclerWinIMG,(cwidth/2-236,cheight/2),-math.degrees(cyclerAngle))
    else:
        blitRotateCenter(canvas,cyclers[CYCLE_IMG],(cwidth/2-236,cheight/2),-math.degrees(cyclerAngle))


    drawUI()
    #Final Transform
    #SHOULD CONVERT TO OPENgl AND APPLY SHADERS HERE
    window.blit(pygame.transform.scale(canvas,(width,height)),(0,0))#Draws pixel surface onto screen

    for event in pygame.event.get():#Cycles all events (keys)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==pygame.FINGERDOWN:
            started=True
            startTime=time.time()


    pygame.display.flip()
    clock.tick(60)
    fps=clock.get_fps()


#Add heights and more map features
#Add downhill sections where don't lose
#Add saving of scores and a basic menu
#Make AI's stop for breaks, change their colour