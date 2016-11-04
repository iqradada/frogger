# Frogger is a game that has a 2D top-down environment. Use the ARROW KEYS to move
# 		Frogger in increments. Avoid getting hit by dangerous cars. Get across the river by 
# 		hopping on friendly turtles. Play against a friend (who uses ASWD keys) and race to
# 		get Frogger to the top of the screen!
# Summary: Use the arrows to get Frogger home safe. 
 

import simplegui 
import math 
import random

#canvas measurements
WIDTH = 800
HEIGHT = 600

#create global variables
score1 = 0
score2 = 0
points1 = 0
points2 = 0
level = 1
time = 0
lives1 = 3
lives2 = 3
status = ""
ride = [False, None]
flo = [False, None]
crash = [False, None]
winner = "Winner's Initials: "
winnerscore = 0
highscores = list([])
hs = False
screen = 0

#set speeds
car1v = [3, 0]
car2v = [-4, 0]
car3v = [-1, 0]
car4v = [-2, 0] 
car5v = [1, 0]
slow = [1, 0]
nslow = [-2, 0] 
med = [2.5, 0]
fast = [3, 0]
turtle2_vel = [-1, 0]
turtle3_vel = [-2, 0]



#angles for the frog image
RIGHT = math.pi
UP = (math.pi)/2
LEFT = 0
DOWN = -(math.pi)/2

#distance method checks if two sprites are touching *used later*
def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def format_time(t):
    global time
    minutes = t/600
    t = t%600
    seconds = t/10
    #t = t%10
    #tenths = t
    
    if seconds <10:
        sec = "0" + str(seconds)
    else:
        sec = seconds
    tim=  str(minutes) + ":" + str(sec) 
    #+ "."  + str(tenths)
    return tim

#store image information in a method for easy access
class ImageInfo:   
    def __init__(self, center, size, lifespan = None, animated = False):
        self.center = center
        self.size = size
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    
    def get_dim(self):
        return [self.center[0]+self.size[0]/2, self.center[1]+self.size[1]/2, self.center[0]-self.size[0]/2, self.center[1]-self.size[1]/2]

#create a class for frogs with parameters of position angle and image/imageinfo
class Frog:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = angle
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
       
    def update(self):
        #print "Vel: " + str(self.vel)
        #print "Before pos: " + str(self.pos)
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        #print "After pos: " + str(self.pos)
    def get_dim(self):
        return [(self.pos[0] + self.image_size[0]/2)-1, (self.pos[1]+self.image_size[1]/2)-1, self.pos[0]-self.image_size[0]/2, self.pos[1]-self.image_size[1]/2]
     
    #draw the frog	
    def draw(self,canvas):
        self.update()
        canvas.draw_image(self.image, [self.image_center[0]+self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)

# move the frog in increments the keydown handler & rotate it accordingly
def keydown(key):
    jumpx = frogger1.image_size[0]-10
    jumpy = frogger1.image_size[1]
    if key == simplegui.KEY_MAP['w']:
        frogger1.angle = UP
        frogger1.pos[1] -= jumpy
        hop.pause()
        hop.rewind()
        hop.play()
    if key == simplegui.KEY_MAP['s']:
        frogger1.angle = DOWN
        frogger1.pos[1] += jumpy
        hop.pause()
        hop.rewind()
        hop.play()
    if key == simplegui.KEY_MAP['d']:
        frogger1.angle = RIGHT
        frogger1.pos[0] += (jumpx)
        hop.pause()
        hop.rewind()
        hop.play()
    if key == simplegui.KEY_MAP['a']:
        frogger1.angle = LEFT
        frogger1.pos[0] -= (jumpx)
        hop.pause()
        hop.rewind()
        hop.play()
        
    jumpx = frogger2.image_size[0]-10
    jumpy = frogger2.image_size[1]
    if key == simplegui.KEY_MAP['up']:
        frogger2.angle = UP
        frogger2.pos[1] -= jumpy
        hop.pause()
        hop.rewind()
        hop.play()
    if key == simplegui.KEY_MAP['down']:
        frogger2.angle = DOWN
        frogger2.pos[1] += jumpy
        hop.pause()
        hop.rewind()
        hop.play()
    if key == simplegui.KEY_MAP['right']:
        frogger2.angle = RIGHT
        frogger2.pos[0] += (jumpx)
        hop.pause()
        hop.rewind()
        hop.play()
    if key == simplegui.KEY_MAP['left']:
        frogger2.angle = LEFT
        frogger2.pos[0] -= (jumpx)
        hop.pause()
        hop.rewind()
        hop.play()

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, flowered):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.flowered = flowered
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0  
    
    def draw(self, canvas): 
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    def update(self):
        self.age += 1
        
        if self.pos[0]>WIDTH or self.pos[0]<0:
            self.pos[0] = self.pos[0] % WIDTH
            
        if self.pos[1]>HEIGHT or self.pos[1]<0:
            self.pos[1] = self.pos[1] % HEIGHT
        
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        if self.age >= self.lifespan:
            return True
        else:
            return False
        
    def get_flowered(self):
        return self.flowered
    def get_dim(self):
        return [(self.pos[0] + self.image_size[0]/2)-1, (self.pos[1]+self.image_size[1]/2)-1, self.pos[0]-self.image_size[0]/2, self.pos[1]-self.image_size[1]/2]
        
    def sprites_collide(self, other):
        if (dist(self.pos, other.pos) <= self.radius + other.radius):
            return True

