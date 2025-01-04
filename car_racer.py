from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time


# Global Variables
screen_x= 600
screen_y= 650
chances_life=3
highscore=0
score=0   
is_paused=False
gameover=False
lanes= [200,300,400]
speed=4

health_powerup_falling=False


TARGET_FPS=30
FRAME_TIME= 1/TARGET_FPS
last_time = time.time()

class Vehicles:
    def __init__(self,x,y,type,color):
        self.x = x
        self.y = y
        self.type=type
        self.color=color

class Player:
    def __init__(self,x,y,type):
        self.x = x
        self.y = y
        self.type=type
class HealthPowerUp:
    def __init__(self,x,y):
        self.x=x
        self.y=y

health_lanes=[350,450]
health_powerup=HealthPowerUp(random.choice(health_lanes),random.randint(700,800))
   
def change_zone(x,y,z):
    if z== 0:
        return (x,y)    
    elif z==1:
        return (y,x)
    elif z==2:
        return (y,-x)    
    elif z==3:
        return (-x,y)
    elif z==4:
        return (-x,-y)    
    elif z==5:
        return (-y,-x)
    elif z==6:
        return (-y,x)  
    elif z==7:
        return (x,-y)
def original_zone(x, y, z):
    if z==0:
        return (x,y)    
    elif z==1:
        return (y,x)    
    elif z==2:
        return (-y,x)    
    elif z==3:
        return (-x,y)    
    elif z==4:
        return (-x,-y)    
    elif z==5:
        return (-y,-x)    
    elif z==6:
        return (y,-x)    
    elif z==7:
        return (x,-y)

def midpoint_line_drawing_algorithm(x1,y1,x2,y2,stroke_thickness=2):
    z=0
    dy=y2-y1
    dx=x2-x1
    if abs(dy)<abs(dx):
        if dx>=0 and dy>=0:
            z=0
        elif dx>=0 and dy<0:
            z=7        
        elif dx<0 and dy<0:
            z=4
        elif dx<0 and dy>=0:
            z=3
    else:
        if dx>=0 and dy>=0:
            z=1
        elif dx<0 and dy>=0:
            z=2
        elif dx<0 and dy<0:
            z=5
        elif dx>=0 and dy<0:
            z=6

    x1,y1=change_zone(x1,y1,z)
    x2,y2=change_zone(x2,y2,z)
    dy=y2-y1
    dx=x2-x1 
    increment_east=2*dy
    inc_northeast=2*(dy-dx)
    d=2*dy-dx
    x0,y0=original_zone(x1,y1,z)
    create_pixel(x0, y0,stroke_thickness)
    while x1<x2:
        if d>0:
            d+=inc_northeast
            x1+=stroke_thickness
            y1+=stroke_thickness
        else:
            d+=increment_east
            x1+=stroke_thickness
        x0,y0=original_zone(x1,y1,z)           
        create_pixel(x0, y0,stroke_thickness)

def create_midpoint_circle(r, x_main, y_main,stroke_thickness=2):
    x=0
    y=r
    d=1-r
    while y>x:
        create_pixel(x+x_main,y_main+y,stroke_thickness)
        create_pixel(y+x_main,y_main-x,stroke_thickness)
        create_pixel(x_main-y,y_main+x,stroke_thickness)
        create_pixel(x_main-y,-x+y_main,stroke_thickness)
        create_pixel(x+x_main,-y+y_main,stroke_thickness)
        create_pixel(x_main-x,y+y_main,stroke_thickness)
        create_pixel(x_main-x,y_main-y,stroke_thickness)
        create_pixel(y+x_main,x+y_main,stroke_thickness)
        if d<0:
            d+=2*x+3
        else:
            d+=5+2*x-2*y
            y=y-1
        x=x+1
def create_pixel(x,y,size=2): 
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()

