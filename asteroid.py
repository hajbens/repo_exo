from if3_game.engine import Sprite, Game, Layer, Text
from random import randint
from pyglet import window, font
from math import cos, sin, radians


#spaceItem est le fichier asteroide modifié

RESOLUTION = (800, 600)
# en majuscule car c'est une constante
#c'est une variable avec un tuple 


class AsteroidGame(Game):
    
    def __init__ (self):
        super().__init__()

        font.add_file ("fonts/Sunny April.ttf")

        self.bg_layer = Layer()
        self.add(self.bg_layer)

        self.game_layer = Layer()
        self.add(self.game_layer)

        self.ui_layer = UILayer()
        self.add(self.ui_layer)

        # créer les éléments de jeu

        position = (RESOLUTION [0] / 2 , RESOLUTION [1] / 2 )
        self.spaceship = Spaceship(position)

        self.game_layer.add(self.spaceship)
        self.ui_layer.spaceship = self.spaceship


        for n in range(3):
            x = randint (0, RESOLUTION[0])
            y = randint (0, RESOLUTION[1])

            position = (x,y)

            sx = randint (-300,300)
            sy = randint (-300,300)

            speed = (sx, sy)

            asteroid = Asteroid (position, speed)
            self.game_layer.add(asteroid)

# créer les élément de background

        bg = Sprite ("images/bg_1.gif", (0,0), scale = 2)
        #self.scale += 2
        self.bg_layer.add(bg)


class UILayer(Layer):

    def __init__ (self):

        super().__init__()

        #text = Text ("GAME OVER !!! " , (400,560), 36 , anchor = "center", font_name = "Sunny April")
        #self.add(text)
        self.spaceship = None
        self.lifes = []

        for n in range(3):
            x = 730 + n * 24
            y = 580 
            
            image = "images/life.png"
            position = (x,y)
            anchor = (8 , 8)
            

            """""sprite = Sprite (image, position, scale = 2 , anchor = anchor)"""

            sprite = Sprite (image, position, anchor = anchor)
            self.add(sprite)

            self.lifes.append(sprite)
        
    def update (self, dt):
        super().update(dt)
        
        
        for index in range (len(self.lifes)):
            if index < self.spaceship.life:
                self.lifes[index].opacity = 255
                

            else :
                self.lifes[index].opacity = 0
        
        if self.spaceship.life <= 0:
            text = Text ("GAME OVER !!! " , (400,300), 72 , anchor = "center", font_name = "Sunny April", color=  (154, 56, 114) )
            self.add(text)





class SpaceItem(Sprite):

    def __init__(self, image, position, anchor, speed = (0,0), rotation_speed=0): # si on met 0,0 à speed , ça signifie que sa vitesse est de 0 si on la spécifie pas
        super().__init__(image, position, anchor = anchor, collision_shape="circle")
        self.speed = speed
        #pour que la rotation devienne un attribut:
        self.rotation_speed = rotation_speed

    #dt = delta time = difference, écart de temps depuis la dernière fois qu'on a appelé l'update= ecart entre deux frame
    def update (self,dt):
        super().update(dt)
        #position actuelle
        pos_x = self.position [0] # position en x
        pos_y = self.position [1] # position en y
        
        # calcul le déplacement
        move = (self.speed [0]* dt , self.speed[1] * dt) # move = 100*0.01 , 200*0.01

        # application du déplacement
        pos_x += move[0]
        pos_y += move[1]

        # correction de la position si on sort de l'écran
        if pos_x > RESOLUTION [0] + 32:
            pos_x = -32
        elif pos_x < -32 :
            pos_x = RESOLUTION[0] + 32

        if pos_y > RESOLUTION [1] + 32:
            pos_y = -32
        elif pos_y < -32 :
            pos_y = RESOLUTION[1] + 32

        #self.position = (pos_x + 3 , pos_y +1) on rmplace par :
        #self.position = (pos_x + move[0], pos_y + move[1])
        # le 3 à pos_x  détermine la vitesse de deplacement horizontalement
        
        #on bouge effectivement l'objet
        self.position = (pos_x, pos_y)

        # on applique la rotation ici:
        self.rotation += self.rotation_speed * dt 


        