def rect_collide(obj1, obj2):
    o1 = obj1.get_dim() 
    o2 = obj2.get_dim()
    return not (o1[0]<o2[2] or o1[2]>o2[0] or o1[3]>o2[1] or o1[1]<o2[3])
    
def collide(player, sprite):
    return rect_collide(player, sprite)

def group_collide(group, other): 
    for obj in group:
        if (collide(other, obj)): 
            return [True, obj]
    return [False, None]  

def process_sprite_group(spriteset, canvas):
    for s in spriteset:
        s.update()
        s.draw(canvas)

def update_sprite_group(spriteset, canvas):
    for s in spriteset:
        s.update() 
        
#create turtle and add them to sets             
def spawn_turtles():
    global turtle2_vel, turtle3_vel
    turtle2y = 80
    turtle3y = 160 
    posx = WIDTH    
    x = 0
    
    while x<=7:
        if x==0 or x==4:
            #posx += 10
            new_turtle = Sprite([posx, turtle2y], turtle2_vel, LEFT, 0, clearturtle, iturtle, True)
            turtles_under.add(new_turtle)
            new_turtle = Sprite([posx, turtle2y], turtle2_vel, LEFT, 0, everything, turtle_open, False)
            turtles.add(new_turtle)
            posx += 40
            
            new_turtle = Sprite([posx, turtle2y], turtle2_vel, LEFT, 0, clearturtle, iturtle, True)
            turtles_under.add(new_turtle)
            new_turtle = Sprite([posx, turtle2y], turtle2_vel, LEFT, 0, everything, turtle_open, False)
            turtles.add(new_turtle)
            posx += 150
            
        else:
            #posx += 10
            new_turtle = Sprite([posx, turtle2y], turtle2_vel, LEFT, 0, everything, turtle_open, False)
            turtles_under.add(new_turtle)
            new_turtle = Sprite([posx, turtle2y], turtle2_vel, LEFT, 0, everything, turtle_open, False)
            turtles.add(new_turtle)
            posx += 40
            
            new_turtle = Sprite([posx, turtle2y], turtle2_vel, LEFT, 0, everything, turtle_open, False)
            turtles_under.add(new_turtle)
            new_turtle = Sprite([posx, turtle2y], turtle2_vel, LEFT, 0, everything, turtle_open, False)
            turtles.add(new_turtle)
            posx += 150
            
        x += 2
    
    
    x=0
    while x<=5:
        if x==0 or x==4:
            new_turtle = Sprite([posx, turtle3y], turtle3_vel, LEFT, 0, clearturtle, iturtle, True)
            turtles_under.add(new_turtle)
            new_turtle = Sprite([posx, turtle3y], turtle3_vel, LEFT, 0, everything, turtle_open, False)
            turtles.add(new_turtle)
            posx += 40
            
            new_turtle = Sprite([posx, turtle3y], turtle3_vel, LEFT, 0, clearturtle, iturtle, True)
            turtles_under.add(new_turtle)
            new_turtle = Sprite([posx, turtle3y], turtle3_vel, LEFT, 0, everything, turtle_open, False)
            turtles.add(new_turtle)
            posx += 40
            
            new_turtle = Sprite([posx, turtle3y], turtle3_vel, LEFT, 0, clearturtle, iturtle, True)
            turtles_under.add(new_turtle)
            new_turtle = Sprite([posx, turtle3y], turtle3_vel, LEFT, 0, everything, turtle_open, False)
            turtles.add(new_turtle)
            posx += 120
        
        else:
            new_turtle = Sprite([posx, turtle3y], turtle3_vel, LEFT, 0, everything, turtle_open, False)
            turtles_under.add(new_turtle)
            new_turtle = Sprite([posx, turtle3y], turtle3_vel, LEFT, 0, everything, turtle_open, False)
            turtles.add(new_turtle)
            posx += 40
            
            new_turtle = Sprite([posx, turtle3y], turtle3_vel, LEFT, 0, everything, turtle_open, False)
            turtles_under.add(new_turtle)
            new_turtle = Sprite([posx, turtle3y], turtle3_vel, LEFT, 0, everything, turtle_open, False)
            turtles.add(new_turtle)
            posx += 40
            
            new_turtle = Sprite([posx, turtle3y], turtle3_vel, LEFT, 0, everything, turtle_open, False)
            turtles_under.add(new_turtle)
            new_turtle = Sprite([posx, turtle3y], turtle3_vel, LEFT, 0, everything, turtle_open, False)
            turtles.add(new_turtle)
            posx += 120   
        x += 1 

