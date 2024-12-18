import pygame
import random
import math
import csv
import time

score = 0
base_health = 2160
print("Intercepted Military Communication, Carrier Strike Group 5, United States 7th Fleet, Nort-NorthEast Pacific:") #Lore, uses time.sleep to slowly communicate for dramatic effect
time.sleep(3)
print("o o o")
time.sleep(3)
print("Vice Admiral Fred Kacher: Th3 S3v3nth Fl33t 1s sust@1n1ng h3@vy b0mb@rdm3nt by th3 1nt3rg@l@t1c Tusk@ry 18th R@mp@rt Fl33t.")
time.sleep(5)
print("Vice Admiral Fred Kacher: 0p3r@t10n L@st F0g h@s b33n d3pl0y3d. 1 c@n 0nly h0p3 @ny c0untry h@s th3 p1l0ts, 3xp13r1e3nc3, @nd h3l1c0pt3rs t0 d3pl0y 1n 1t")
time.sleep(5)
print("Vice Admiral Fred Kacher: Th3 r3mn@nts 0f Th3 S3v3nth Fl33t w1ll h0ld th3 Tusk@ry Fl33t @s l0ng @s w3 c@n.")
time.sleep(5)
print("Vice Admiral Fred Kacher: Th1s w1ll b3 my l@st tr@nsm1ss10n. G00dn1ght.")
time.sleep(5)
print("o o o")
time.sleep(3)
name = input("Name: ")
time.sleep(3)
print("o o o")
time.sleep(3)
while True: #Uses While True loop to detect if player input good answer
    print("CONTRACT: You agree to pilot a helicopter a. powered by a Nuclear Reactor b. slightly broken c. that will continously get shot at by very power lasers")
    Contract = input("To save humanity by protecting Joint Base Anacostia-Bolling, Washington DC, Carrying the President, Joint Cheifs of Staff, and Schematics for the Apache? (\"yes\" or \"no\" or \"score\"): ")
    if Contract == "yes":
        break
    elif Contract == "no":
        print("You have failed us.")
        exit()
    elif Contract == "score": #Reads CSV file to get scores
        time.sleep(1)
        print("o o o")
        time.sleep(1)
        with open("score.csv", "r") as file:
            scores = csv.DictReader(file)
            for row in scores:
                print(f"Name: {row['Name']}, Score: {row['Score']}, Ending: {row['How']}")           
        time.sleep(1)
        print("o o o")
        time.sleep(1)
        continue
    else:
        print("If you don't choose you are going to get court-martialed.")
print("o o o")
time.sleep(3)#Tells inputs to user
print("Use WASD or Arrow Keys to Move.\nShoot through Space or Right Click.\nUpgrade at the Helipad, Regens every Minute.\nAliens fire Retaliatory Lasers.\nPress E to view stats\nYou are Humanities Last Hope")
print("o o o")
time.sleep(3)
print("Best of Luck Pilot")


#Initalizes the Pygame Module, Sets Size, Changes Screen Caption and Icon
pygame.init()
SIZE = (1750,500)
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("The Last Apache")
pygame.display.set_icon(pygame.image.load('ModelsSounds\Apache.png'))

#Initalizes Background
background = pygame.image.load('ModelsSounds\Background.png')