def draw_car(x,y,color,main_player=False):
    if main_player:
        color=[1,0,0]

    # head_lights
    glColor3fv([color[0]*0.3,color[1]*0.3,color[2]*0.3])
    midpoint_line_drawing_algorithm(x-24,y+56,x+14,y+56,2)
    midpoint_line_drawing_algorithm(x-24,y+58,x+14,y+58,2)
    glColor3fv(color)
    for i in range(-20,20,10):
        midpoint_line_drawing_algorithm(x+i,y-10,x+i,y+45,10) #body

    glColor3fv(color)
    midpoint_line_drawing_algorithm(x-15,y+55,x+5,y+55,5) 
    if main_player:
        glColor3fv([1,1,1])
        midpoint_line_drawing_algorithm(x-7,y+53,x-7,y-10,7) #stripe
    else:
        glColor3fv([1,1,0])
        create_pixel(x-5,y+55,5)
    #windsheild
    glColor3fv([0.1,0.1,0.1])
    midpoint_line_drawing_algorithm(x-23,y+35,x+12,y+35,5)
    midpoint_line_drawing_algorithm(x-15,y+40,x+5,y+40,5)

    #windows
    midpoint_line_drawing_algorithm(x-23,y+25,x-23,y+19,5)
    midpoint_line_drawing_algorithm(x+12,y+25,x+12,y+19,5)

    midpoint_line_drawing_algorithm(x-23,y+8,x-23,y,5)
    midpoint_line_drawing_algorithm(x+12,y+8,x+12,y,5)

    #tail_lights
    glColor3fv([0.8,0,0])
    midpoint_line_drawing_algorithm(x-20,y-13,x-15,y-13,5)
    midpoint_line_drawing_algorithm(x+2,y-13,x+7,y-13,5)
    

def draw_bike(x,y,color,main_player=False):
    if main_player:
        color=[1,0,0]

    #bike
    glColor3fv(color)   
    midpoint_line_drawing_algorithm(x,y-20,x,y+30,10)
    midpoint_line_drawing_algorithm(x,y+24,x-15,y+22,4) #handle
    midpoint_line_drawing_algorithm(x,y+24,x+15,y+22,4)
    midpoint_line_drawing_algorithm(x,y-25,x,y-25,12) 
    glColor3fv([0.8,0,0])
    midpoint_line_drawing_algorithm(x,y-27,x,y-27,8) #taillight
    glColor3fv([0.7,0.7,0]) #headlight
    midpoint_line_drawing_algorithm(x,y+35,x,y+35,8)
    #driver
    if main_player:
        glColor3fv([0.8,0.7,0.7])
    else:
        glColor3fv([0.7,0.7,0.7]) #body
    midpoint_line_drawing_algorithm(x,y-10,x,y+10,10)

    midpoint_line_drawing_algorithm(x,y,x-15,y+22,4) #hands
    midpoint_line_drawing_algorithm(x,y,x+15,y+22,4)

    midpoint_line_drawing_algorithm(x-5,y-10,x-5,y-15,4) #legs
    midpoint_line_drawing_algorithm(x+5,y-10,x+5,y-15,4)

    glColor3fv([0.7,0.7,0.7])
    create_midpoint_circle(6,x,y+15,5) #head
    glColor3fv([0.9,0.9,0.9])
    create_midpoint_circle(4,x,y+15,5)



def draw_truck(x,y,color):

    #head
    glColor3fv([0.8,0.8,0.8])
    midpoint_line_drawing_algorithm(x-10,y+40,x+10,y+40,20)
    midpoint_line_drawing_algorithm(x-10,y+40,x+10,y+50,20) 
    glColor3fv([0.5,0.5,0.5])
    midpoint_line_drawing_algorithm(x-18,y+51,x+16,y+51,5)
    # head_lights
    glColor3fv([0.8,0.8,0])
    midpoint_line_drawing_algorithm(x-15,y+50,x-10,y+50,5)
    midpoint_line_drawing_algorithm(x+15,y+50,x+10,y+50,5)

    #body
    glColor3fv(color)
    for i in range(-20,21,10):
        midpoint_line_drawing_algorithm(x+i,y-45,x+i,y+20,10)
    glColor3fv([color[0]*0.6,color[1]*0.6,color[2]*0.6])
    midpoint_line_drawing_algorithm(x-15,y-45,x+15,y-45,10)
    glColor3fv([0.8,0,0]) #taillight
    midpoint_line_drawing_algorithm(x-20,y-48,x-15,y-48,5)
    midpoint_line_drawing_algorithm(x+20,y-48,x+15,y-48,5)

          