#create log sprites and add them to a set
def spawn_logs():
    global slow, nslow, med
    log1y = 120
    log2y = 200
    log3y = 240 
    posx = WIDTH
    
    x=0    
    while x<=2:
        posx += 40
        new_log = Sprite([posx, log1y], slow, LEFT, 0, everything, log, False)
        logs.add(new_log)
        posx += 160
        x += 1     
    
    x=0
    while x<=2:
        posx += 10
        new_log = Sprite([posx, log2y], med, LEFT, 0, everything, log, False)
        logs.add(new_log)
        posx += 100
        x += 2    
    
    x=0
    while x<=4:
        new_log = Sprite([posx, log3y], nslow, LEFT, 0, everything, log, False)
        logs.add(new_log)
        posx += 40
        x += 1

#create car sprites and add them to a set
def spawn_cars():
    global car1v, car2v, car3v, car4v, car5v
    car1y = 320
    car2y = 360
    car3y = 400
    car4y = 440 
    car5y = 480
    
    posx = WIDTH
    
    x=0    
    while x<=4:
        posx += 120
        new_car = Sprite([posx, car1y], car1v, LEFT, 0, everything, car1, False)
        cars.add(new_car)
        posx += 100
        x += 1     
    x=0
    while x<=3:
        posx += 40
        new_car = Sprite([posx, car2y], car2v, LEFT, 0, everything, car2, False)
        cars.add(new_car)
        posx += 80
        x += 2    
    x=0
    while x<=2:
        posx += 120
        new_car = Sprite([posx, car3y], car3v, LEFT, 0, everything, car3, False)
        cars.add(new_car)
        posx += 360
        x += 1
    x=0
    while x <= 3:
        posx += 100
        new_car = Sprite([posx, car4y], car4v, LEFT, 0, everything, car4, False)
        cars.add(new_car)
        posx += 100
        x += 1
    x=0
    while x <= 4:
        posx += 40
        new_car = Sprite([posx, car5y], car5v, LEFT, 0, everything, car5, False)
        cars.add(new_car)
        posx += 160
        x += 1 
   