#Handles Apache Attack Helicopter Player, Updates Position Through Keys, Handles Health
class ApacheAttackHelicopter(pygame.sprite.Sprite):
    def __init__(self, name, max_health, x, y, SCALE, speed):
        pygame.sprite.Sprite.__init__(self)
        self.name = name 
        self.max_health = max_health
        self.SCALE = SCALE #Scales Image
        self.speed = speed
        self.x = x
        self.y = y
        self.health = max_health
        self.xchange = 2
        self.image = pygame.image.load('ModelsSounds\Apache.png') #Loads Image
        self.image = pygame.transform.scale(self.image, (2*self.SCALE, self.SCALE)) #Sets Image Size
        self.rect = self.image.get_rect() #Turns image into a rect object for pygame collision (If it worked)
        self.rect.center = (self.x, self.y)

    #Handles keys from player
    def keyer(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] or key[pygame.K_w] and self.y >= 0:
            self.y -= self.speed
        elif key[pygame.K_DOWN] or key[pygame.K_s] and self.y <= 400: 
            self.y += self.speed
        if key[pygame.K_RIGHT] or key[pygame.K_d] and self.x <= 1600:
            self.x += self.speed
        elif key[pygame.K_LEFT] or key[pygame.K_a] and self.x >= 0:
            self.x -= self.speed
        
    def return_x(self):
        return self.xchange
    #Returns cords for bullets and collision detection with enemy bullets
    def return_cords(self):
        return (self.x, self.y)
    
    def upgrade(self): #Handles Upgrading for helicoter when at helipad
        global allied_bullets
        upgrade = random.randint(1,100) #Generates random value then uses value to determine upgrade
        if upgrade < 20:
            self.health = self.max_health
            print("You got health")
        elif 20 <= upgrade <= 39:
            self.max_health += 20
            print("You got more Max_Health")
        elif 40 <= upgrade <= 59:
            if self.xchange <= 1:
                self.xchange += 1
                print("Your bullets are less stable")
            else:
                self.xchange -= 1
                print("Your bullets are more stable")
        elif upgrade == 65 and allied_bullets <= 2:
            allied_bullets += 1
            print("You got a second bullet")
        else:
            print("You got nothing")
            pass


    #Handles regen (Negative Numbers) and hits from enemy bullets
    def hit(self, health_gone):
        if (self.health - health_gone) <= 100:
            self.health -= health_gone
        #Handles ending of game, saves score to csv
        if self.health <= 0:
            score_keeper("Sacrifice")
            print("Thank you for your sacrifice. o7")
            global running #Stops program
            running = False

    #Returns Health to be displayed when "E" is pressed.
    def return_health(self):
        return self.health

    #Updates Screen to move Heli to new position
    def update(self):
        SCREEN.blit(self.image, (self.x, self.y))

#Class for Aliens, Handles Movement, Health, and Base Destruction
class Aliens(pygame.sprite.Sprite):
    def __init__(self, level, x, y, speed, max_health, SCALE):
        pygame.sprite.Sprite.__init__(self)
        self.level = level
        self.x = x
        self.y = y
        self.speed = speed
        self.max_health = max_health
        self.SCALE = SCALE
        self.health = 100
        self.image = pygame.image.load('ModelsSounds\Alien.png')#Loads Image
        self.image = pygame.transform.scale(self.image, (self.SCALE, 0.25*self.SCALE)) #Scales Image
        self.rect = self.image.get_rect() #Turns image into a rect object for pygame collision (If it worked)
        self.rect.center = (self.x, self.y)

    #Return Cords for detection with allied bullets
    def return_cords(self):
        return (self.x, self.y)
    
    #Handles health decreases after collision detection
    def hit(self, health_gone):
        self.health -= health_gone
        if self.health <= 0: #Removes itself from update_group to not get access to the update_group.update() line, when Health  is less than 1. 
            self.kill()
            
    #Updates Screen to move the Aliens
    def update(self):
        self.x += self.speed
        if random.randint(0,1) == 1:
            self.x += self.speed
        if self.x >= 1530: #Handles Base_Destruction, Randomizes Speed
            self.kill()
            global score, base_health
            score -= 30
            base_health -= 3
        SCREEN.blit(self.image, (self.x, self.y))
       

