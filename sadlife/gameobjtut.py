# Pygame base setup
import pygame, math, random

# Dictionary of colours
COLOURS = {'BLACK':(0,0,0), 'WHITE':(255,255,255), 'RED':(240,0,0),
           'GREEN':(0,180,0), 'BLUE':(0,0,240), 'BROWN':(139,69,19),
           'BLUISH':(50,125,200)}

# Dictionary of fonts
pygame.font.init()
FONTS = {}
comic_sans = pygame.font.SysFont('comicsans', 100)
FONTS['COMICSANS'] = comic_sans
arial_black = pygame.font.SysFont('arialblack', 12)
FONTS['ARIALBLACK'] = arial_black

# FPS
TICK_RATE = 60
# System clock for screen refresh
clock = pygame.time.Clock()

## App window and screen
class Container:

    def __init__(self, title, size = (1600,900), img_path = None):
        self.title = title
        self.size = size
        self.img_path = img_path

        # Create screen of specified size, set colour and title
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)

        # Create screen background image
        if img_path != None:
            bg_img = pygame.image.load(img_path)
            self.img = pygame.transform.scale(bg_img, self.size)
            self.screen.blit(self.img, (0,0))
            pygame.display.update()
        else:
            # Fill the screen with a colour
            self.screen.fill(COLOURS['BLACK'])
            pygame.display.update()

    # Draw background
    def draw_bg(self):
        if self.img_path != None:
            self.screen.blit(self.img, (0,0))
        else:
            self.screen.fill(COLOURS['BLACK'])
        

## Game objects class
class GameObject:

    # Initiate gameobject object with position and size
    def __init__(self, x, y, width, height, img_path = None):
        self.pos = (x, y)
        self.size = (width, height)
        # Load image if path is given
        if img_path != None:
            obj_img = pygame.image.load(img_path)
            self.img = pygame.transform.scale(obj_img, self.size)

    # Draw function for object if image
    def draw(self, background, pos = (0,0), setpos = False):
        if setpos:
            background.blit(self.img, pos)
        else:
            background.blit(self.img, self.pos)

    # Collision detection
    def collision(self, obj):
        xbox = (self.pos[0], self.pos[0] + self.size[0])
        ybox = (self.pos[1], self.pos[1] + self.size[1])
        obj_xbox = (obj.pos[0] + obj.hitx, obj.pos[0] + obj.size[0] - obj.hitx)
        obj_ybox = (obj.pos[1] + obj.hity, obj.pos[1] + obj.size[1] - obj.hity)
        if xbox[0] > obj_xbox[1] or xbox[1] < obj_xbox[0]:
            return False
        elif ybox[0] > obj_ybox[1] or ybox[1] < obj_ybox[0]:
            return False
        else:
            return True


## Player game object subclass
class PlayerCharacter(GameObject):

    speed = 7
##    health = 100
##    lives = 5

    # Initiate player character
    def __init__(self, x, y, width, height, img_path = None):
        super().__init__(x, y, width, height, img_path)

    # Movement (positive = right, negative = left)
    def move(self, direction, screen):
        if direction > 0:
            self.pos = (self.pos[0] + self.speed, self.pos[1])
            if self.pos[0] >= screen.size[0] - (self.size[0] + self.speed):
                self.pos = (screen.size[0] - self.size[0] - self.speed, self.pos[1])
        elif direction < 0:
            self.pos = (self.pos[0] - self.speed, self.pos[1])
            if self.pos[0] <= self.speed:
                self.pos = (self.speed, self.pos[1])

## Non Player game object subclass
class NonPlayerCharacter(GameObject):

##    speed = 3
##    health = 100
##    lives = 5

    # Initiate player character
    def __init__(self, x, y, width, height, hitx, hity, img_path = None, speed = 3):
        super().__init__(x, y, width, height, img_path)
        self.speed = speed

        # Bad code for hit box lenience
        self.hitx = hitx
        self.hity = hity

    # Movement pattern for NPCs
    def move(self, screen):
        if self.pos[1] <= abs(self.speed):
            self.speed = abs(self.speed)
        elif self.pos[1] >= screen.size[1] - (self.size[1] + self.speed):
            self.speed = -abs(self.speed)
        self.pos = (self.pos[0], self.pos[1] + self.speed)

    # For the Chrome dino
    def dinomove(self, screen, jumptimer=1):
        ypos = self.pos[1] + 5
        if ypos >= 510:
            ypos = self.pos[1]
            if jumptimer <= 0:
                ypos -= 150
        if self.pos[0] <= abs(self.speed):
            self.speed = abs(self.speed)
            self.img = pygame.transform.flip(self.img, True, False)
        elif self.pos[0] >= screen.size[0] - (self.size[0] + self.speed):
            self.speed = -abs(self.speed)
            self.img = pygame.transform.flip(self.img, True, False)
        self.pos = (self.pos[0] + self.speed, ypos)
        return jumptimer

def drawTree(display, x1, y1, angle, depth):
    if depth:
        x2 = x1 + int(math.cos(math.radians(angle)) * depth * 10.0)
        y2 = y1 + int(math.sin(math.radians(angle)) * depth * 10.0)
        if round(depth) <= 6:
            pygame.draw.line(display, COLOURS['GREEN'], (x1, y1), (x2, y2), round(depth*0.8))
        else:
            pygame.draw.line(display, COLOURS['BROWN'], (x1, y1), (x2, y2), round(depth*0.8))
        drawTree(display, x2, y2, angle - random.randint(10,30), depth - 1)
        drawTree(display, x2, y2, angle + random.randint(10,30), depth - 1)