def click(pos):
    global started, splash, isplash, screen, hs
    d = isplash.get_dim()
 
    if ((screen == 0) and (pos[0] > 210 and pos[0] < 310) and (pos[1] > d[3]+290 and pos[1] < d[3]+400)):
        splash = simplegui.load_image("https://dl.dropbox.com/s/do69ygqdnuggjka/howtoplay1.png")
        
        screen = 1
        pass
        
    if ((screen == 0) and (pos[0] > 475 and pos[0] < 575) and (pos[1] > d[3]+290 and pos[1] < d[3]+400)):
        splash = simplegui.load_image("https://dl.dropbox.com/s/in6zc1a9ko3ylst/highscores2.png")  
        screen = 1
        hs = True
        
    
    if ((screen == 1) and  (pos[0] > 350 and pos[0] < 450) and (pos[1] > d[3]+390 and pos[1] < d[3]+440)):
        splash = simplegui.load_image("https://dl.dropbox.com/s/tyz3ew59ojimo60/splash1.png")
        hs = False
        soundtrack.pause()
        screen = 0
        
    
    if ((screen == 3) and  (pos[0] > 350 and pos[0] < 450) and (pos[1] > d[3]+390 and pos[1] < d[3]+440)):
        splash = simplegui.load_image("https://dl.dropbox.com/s/tyz3ew59ojimo60/splash1.png")
        soundtrack.pause()
        screen = 0
        
    
    if ((screen == 2) and  (pos[0] > 350 and pos[0] < 450) and (pos[1] > d[3]+390 and pos[1] < d[3]+440)):
        splash = simplegui.load_image("https://dl.dropbox.com/s/tyz3ew59ojimo60/splash1.png")
        soundtrack.pause()
        screen = 0
        
    
    if ((screen == 0) and (pos[0] > 350 and pos[0] < 450) and (pos[1] > d[3]+290 and pos[1] < d[3]+400)):
        refresh()
        started = True
        soundtrack.rewind()
        soundtrack.play()
        screen = 2
            
def flow(): 
    global time, screen
    if started:
        time += 1
    pass

def save_scores(s):
    global winnerscore, highscores
    highscores.append([winnerscore, s])
    print highscores