def set_background_color():
    glClearColor(0.2, 0.2, 0.27176, 0)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3fv([0.2,0.62,0.1])

    midpoint_line_drawing_algorithm(screen_x-60,60,screen_x-60,screen_y-120,120)
    midpoint_line_drawing_algorithm(60,60,60,screen_y-120,120)
    # print("test")


def Collision(obs,player):
    if player.type=="bike":
        playerlow_x= player.x-10
        playerhi_x=player.x +10
        playerlow_y=player.y-20     #player bounding box
        playerhi_y=player.y+55
    else:
        playerlow_x= player.x-15
        playerhi_x=player.x+15
        playerlow_y=player.y-20     #player bounding box
        playerhi_y=player.y+55
    # print(obs.x)
    obstacle_min_x=obs.x-25
    obstacle_max_x=obs.x+25
    obstacle_min_y=obs.y-20    # obstacle bounding box
    obstacle_max_y=obs.y+55

    if playerhi_x>=obstacle_min_x and playerlow_x<=obstacle_max_x:
        if playerhi_y>=obstacle_min_y and playerlow_y<=obstacle_max_y:
            return True
    return False


def draw_vehicles(vehicles,ismain_player=False):
    if isinstance(vehicles, list):
        for v in vehicles:

            if v.type=="car":
                draw_car(v.x,v.y,v.color,ismain_player)
            elif v.type=="bike":
                draw_bike(v.x,v.y,v.color,ismain_player)
            elif v.type=="truck":
                draw_truck(v.x,v.y,v.color)
    else:
        # print(vehicles)
        if vehicles.type=="car":
            draw_car(vehicles.x,vehicles.y,[1,0,0],ismain_player)
        elif vehicles.type=="bike":
            draw_bike(vehicles.x,vehicles.y,[1,0,0],ismain_player)

vehicle=[]
lanes_spacing=150

def spawn_new_vehicle(n=1):
    global vehicle,lanes,lanes_spacing

    for _ in range(n):
        ymax=0
        color=[[0.8,0.8,0],[0.8,0.8,0.8],[0.8,0,0.8],[0,0.8,0.8],[0,0.8,0],[0,0.8,0]]
        color=random.choice(color)
        xcor=random.choice(lanes)
        vehicle_type=random.choice(["car","bike","truck"])
        if not vehicle:
            vehicle.append(Vehicles(xcor,random.randint(600,800),vehicle_type,color))
        for v in vehicle:
            
            if v.y>ymax:
                ymax=v.y
        color=[[0.8,0.8,0],[0.8,0.8,0.8],[0.8,0,0.8],[0,0.8,0.8],[0,0.8,0],[0,0.8,0]]
        color=random.choice(color)
        xcor=random.choice(lanes)
        vehicle_type=random.choice(["car","bike","truck","car","car"])
        vehicle.append(Vehicles(xcor,random.randint(int(ymax)+200,int(ymax)+300),vehicle_type,color))        
        # if 900>ymax>=700:
        #     vehicle.append(Vehicles(xcor,random.randint(1000,1200),vehicle_type,color))
        # elif 1100>ymax>=900:
        #     vehicle.append(Vehicles(xcor,random.randint(1200,1400),vehicle_type,color))
        # elif 1300>ymax>=1100:
        #     vehicle.append(Vehicles(xcor,random.randint(1400,1600),vehicle_type,color))
        # elif 1500>ymax>=1300:
        #     vehicle.append(Vehicles(xcor,random.randint(1600,1800),vehicle_type,color))
        # elif 1700>ymax>=1500:
        #     vehicle.append(Vehicles(xcor,random.randint(1800,2000),vehicle_type,color))
        # elif 1900>ymax>=1700:
        #     vehicle.append(Vehicles(xcor,random.randint(2000,2200),vehicle_type,color))


        # for _ in vehicle:
        #     print(_.y)
        # print("ok")

            
           