#Handles allied and enemy bullets through boolean, Moves Bullets through Update, Gives different bullet damages for each type of weapon
class Bullets(pygame.sprite.Sprite):
    def __init__(self, is_enemy, cord, speed, SCALE, xchange, ran = None, weapons=None):
        pygame.sprite.Sprite.__init__(self)
        self.x = cord[0]
        self.y = cord[1]
        self.is_enemy = is_enemy #Changes bullet attributes based on who fires
        self.SCALE = SCALE
        self.speed = speed
        if ran != None: #Randomizes Y Change in code
            self.ran = ran
        if weapons != None:
            self.weapons = weapons
        if is_enemy:
            self.RANDOM_DES = random.randint(0, 200)
            self.xchange = random.randint(-xchange,xchange)
        else:
            self.RANDOM_DES = random.randint(470,500)
            self.xchange = random.randint(-xchange,xchange)
        self.image_choose = {"Bullet" : "ModelsSounds\Bullet.png", "Rocket" : "ModelsSounds\Rocket.png", "Lasers" : "ModelsSounds\Laser.png"} 
        self.image = pygame.image.load(self.image_choose[weapons]) #Uses a dictionary to choose the model of the lasers based on the weapon given
        self.image = pygame.transform.scale(self.image, (self.SCALE, 2*self.SCALE))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def return_weapon(self): #Returns different health decreases based on type of bullet
        if self.weapons == "Rocket":
            return 100
        elif self.weapons == "Bullet":
            return 50
        else:
            return 2 #Laser
    
    def die(self): #Destroys the bullet if it reachs a target
        self.kill()
    
    def return_cords(self): #Returns cords to collision detecter to see if it is close to a target.
        return (self.x, self.y)
	
    def update(self): #Updates bullets direction and blits it to the screen, is_enemy changes values of variables controlling movement
        self.y += self.speed
        self.x += self.xchange
        if self.is_enemy: #Randomizes bullet speed if enemy
            self.y += random.randint(self.speed*self.ran, 0)
            if self.y < self.RANDOM_DES: #Kills enemy bullets
                self.kill()
        else:
            if self.y > self.RANDOM_DES: #Kills our bullets
                self.kill()
        SCREEN.blit(self.image, (self.x, self.y)) #Draws out bullet
        
def score_keeper(how):
    with open("score.csv", "a") as file:
                header = ["Name", "Score", "How"]
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writerow({"Name": name, "Score": score, "How": how})

running = True #Variable for main pygame loop
apache = ApacheAttackHelicopter(name, 100, 1470, 400, 30, 1.5) #Initalizes our Heli.
clock = pygame.time.Clock() #Iniatlizes clock to throttle code to 60 fps


enemy_group = pygame.sprite.Group() #Group of enemy, used for collision detection
Alien = Aliens(1, 50, random.randint(425, 470), 0.5, 50, 25) #Creates first enemy
enemy_group.add(Alien) #Adds first enemy to group


update_group = pygame.sprite.Group() #Updates sprites using the .update() function
update_group.add(Alien) 
update_group.add(apache)

allied_bullets = 1
bullet_speed = 1 #Defines events for allied and enemy bullets
bullet_reload = 1000 #Creates reload timer
bullet_event = pygame.USEREVENT+1 #Creates event
pygame.time.set_timer(bullet_event, bullet_reload) #Sets event to Timer
bullet = True #Allows bullet to be fired, when reload timer above sets it to true
bullet_group_ally = pygame.sprite.Group() #Creates enemy and ally bullet groups for collison detection
bullet_group_enemy = pygame.sprite.Group()

retal = False #Code below controls Retaliation event for Aliens, like event above does
retal_reload = random.randint(1000,3000)
retal_event = pygame.USEREVENT+2
pygame.time.set_timer(retal_event, retal_reload)

enemy_reload = 3000 #Code below spawns enemies using same event technique as bullets
enemy_spawn = pygame.USEREVENT+3
pygame.time.set_timer(enemy_spawn, enemy_reload)

regen_reload = 60000 #Code below reloads the upgrade and health regen timer, using same events technique
regen_event = pygame.USEREVENT+4
pygame.time.set_timer(regen_event, regen_reload)
regen_poss = True

end_reload = 1200000 #Code below stops the game at a victory at 20 min. Same event technique
end_event = pygame.USEREVENT+5
pygame.time.set_timer(end_event, end_reload)