#def play_sounds():
#    global screen
#    loop = False    
#    while not loop and screen == 0:
#        start.pause()
#        start.rewind()
#        start.play()
#        loop = True
#    while not loop and screen == 1:
#        extra.pause()
#        extra.rewind()
#        extra.play()
#        loop = True
#    while not loop and screen == 2:
#        soundtrack.pause()
#        soundtrack.rewind()
#        soundtrack.play()
#        loop = True
#    while not loop and screen == 3:
#        tweener.pause()
#        tweener.rewind()
#        tweener.play()
#        loop = True 
        
    
def draw(canvas):
    global started, time, lives1, lives2, score1, score2, status, points1, points2, splash
    global car1v, car2v, car3v, car4v, car5v, turtle2_vel, turtle3_vel, slow, nslow, med
    global winnerscore, level, screen, hs, homes, homes_flowered
    #draw the backdrop 
    canvas.draw_image(backdrop, [400,300], [800,600], [400,300], [800,600])
    
    #play sounds
    if started == False:
        start.play()
        canvas.draw_image(splash, isplash.get_center(), isplash.get_size(), [WIDTH / 2, HEIGHT /2], isplash.get_size())
        refresh()
        
    if started == True:
        extra.pause()
        tweener.pause()
        start.pause()
        soundtrack.play()
        
        if time == 1980:
            soundtrack.pause()
            soundtrack.rewind()
            soundtrack.play()
        
        if time == 3960:
            soundtrack.pause()
            soundtrack.rewind()
            soundtrack.play()
        
        #Check if game is over    
        if lives2 == 0 or lives1 == 0:
            gameover()
        #draw all the sprites
        if time%100 < 40 or time%100 > 80:
            under = True
        else:
            under = False
        
        if under:
            process_sprite_group(turtles_under, canvas)
            update_sprite_group(turtles, canvas)
        else:
            process_sprite_group(turtles, canvas)
            update_sprite_group(turtles_under, canvas)
        
        process_sprite_group(logs, canvas)
        process_sprite_group(cars, canvas)
        process_sprite_group(homes, canvas)
        process_sprite_group(homes_flowered, canvas)
        
        #call the frog's draw method 
        frogger1.draw(canvas)
        frogger2.draw(canvas)
        
 
        #FROG 1 COLLISIONS
        #check if froggy is floating on logs 
        flo = group_collide(logs, frogger1)
        if flo[0]==True:
        #print "Flo: " + str(flo[1].vel)
            frogger1.vel[0] = flo[1].vel[0]
            frogger1.vel[1] = flo[1].vel[1]
            #print "After: " + str(frogger.vel)
            
        #check if froggy is riding turtles     
        if not under:      
            ride = group_collide(turtles, frogger1)
            if ride[0]==True:
                frogger1.vel[0] = ride[1].vel[0]
                frogger1.vel[1] = ride[1].vel[1]
        if under:      
            ride = group_collide(turtles_under, frogger1)
            if ride[0]==True:
                frogger1.vel[0] = ride[1].vel[0]
                frogger1.vel[1] = ride[1].vel[1]
                
        #check if froggy got hit by a car
        crash = group_collide(cars, frogger1)
        if crash[0]==True:
            frogger1.pos = [WIDTH/3, HEIGHT-80]
            frogger1.vel = [0, 0]
            lives2 -= 1
            squash.rewind()
            squash.play()
            
        #check if froggy got home
        safe = group_collide(homes, frogger1)
       
        #check if off screen 
        if frogger1.pos[0]<0 or frogger1.pos[0]>800 or frogger1.pos[1]<0 or frogger1.pos[1]>600:
            lives2 -= 1
            frogger1.pos = [WIDTH/3, HEIGHT-80]
            frogger1.vel = [0, 0]
            squash.pause()
            squash.rewind()
            squash.play()
            print "off screen"
        
        #lose a life if froggy isnt home safe, riding a log, or floating on a turtle 
        if frogger1.pos[1] < 264:
            if not (ride[0] or flo[0]): 
                frogger1.pos = [WIDTH/3, HEIGHT-80]
                frogger1.vel = [0, 0]
                if not safe[0]:
                    lives1 -= 1
                    squash.pause()
                    squash.rewind()
                    squash.play()
                    print "not riding log or turtle and not home safe"
                else:
                    score1 += 1
                    status1 = "Frogger1 is home safe!"
                    points1+= (5000 - time)
                    homey.pause()
                    homey.rewind()
                    homey.play()
                    homes_flowered.add(Sprite(safe[1].pos, safe[1].vel, safe[1].angle, safe[1].angle_vel, homepurple, ihome, True))
                    homes.remove(safe[1])
            if ride[0]:
                if (under and ride[1].flowered):
                    lives1 -= 1
                    frogger1.pos = [WIDTH/3, HEIGHT-80]
                    frogger1.vel = [0, 0]
                    squash.pause()
                    squash.rewind()
                    squash.play()
                    print "under and on submerged turtle"		

 
        #FROG 2 COLLISIONS
        #check if froggy is floating on logs 
        flo = group_collide(logs, frogger2)
        if flo[0]==True:
        #print "Flo: " + str(flo[1].vel)
            frogger2.vel[0] = flo[1].vel[0]
            frogger2.vel[1] = flo[1].vel[1]
            #print "After: " + str(frogger.vel)
            
        #check if froggy is riding turtles     
        if not under:      
            ride = group_collide(turtles, frogger2)
            if ride[0]==True:
                frogger2.vel[0] = ride[1].vel[0]
                frogger2.vel[1] = ride[1].vel[1]
        if under:      
            ride = group_collide(turtles_under, frogger2)
            if ride[0]==True:
                frogger2.vel[0] = ride[1].vel[0]
                frogger2.vel[1] = ride[1].vel[1]
                
        #check if froggy got hit by a car
        crash = group_collide(cars, frogger2)
        if crash[0]==True:
            frogger2.pos = [WIDTH*2/3, HEIGHT-80]
            frogger2.vel = [0, 0]
            lives2 -= 1
            squash.rewind()
            squash.play()
            
        #check if froggy got home
        safe2 = group_collide(homes, frogger2)
       
        #check if off screen 
        if frogger2.pos[0]<0 or frogger2.pos[0]>800 or frogger2.pos[1]<0 or frogger2.pos[1]>600:
            lives2 -= 1
            frogger2.pos = [WIDTH*2/3, HEIGHT-80]
            frogger2.vel = [0, 0]
            squash.pause()
            squash.rewind()
            squash.play()
            print "off screen"
        
        #lose a life if froggy isnt home safe, riding a log, or floating on a turtle 
        if frogger2.pos[1] < 264:
            if not (ride[0] or flo[0]): 
                frogger2.pos = [WIDTH*2/3, HEIGHT-80]
                frogger2.vel = [0, 0]
                if not safe2[0]:
                    lives2 -= 1
                    squash.pause()
                    squash.rewind()
                    squash.play()
                    print "not riding log or turtle and not home safe"
                else:
                    score2 += 1
                    status2 = "Frogger2 is home safe!"
                    points2+= (5000 - time)
                    homey.pause()
                    homey.rewind()
                    homey.play()
                    homes_flowered.add(Sprite(safe2[1].pos, safe2[1].vel, safe2[1].angle, safe2[1].angle_vel, homeyellow, ihome, True))
                    homes.remove(safe2[1])
            if ride[0]:
                if (under and ride[1].flowered):
                    lives2 -= 1
                    frogger2.pos = [WIDTH*2/3, HEIGHT-80]
                    frogger2.vel = [0, 0]
                    squash.pause()
                    squash.rewind()
                    squash.play()
                    print "under and on submerged turtle"
                    
        #draw info on screen
        canvas.draw_text("P1 Frogs Home: " + str(score1), [10, HEIGHT-40], 16, "Yellow", "sans-serif")
        canvas.draw_text("P2 Frogs Home: " + str(score2), [620, HEIGHT-40], 16, "Cyan", "sans-serif")
        canvas.draw_text("P1 Score: " + str(points1), [10, HEIGHT-22], 16, "Yellow", "sans-serif")
        canvas.draw_text("P2 Score: " + str(points2), [620, HEIGHT-22], 16, "Cyan", "sans-serif")
    
        canvas.draw_text("P1 Lives: " +str(lives1), [10, HEIGHT -4], 16, "Yellow", "sans-serif")     
        canvas.draw_text("P2 Lives: " +str(lives2), [620, HEIGHT -4], 16, "Cyan", "sans-serif")       
        canvas.draw_text("Time: " + format_time(time), [WIDTH/2, HEIGHT-20], 16, "BlueViolet", "sans-serif")
        canvas.draw_text(str(status), [WIDTH/3, HEIGHT-20], 16, "BlueViolet", "sans-serif")
        
        #Check if all homes are occupied - LEVEL UP            
        if (score1 + score2 == 6):
            level +=1
            status = "LEVEL" + str(level) + "!"
            score1 = 0
            score2 = 0
            
            homes = set([])
            homes_flowered = set([])
            new_home = Sprite([62, 42], [0, 0], UP, 0, homeclear, ihome, False)
            homes.add(new_home)
            new_home = Sprite([196, 42], [0, 0], UP, 0, homeclear, ihome, False)
            homes.add(new_home)
            new_home = Sprite([330, 42], [0, 0], UP, 0, homeclear, ihome, False)
            homes.add(new_home)
            new_home = Sprite([464, 42], [0, 0], UP, 0, homeclear, ihome, False)
            homes.add(new_home)
            new_home = Sprite([597, 42], [0, 0], UP, 0, homeclear, ihome, False)
            homes.add(new_home)
            new_home = Sprite([731, 42], [0, 0], UP, 0, homeclear, ihome, False)
            homes.add(new_home)
      
            frogger1.pos = [WIDTH/3, HEIGHT-80]
            frogger1.vel = [0, 0]
            frogger2.pos = [WIDTH*2/3, HEIGHT-80]
            frogger2.vel = [0, 0]
            pass
        
        #check level (speeds)
        if level == 2:
            car1v[0] *=2
            car2v[0] *=2
            car3v[0] *=2
            car4v[0] *=2 
            car5v[0] *=2
            slow[0] *=2
            nslow[0] *=2 
            med[0] *=2
            fast[0] *=2
            turtle2_vel[0] *=2
            turtle3_vel[0] *=2    
        if level == 3:
            car1v[0] *= 3/2
            car2v[0] *= 3/2
            car3v[0] *=3/2
            car4v[0] *=3/2
            car5v[0] *=3/2
            slow[0] *=3/2
            nslow[0] *=3/2
            med[0] *=3/2
            fast[0] *=3/2
            turtle2_vel[0] *=3/2
            turtle3_vel[0] *=3/2
        if level == 4:
            car1v[0] *= 4/3
            car2v[0] *= 4/3
            car3v[0] *= 4/3
            car4v[0] *= 4/3 
            car5v[0] *= 4/3
            slow[0] *= 4/3
            nslow[0] *= 4/3 
            med[0] *= 4/3
            fast[0] *= 4/3
            turtle2_vel[0] *= 4/3
            turtle3_vel[0] *= 4/3            
    
    #If the high scores screen is up, print the high scores    
    if screen == 1 and hs == True:
        
        highscores.sort()
        highscores.reverse()
        while len(highscores) > 5:
            highscores.pop(-1)    
        p_score = 265
        p_name = 500
        h = 270
        for g in highscores:
            canvas.draw_text(str(g[0]), [p_score, h], 16, "Violet", "monospace")
            canvas.draw_text(str(g[1]), [p_name, h], 16, "Violet", "monospace")
            h += 30
    
        
        
