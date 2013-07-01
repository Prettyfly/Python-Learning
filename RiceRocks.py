# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
spaceship_speed = 0.15
friction = 0.99 # friction multiple
missile_vel = 10
rock_group = set([])
missile_group = set([])
explosion_group = set([])
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 48, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def random_velocity():
    angle = 2 * math.pi * random.random()   
    vector = angle_to_vector(angle)
    vel = [random.random() * vector[0], random.random() * vector[1]]
    return vel
    
def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)
 
# Ship class
class Ship:
    thrust = False
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
    
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, (self.image_center[0] * 3, self.image_center[1]), self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def shoot(self):
        global a_missile
        missile_group.add(Sprite([self.pos[0] + self.forward[0] * self.radius, self.pos[1] + self.forward[1] * self.radius],
                                 [self.vel[0] + (self.forward[0] * 4), self.vel[1] + (self.forward[1] * 4)],
                                 0, 0, missile_image, missile_info, missile_sound))
        missile_sound.play()
        
    def sound(self):
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
            
    
    def update(self):
        self.forward = angle_to_vector(self.angle)
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.vel[0] *= friction
        self.vel[1] *= friction      
        
        self.sound()
        
        if self.thrust:
            self.vel[0] += spaceship_speed * self.forward[0] 
            self.vel[1] += spaceship_speed * self.forward[1] 
        else:
            ship_thrust_sound.pause()
            
    
    
# Sprite class
class Sprite:
    age = 0
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        
        if sound:
            sound.rewind()
            sound.play()
   
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
    
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, (self.image_center[0] * self.age, self.image_center[1]), self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel       
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 1
        if self.age > self.lifespan:
            return True
        else:
            return False
    
    def collide(self, other_object):
        distance = dist(self.get_position(), other_object.get_position())
        if distance > self.get_radius() + other_object.get_radius():
            return False
        else:
            return True
        
def process_sprite_group(group, canvas):
    for sprite in set(group):
        sprite.update()
        sprite.draw(canvas)
        if sprite.update() == True:
            group.remove(sprite)
              
def group_collide(group, other_object):
    collisions_count = 0
    for sprite in set(group):
        if sprite.collide(other_object):
            group.remove(sprite)
            explosion_group.add(Sprite(sprite.get_position(),[0,0] , 0, 0, explosion_image, explosion_info))
            collisions_count += 1
    return collisions_count

def group_group_collide(group, other_group):
    hits = 0
    for item in set(group):
        if group_collide(other_group, item) > 0:
            group.remove(item)
            hits += 1
    return hits
            
def draw(canvas):
    global time, lives, score, rock_group, started
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])
    canvas.draw_text("Lives " + str(lives) , (WIDTH - 100, HEIGHT - .9 * HEIGHT), 18, "White")
    canvas.draw_text("Scores " + str(score), (WIDTH - 100, HEIGHT - .95 * HEIGHT), 18, "White")
      
    # draw ship and sprites
    my_ship.draw(canvas)
       
    # update ship and sprites
    my_ship.update()
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
     
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        score = 0
        lives = 3
        rock_group = set([])
    
    if lives <= 0:
        started = False
        
    
    
    lives -= group_collide(rock_group, my_ship)
    score += group_group_collide(rock_group, missile_group)
    
    
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
    
def keydown(key):
    
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
    if key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = 0.1
    elif key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel = -0.1 
    if key == simplegui.KEY_MAP['space']:
        my_ship.shoot()

def keyup(key):
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False
    if key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel = 0
    
        
# timer handler that spawns a rock    
def rock_spawner():
    if len(rock_group) < 12 and started:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)] 
        new_rock = (Sprite(rock_pos, random_velocity(), 0, (random.random() - .5) * 0.3 , asteroid_image, asteroid_info))  
        if not new_rock.collide(my_ship):
            rock_group.add(new_rock)
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
my_ship.update()
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
