import pygame

class Hoop(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/hoop.png")
        self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()

class CollideRect(pygame.sprite.Sprite):
    def __init__(self, width, height, angle):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.image.fill((255, 0, 0))
        self.image = pygame.transform.rotozoom(self.orig_image, angle, 1)
        self.mask = pygame.mask.from_surface(self.image)
        self.image.set_alpha(0)

        self.collided = False

        self.rect = self.image.get_rect(center=self.rect.center)

def circleSurface(color, radius):
    shape_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    return shape_surf

class Ball(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/bball.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        circle = circleSurface((255, 255, 255), 40)
        self.mask = pygame.mask.from_surface(circle)
        self.rect = self.image.get_rect()
        self.clicked = False
    
    def drag(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action

class Spike(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        shape = pygame.Surface((50, 70), pygame.SRCALPHA)
        pygame.draw.polygon(shape, (225, 0, 0), [(25, 0), (0, 70), (50, 70)])

        self.image = shape
        self.mask = pygame.mask.from_surface(shape)
        self.rect = self.image.get_rect()