def refresh():
    global started, time, lives1, lives2, score1, score2, status, points1, points2, winnerscore
    score1=0
    score2=0
    lives1=3
    lives2=3
    time = 0
    level = 1
    winnerscore=0
    points1 =0
    points2=0
    homes = set([])
    
    homes_flowered = set([])
    new_home = Sprite([62, 42], [0, 0], UP, 0, homeclear, ihome, False)
    homes.add(new_home)
    new_home = Sprite([196, 42], [0, 0], UP, 0, homeclear, ihome, False)
    homes.add(new_home)
    new_home = Sprite([330, 42], [0, 0], UP, 0, homeclear, ihome, False)
    homes.add(new_home)
    new_home = Sprite([464, 42], [0, 0], UP, 0, homeclear, ihome, False)
    homes.add(new_home)
    new_home = Sprite([597, 42], [0, 0], UP, 0, homeclear, ihome, False)
    homes.add(new_home)
    new_home = Sprite([731, 42], [0, 0], UP, 0, homeclear, ihome, False)
    homes.add(new_home)
    
    frogger1.pos = [WIDTH/3, HEIGHT-80]
    frogger1.vel = [0, 0]
    frogger2.pos = [WIDTH*2/3, HEIGHT-80]
    frogger2.vel = [0, 0]
    
