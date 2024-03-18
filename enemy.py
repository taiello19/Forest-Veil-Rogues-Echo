import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x=1000, y=250, health=30):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('Images/wizard.png'), (400, 400))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = health
        self.max_health = health
        self.shield = 0  # Add this if you plan on having enemy shielding mechanics

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update_health(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        elif self.health < 0:
            self.health = 0

    def update_shield(self, amount):
        self.shield += amount
        if self.shield < 0:
            self.shield = 0