## Main body
def main():

    # Smooth movement buffer
    keysDown = -1
    keyValues = []

    # Pygame rectstyles sequence for selective updating
    pyRects = []

    # Start pygame
    pygame.init()

    # Create screen instance
    game_screen = Container('Shana and a Tree', (1600, 600), 'background.jpg')

    ## Load in character object with directional variable
    char = PlayerCharacter(10, 350, 50, 50, 'char.png')
    win1 = PlayerCharacter(0, 0, 50, 50, 'win1.png')
    win2 = PlayerCharacter(0, 0, 50, 50, 'win2.png')
    lose1 = PlayerCharacter(0, 0, 50, 50, 'lose1.png')
    lose2 = PlayerCharacter(0, 0, 50, 50, 'lose2.png')
    lose3 = PlayerCharacter(0, 0, 50, 50, 'lose3.png')
    win = [win1, win2]
    lose = [lose1, lose2, lose3]
    direction = 0

    ## Load in npcs
    npcs = {}
    laundryBoss = NonPlayerCharacter(1350, 100, 120, 180, 5, 10, 'laundry.png', 20)
    npcs['boss'] = laundryBoss
    debt_npc = NonPlayerCharacter(1000, 200, 240, 120, 5, 15, 'debt.png', 10)
    npcs['debt'] = debt_npc
    muscle_npc = NonPlayerCharacter(850, 10, 60, 120, 5, 5, 'muscle.png', 18)
    npcs['gym'] = muscle_npc
    school_npc = NonPlayerCharacter(550, 90, 160, 160, 5, 5, 'school.png', 10)
    npcs['school'] = school_npc
    food_npc = NonPlayerCharacter(300, 400, 160, 100, 5, 15, 'badfood.png', 14)
    npcs['food'] = food_npc

    jumptimer = 0
    internet_npc = NonPlayerCharacter(21, 510, 80, 80, 5, 5, 'internet.png', 20)
    npcs['net'] = internet_npc
    mek = NonPlayerCharacter(1460, 320, 120, 90, 0, 0, 'waterdew.png')

    
    ## ___MAIN GAME LOOP___
    game_over = False
    while not game_over:
        
        ## All possible screen events (clicks, keypresses, etc)
        for event in pygame.event.get():
            # Quit program on pressing the x button
            if event.type == pygame.QUIT:
                game_over = True

            # Key press events
            elif event.type == pygame.KEYDOWN:

                # UP DOWN LEFT RIGHT
                if event.key == pygame.K_UP:
                    continue
                elif event.key == pygame.K_DOWN:
                    continue
                elif event.key == pygame.K_LEFT:
                    direction = -1
                    keysDown += 1
                    keyValues.append(direction)
                elif event.key == pygame.K_RIGHT:
                    direction = 1
                    keysDown += 1
                    keyValues.append(direction)



            # Key release events
            elif event.type == pygame.KEYUP:

                # Stop horizontal movement upon key release of left or right
                if event.key == pygame.K_LEFT:
                    direction = 0
                    keysDown -= 1
                    keyValues.remove(-1)
                elif event.key == pygame.K_RIGHT:
                    direction = 0
                    keysDown -= 1
                    keyValues.remove(1)

            # Movement smoothing
            if keysDown >= 0:
                direction = keyValues[keysDown]
            
##            print(event)

        # Reset screen
        game_screen.draw_bg()

        # Draw tree
##        drawTree(game_screen.screen, 799, 900, -90, 12)

        # Draw npcs
        for npc in npcs.values():
            if npc == npcs['net']:
                if jumptimer == 0:
                    jumptimer = random.randint(30,60)
                jumptimer = npc.dinomove(game_screen, jumptimer-1)
            else:
                npc.move(game_screen)
            npc.draw(game_screen.screen)

        mek.draw(game_screen.screen)

        # Draw character
        char.move(direction, game_screen)
        char.draw(game_screen.screen)

        # FPS Text
        fps_value = clock.get_fps()
        fps_text = FONTS['ARIALBLACK'].render('FPS: '+str(round(fps_value)), True, COLOURS['BLUISH'])
        game_screen.screen.blit(fps_text,(20,10))

        # Collision check
        for npc in npcs.values():
            if char.collision(npc):
                game_over = True
                text = FONTS['COMICSANS'].render('You suck tbh', True, COLOURS['RED'])
                game_screen.screen.blit(text,(600, 250))
                lose[random.randint(0,2)].draw(game_screen.screen, char.pos, True)
                pygame.display.update()
                clock.tick(0.2)
        if char.collision(mek):
            game_over = True
            text = FONTS['COMICSANS'].render('I guess you won', True, COLOURS['GREEN'])
            game_screen.screen.blit(text,(600, 250))
            win[random.randint(0,1)].draw(game_screen.screen, char.pos, True)
            pygame.display.update()
            clock.tick(0.2)
        
        # Screen update and clock ticks to standardize frame rate
        pygame.display.update()
        clock.tick(TICK_RATE)

    ## ___END OF GAME LOOP___

    # Quit pygame once game loop exits
    pygame.quit()

# Main function
main()
#quit()