def newgame():
    global started, time, lives1, lives2, score1, score2, status, points1, points2, splash
    global winnerscore, homes, homes_flowered, screen, frogger1, frogger2, turles, logs, cars
    score1=0
    score2=0
    lives1=3
    lives2=3
    time = 0
    winnerscore=0
    points1 =0
    points2=0
    started = False
    screen = 0    
    frogger1 = Frog([WIDTH/3, HEIGHT-80], [0,0], UP, everything, f_jump1)
    frogger2 = Frog([WIDTH*2/3, HEIGHT-80], [0,0], UP, everything, f_jump2)
    turtles = set([])
    logs = set([])
    cars = set([])
    homes = set([])
    homes_flowered = set([])
    new_home = Sprite([62, 42], [0, 0], UP, 0, homeclear, ihome, False)
    homes.add(new_home)
    new_home = Sprite([196, 42], [0, 0], UP, 0, homeclear, ihome, False)
    homes.add(new_home)
    new_home = Sprite([330, 42], [0, 0], UP, 0, homeclear, ihome, False)
    homes.add(new_home)
    new_home = Sprite([464, 42], [0, 0], UP, 0, homeclear, ihome, False)
    homes.add(new_home)
    new_home = Sprite([597, 42], [0, 0], UP, 0, homeclear, ihome, False)
    homes.add(new_home)
    new_home = Sprite([731, 42], [0, 0], UP, 0, homeclear, ihome, False)
    homes.add(new_home)
    spawn_turtles()
    spawn_logs()
    spawn_cars()
    
def gameover(): 
    global winner, winnerscore, splash, screen, started, points1, points2
    soundtrack.pause()
    extra.rewind() 
    #extra.play()
    if points1>points2:
        splash = simplegui.load_image("https://dl.dropbox.com/s/jtbgl4u2wyl1adn/gameover1.png")
        winnerscore = points1
        save_scores(winnerscore)
        winner = "P1 Initials"
        label.set_text(winner)
        screen = 3
        pass
                
    elif points2 > points1:
        splash = simplegui.load_image("https://dl.dropbox.com/s/5oqoayb066yqros/gameover2.png")             
        winnerscore = points2
        winner = "P2 Initials"
        label.set_text(winner)
        screen = 3
        pass
    else:
        splash = simplegui.load_image("https://dl.dropbox.com/s/4t9i52y8rfh7rxz/gameover.png")             
        winner = "TIE- P1 & P2 Initials"
        winnerscore = points1
        label.set_text(winner)
        screen = 3
        pass
    started = False
    