class Spaceship(SpaceItem):
    def __init__ (self, position):
        image = "images/fusee_12.png"
        anchor = (32 , 32)
        super().__init__ (image, position, anchor)
        
        self.velocity = 0

        self.invulnerability = False   
        
        self.chrono = 0

        self.life = 3

    def update (self, dt):
        

        if self.invulnerability == True :
            self.opacity = 125
            self.chrono += dt
            if self.chrono >= 3:
                self.invulnerability = False
                self.chrono = 0
               
           
        else :
            self.opacity = 255
           
            
       
        # on va calculer la vitesse
        dsx = cos(radians(self.rotation)) * self.velocity
        dsy = sin (radians (self.rotation)) * self.velocity * -1
        
        sx = self.speed [0] + dsx
        sy = self.speed [1] + dsy
        
        self.speed = (sx, sy) 

        super().update(dt)


    #on key press, c'est qd on appuie sur la touche
    # on key release, c'est qd on relache la touche

    #qd on appuie
    def on_key_press(self, key, modifiers): # modifiers = alt, ctr et shift (doivent tjrs etre là m$eme si on utilise pas)
        #return super().on_key_press(key, modifiers)
        if key == window.key.LEFT:
            self.rotation_speed = -50

        elif key == window.key.RIGHT:
            self.rotation_speed = 50
        elif key == window.key.UP:
            self.velocity = 5
        elif key == window.key.SPACE:
            self.spawn_bullet()
            

    #qd on relache
    def on_key_release(self, key, modifiers):
        #return super().on_key_release(key, modifiers)
        if key == window.key.LEFT and self.rotation_speed < 0 :
            self.rotation_speed = 0

        elif key == window.key.RIGHT and self.rotation_speed > 0 :
            self.rotation_speed = 0

        elif key == window.key.UP:
            self.velocity = 0

    def spawn_bullet(self):

        bullet_velocity = 100
        sx = cos(radians(self.rotation)) * bullet_velocity
        sy = sin(radians(self.rotation)) * bullet_velocity * -1

        bullet_speed = (self.speed[0] + sx, self.speed[1] + sy)

        x = cos(radians(self.rotation)) * 40
        y = sin(radians(self.rotation)) * 40 * -1

        bullet_positon = (self.position[0] + x, self.position[1] + y)

        bullet = Bullet(bullet_positon, bullet_speed)
        self.layer.add(bullet) 
    
    
    def on_collision(self, other):
        if isinstance (other, Asteroid):
            self.destroy()
            

    def destroy (self):
           
            if self.invulnerability == False:
                
                self.invulnerability = True
                self.life -= 1
                if self.life <= 0 :
                    super().destroy()
                    


        

class Asteroid (SpaceItem):
    def __init__ (self, position, speed, level = 3):
        self.level = level 
        if level == 3:

            image = "images/asteroid_128.png"
            anchor = (64,64)

        elif level == 2:
            image = "images/asteroid64.png"
            anchor = (32,32)

        else :
            image = "images/asteroid32.png"
            anchor = (16,16)

        #speed = (-300,300) on l'enlève maintenant que l'on change la vitesse aléatoirement ds le main.py
        rotation_speed = 50
        super().__init__(image, position, anchor, speed, rotation_speed)


    def on_collision(self, other):
        if isinstance (other, Spaceship):
            other.destroy()



    def destroy(self):
        if self.level > 1:
            for n in range(2):
                sx = randint(-300, 300)
                sy = randint(-300, 300)
                speed = (sx, sy)

                level = self.level -1

                asteroid = Asteroid (self.position, speed, level=level)

                self.layer.add(asteroid)

        super().destroy()




class Bullet(SpaceItem):
    def __init__ (self, position, speed):
        image = "images/bullet.png"
        anchor = (8,8)
        rotation_speed = 100
        super().__init__(image, position, anchor, speed, rotation_speed)

        self.life_time = 0

        def update (self, dt) :
            super().update(dt)

            self.life_time += dt

            if self.life_time >= 3 :
                self.destroy()
    
    
    def on_collision(self, other):
        #isinstance :permet de vérifié qu'un objet appartient à une classe ou à un de ses enfants
        if isinstance(other, Asteroid):
            self.destroy()
            other.destroy()





