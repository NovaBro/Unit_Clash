import pygame
import numpy as np

class player(pygame.sprite.Sprite):
    def __init__(self, left, top, color):
        pygame.sprite.Sprite.__init__(self)
        self.vector = pygame.Vector2(left, top)
        sideLength = 50 # hit box side length
        self.rect = pygame.Rect((left - sideLength/2, top - sideLength/2), (sideLength, sideLength))
        self.color = color
        # self.x = left
        # self.y = top
        self.position = {
            'x':left,
            'y':top,
        }

        self.health = 1000
        self.resources = 5

    def update(self):
        self.stats = f'Health: {self.health}\nResources: {self.resources}\n'
        self.render_castle()

    def render_castle(self):
        screen = pygame.display.get_surface()
        pygame.draw.circle(screen, self.color, self.vector, 20)

class monster(pygame.sprite.Sprite):
    def __init__(self, position, 
                 color:str, stats:dict,
                 destination:pygame.Vector2
            ):
        pygame.sprite.Sprite.__init__(self)
        sideLength = 50 # hit box side length
        self.rect = pygame.Rect((position['x'] - sideLength/2, position['y'] - sideLength/2), (sideLength, sideLength))
        self.color = color
        self.position = position
        self.destination = destination

        self.health = stats['health']
        self.damage = stats['damage']
        self.speed = stats['speed']
        
        self.moving = True
        self.addStory_capture = True
        self.addStory_attack = True

    def update(self):
        self.move_to(self.destination.x, self.destination.y)

    def move_to(self, x, y):
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, self.color, self.rect)
        x_diff = (x - self.rect.centerx)
        y_diff = (y - self.rect.centery)
        magnitude = np.sqrt(x_diff ** 2 + y_diff ** 2)
        if not x_diff and not y_diff:
            self.moving = False

        if self.moving:
            move_y = y_diff / magnitude * float(self.speed)
            move_x = x_diff / magnitude * float(self.speed)

            self.rect = self.rect.move(move_x, move_y)

class capture_point(pygame.sprite.Sprite):
    def __init__(self, left, top, color):
        pygame.sprite.Sprite.__init__(self)

        self.vector = pygame.Vector2(left, top)
        sideLength = 1 # hit box side length
        self.rect = pygame.Rect((left - sideLength/2, top - sideLength/2), (sideLength, sideLength))
        self.color = color

        self.damage = 1
        self.health = 2

    def update(self):
        self.render_capture()

    def render_capture(self,):
        screen = pygame.display.get_surface()
        pygame.draw.circle(screen, self.color, self.vector, 40)