#load sprite sheet and backdrop   
everything = simplegui.load_image("https://dl.dropbox.com/s/mhlkyrm1uk7q9mk/froggersprites4.png")
backdrop = simplegui.load_image("https://dl.dropbox.com/s/ng5xg8uvp7v4vaz/Frogger%20Background3.png")
homeclear = simplegui.load_image("https://dl.dropbox.com/s/dhyp6yhnxaf89nv/homeclear.png")
homeyellow = simplegui.load_image("https://dl.dropbox.com/s/jnp5xhj0oc3fqb7/homepurple.png")
homepurple = simplegui.load_image("https://dl.dropbox.com/s/l8on6tptertnk2s/homeyellow.png")
splash = simplegui.load_image("https://dl.dropbox.com/s/tyz3ew59ojimo60/splash1.png")
#gameover = simplegui.load_image("https://dl.dropbox.com/s/4t9i52y8rfh7rxz/gameover.png")
clearturtle = simplegui.load_image("https://dl.dropbox.com/s/5ipn6hi52mc3aae/empty40-40.png")

#load sounds
hop = simplegui.load_sound("https://dl.dropbox.com/s/t2rgb0kuzht93cp/dp_frogger_hop.mp3")
start = simplegui.load_sound("https://dl.dropbox.com/s/o102okw8mf606p6/dp_frogger_start.mp3")
tweener = simplegui.load_sound("https://dl.dropbox.com/s/iyk1xe40u2ls68y/dp_frogger_tweener.mp3")
squash = simplegui.load_sound("https://dl.dropbox.com/s/ivb168rlsnkbdk9/dp_frogger_squash.mp3")
homey = simplegui.load_sound("https://dl.dropbox.com/s/mgxtw6qfst9tuyk/dp_frogger_coin.mp3")
extra = simplegui.load_sound("https://dl.dropbox.com/s/sbrcsjnvnpmnln3/dp_frogger_extra.mp3")
soundtrack = simplegui.load_sound("https://dl.dropbox.com/s/gnrkzsvldqot4wq/1D%20-%20Instrumental.mp3")

#define images from sprite sheet 
f_reg1 = ImageInfo([350, 60], [40, 40])       
f_jump1 = ImageInfo([220, 60], [40, 40])
f_reg2 = ImageInfo([350, 150], [40, 40])       
f_jump2 = ImageInfo([220, 150], [40, 40])
turtle_open = ImageInfo([160, 385], [40, 40])
log = ImageInfo([1280, 795], [120, 40])
car1 = ImageInfo([301, 874], [40, 40])
car2 = ImageInfo([245, 873], [40, 40])
car3 = ImageInfo([163, 873], [80, 40])
car4 = ImageInfo([79, 873], [40, 40])
car5 = ImageInfo([20, 873], [40, 40])
ihome = ImageInfo([15, 15], [30, 30])
isplash = ImageInfo([215, 141], [430, 282])
iturtle = ImageInfo([20, 20], [40, 40])


# initialize frame
frame = simplegui.create_frame("Frogger", WIDTH, HEIGHT)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
l1 = frame.add_label("The goal is to get as many points as possible.")
l2 = frame.add_label("When all homes are occupied, the level of difficulty increases.")
l3 = frame.add_label("Enjoy the game!")
l4 = frame.add_label(" ")
label = frame.add_input(winner, save_scores, 100)
timer = simplegui.create_timer(100, flow)

#variable
points1 =0
points2=0
started = False
screen = 0    
frogger1 = Frog([WIDTH/3, HEIGHT-80], [0,0], UP, everything, f_jump1)
frogger2 = Frog([WIDTH*2/3, HEIGHT-80], [0,0], UP, everything, f_jump2)
turtles = set([])
turtles_under = set([])
logs = set([])
cars = set([])
homes = set([])
homes_flowered = set([])


# get things rolling
frame.start()
newgame()
#play_sounds()
timer.start()