spawn_new_vehicle(7) #initial spawning
# main_player=[]
main_player=Player(300,50,"car")#main player setup


def text_generator (x,y,text,font):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))

hit_time=0
health_time=0
def update_game_animation():
    global last_time,vehicle,speed, main_player,gameover,is_paused, chances_life, hit_time, score, highscore, health_time, hit_time, health_powerup_falling,health_powerup, health_lanes
    current_time=time.time()
    elapsed_time=current_time-last_time

    if elapsed_time >= FRAME_TIME:
        last_time = current_time

        health_time+=1

        if not is_paused:
            for v in vehicle:
                if Collision(v,main_player)==True:
                    chances_life-=1
                    hit_time = 30
                    # print("coll")
                    # print(chances_life)
                    if chances_life==0:
                        # print("game over")
                        gameover=True
                        is_paused=True
                        if score>highscore:
                            highscore=score
                    else:
                        vehicle.remove(v)
                        spawn_new_vehicle()
                else:
                    if score<5:
                        multiplier=1
                    elif 5<=score<25:
                        multiplier=score/5
                    else:
                        multiplier=6
                    
                    v.y-=speed*multiplier
                    if v.y<=-100:
                        vehicle.remove(v)
                        spawn_new_vehicle()
                        score+=1
            if health_powerup_falling:
                health_powerup.y-=speed*multiplier
                if Collision(health_powerup,main_player)==True:
                    chances_life+=1
                    health_powerup=HealthPowerUp(random.choice(health_lanes),random.randint(700,800))
                    health_powerup_falling=False
                    health_time=0
                if health_powerup.y<-20:
                    health_powerup_falling=False
                    health_powerup=HealthPowerUp(random.choice(health_lanes),random.randint(700,800))
                    health_time=0
        if hit_time>0:
            glColor3f(1,1,1)
            text_generator (main_player.x+20, main_player.y+15, "!!!!!!", GLUT_BITMAP_HELVETICA_18)
            hit_time-=1
            glutSwapBuffers()

    glutPostRedisplay()
    

def mouseListener(button,state,x,y):
    global is_paused,main_player,highscore, score

    if button==GLUT_LEFT_BUTTON and state==GLUT_DOWN:
            cursor_x=x
            cursor_y=screen_y-y  
            print(f"clicked ({cursor_x},{cursor_y})")
            if 490<cursor_x<512 and 629>cursor_y>610:
                print("game exiting")
                glutLeaveMainLoop()
            elif 520<cursor_x<548 and 629>cursor_y>610:
                if not gameover:
                    if is_paused:
                        is_paused=False
                        print("game resumed")
                    else:
                        is_paused=True
                    print("game paused")
            elif 550<cursor_x<580 and 629>cursor_y>610:
                print("game restarted")
                if highscore<score:
                    highscore=score
                restart()
            elif 480<cursor_x<600 and 120>cursor_y>70:
                if main_player.type=="bike":
                    main_player.type="car"
                else:
                    main_player.type="bike"


def keyboardListener(key,x,y):
    global main_player
    if not is_paused:
        if key==b'd': 
            if main_player.x<screen_x-180:  
                main_player.x+=40

        elif key==b'a': 
            if main_player.x>180:
                main_player.x-=40

        elif key==b's': 
            if main_player.y>60: 
                main_player.y-=40

        elif key==b'w': 
            if main_player.y<screen_y-260: 
                main_player.y+=40