while running:
    for event in pygame.event.get(): #Handles all events in pygame
        key = pygame.key.get_pressed() #Gets key input
        if (event.type == pygame.MOUSEBUTTONUP or key[pygame.K_SPACE]) and bullet == True: #Handles our firing of bullets
            for i in range(allied_bullets): #Gets 
                rand_weapon = random.randint(0, 20) #Randomizes bullet type
                if rand_weapon == 20:
                    weapon = "Rocket"
                else:
                    weapon = "Bullet"
                Bullet = Bullets(False, (apache.return_cords()), bullet_speed, 10, apache.return_x(), weapons=weapon) #Creates Bullet
                update_group.add(Bullet)
                bullet_group_ally.add(Bullet)
            bullet = False #Starts reload timer again
            retal_reload = random.randint(500,1200) #Creates a new retaliation at a random time
            retal_event = pygame.USEREVENT+2
            pygame.time.set_timer(retal_event, retal_reload)
            retal = True

        elif event.type == bullet_event: #Reloads bullet when bullet_event happens
           bullet = True
        
        elif event.type == retal_event and retal == True: #Handles enemy retaltion to us firing bullets
            for enemy in enemy_group:    #Creates bullet for every enemy
                Bullet = Bullets(True, (enemy.return_cords()), bullet_speed*-1, 10, 15, ran=3, weapons="Lasers") #Creates laser
                update_group.add(Bullet)
                bullet_group_enemy.add(Bullet)
            retal = False #No autocannons, cannot retaliate untill next strike

        elif event.type == enemy_spawn: #Spawns enemys
            Alien = Aliens(1, random.randint(25,75), random.randint(425, 470), 0.5, 50, 25) #Creates enemy
            enemy_group.add(Alien)
            update_group.add(Alien)

        elif event.type == regen_event: #Reloads upgrade for it to be possible to upgrade and regen
            regen_poss = True

        elif key[pygame.K_e]: #Shows stats of player current
            print(f"Base Health: {base_health}")
            print(f"Score: {score}")
            print(f"Health {apache.return_health()}")

        elif event.type == end_event and (base_health > 0): #Victory code once the end event happens, saves to CSV file
            score += 40000 #You earned it
            score_keeper("Victory")
            print("Good Job Soldier")
            running = False

        elif event.type == pygame.QUIT: #Handles exiting loop through X or Control-C
            score_keeper("Unknown Causes") #Saves to csv file, because why not
            print("Farewell, Soldier")
            running = False
            pygame.quit()        
 
    
    #Below is my collision detection system. It gets laggy if there are too many sprites.
    #If you want to know why there isnt a fun autocannon in the game 
    #Blame pygames collision system that decided by rect objects were actually not objects at all 
    #:thumbs=up:

    for bul in bullet_group_ally: #Handles collision between bullets and enemies
        for enm in enemy_group: #Distance formula for every enemy to get distance
            sq_one = math.pow((enm.return_cords()[0])-(bul.return_cords()[0]),2)
            sq_two = math.pow((enm.return_cords()[1])-(bul.return_cords()[1]),2)
            if(math.sqrt(sq_one+sq_two)) <= 50: #Area that bullet needs to be in to hit
                score += 50
                enm.hit(bul.return_weapon())
                bul.die()

    for bul in bullet_group_enemy: #Handles collision between lasers and us, same as above.
        sq_one = math.pow((apache.return_cords()[0])-(bul.return_cords()[0]),2)
        sq_two = math.pow((apache.return_cords()[1])-(bul.return_cords()[1]),2)
        if(math.sqrt(sq_one+sq_two)) <= 50:
            apache.hit(bul.return_weapon())
            score -= 20
            bul.die()

    if regen_poss and 1455 <= apache.return_cords()[0] <= 1470 and  390 <= apache.return_cords()[1] <= 400: #Handles upgrading and regening at the helipad
        apache.hit(-10) #Gets to regen code
        Up = apache.upgrade() #Gets to upgrade code
        regen_poss = False

    if base_health <= 0: #Switches off game when your base dies, sends info to csv before ending
        score_keeper("Defeat")
        print("Humanity Lost")
        running = False

    apache.keyer()#Detects key inputs
    SCREEN.fill((0,0,0))#Removes sprites from last frame
    SCREEN.blit(background, (0, 0))#Draws Epic Background
    update_group.update()#Draws all sprites to display
    pygame.display.update()#Updates Display after Drawing
    clock.tick(60)#Throttles FPS to 60

#Would have added sounds, ran out of time
#Also would have made the code a bit less messy, but again, ran out of time \_*^*_/
#Hope you enjoy me game!