# # Draw pause icon
def pause_menu(x,y,size):
        #pause
    glColor3f(0.2,0.6,0.9)    
    bar_width=size/4
    spacing =bar_width / 2    
    midpoint_line_drawing_algorithm(x, y, x, y + size/1.5, bar_width)
    midpoint_line_drawing_algorithm(x+bar_width+spacing,y,x+bar_width+spacing,y+size/1.5,bar_width)
def play_menuu(x,y,size):
    #play
    glColor3f(1,1,0.2)
    midpoint_line_drawing_algorithm(x, y, x, y + size/1.5, size/4)
    midpoint_line_drawing_algorithm(x, y, x+size/1.5, y+size/3, size/8)
    midpoint_line_drawing_algorithm(x, y+size/1.1, x + size/1.5, y+size/3, size/8)

def draw_menu_icons(x,y,size):
    global is_paused
    if is_paused:
        play_menuu(x,y,size)
    else:
        pause_menu(x,y,size)
    
    # cross
    glColor3f(1,0.2,0.2)
    midpoint_line_drawing_algorithm(x-20,y+15,x-35,y,size/8)
    midpoint_line_drawing_algorithm(x-35,y+15,x-20,y,size/8)

    glColor3f(1,1,1)
    create_midpoint_circle(9,x+35,y+8,size/8)

    
def draw_health_plus(h):
    glColor3f(0.2,0.9,0.7)
    midpoint_line_drawing_algorithm(h.x,h.y,h.x,h.y+20,10)
    midpoint_line_drawing_algorithm(h.x-10,h.y+10,h.x+10,h.y+10,10)

# black box at the top
def status_bar():
    global highscore, score, chances_life
    glColor3f(0, 0, 0) 
    midpoint_line_drawing_algorithm(0,screen_y-30,screen_x,screen_y-30,60) #black box at the top
    glColor3f(1,1,1)
    text_generator (10,screen_y-40,f"Chances:{chances_life}",GLUT_BITMAP_TIMES_ROMAN_24)     # Health
    glColor3f(1,1,1)
    text_generator (5,10,f"Highscore:{highscore}",GLUT_BITMAP_HELVETICA_18)       # Highscore
    glColor3f(1,1,1)
    text_generator (260,screen_y-40,f"Score:{score}",GLUT_BITMAP_TIMES_ROMAN_24)            # Score 

    # Pause icon
    draw_menu_icons(screen_x-70,screen_y-40,20)

    #change car
    glColor3f(0.6,0.4,0.2)
    midpoint_line_drawing_algorithm(510,95,600,95,50)
    glColor3f(1,1,1)
    text_generator (510,100,f"Change",GLUT_BITMAP_HELVETICA_18)       # Current Car
    text_generator (510,80,f"Vehicle",GLUT_BITMAP_HELVETICA_18)  

############################################################################################################ 

def restart(): #need to fix this later so a fresh match starts
    global vehicle,main_player,gameover, is_paused, chances_life, score, health_powerup_falling, health_powerup, health_time
    vehicle=[]
    main_player=Player(300,50,main_player.type)
    gameover=False
    is_paused=False
    chances_life=3
    score=0
    health_powerup_falling=False
    health_powerup=HealthPowerUp(random.choice(health_lanes),random.randint(700,800))
    health_time=0
    spawn_new_vehicle(7)
    glutPostRedisplay()
##########################################################

#glui functions
def update_display():
    global health_powerup_falling
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_viewport()
    set_background_color()
    draw_vehicles(vehicle)
    draw_vehicles(main_player,True)
    
    if health_time>1000:
        health_powerup_falling=True
    
        draw_health_plus(health_powerup)

    status_bar()
            
    glutSwapBuffers()
def setup_viewport():
    global screen_y, screen_x
    glViewport(0, 0, screen_x, screen_y)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, screen_x, 0.0, screen_y, 0, 1.0) 
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
    
glutInit()
glutInitWindowSize(screen_x, screen_y)
glutInitWindowPosition(200,20)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutCreateWindow(b"Car Racer")

glutDisplayFunc(update_display)
glutIdleFunc(update_game_animation)
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)

glutMainLoop()
