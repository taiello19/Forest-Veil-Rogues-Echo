# player.py
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x=0, y=100, health=80, mana=3):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('Images/Player.png'), (400, 400))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = health
        self.max_health = health
        self.mana = mana
        self.max_mana = mana
        self.shield = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update_health(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        elif self.health < 0:
            self.health = 0
    
    def attack_animation(self, screen):
        original_x = self.rect.x
        target_x = original_x + 20  # Move 20 pixels to the right
        steps = 10  # Number of steps in the animation
        for step in range(steps):
            self.rect.x += (target_x - original_x) / steps  # Move right
            self.draw(screen)
            pygame.display.update()
            pygame.time.wait(10)  # Wait 10 milliseconds between steps
        for step in range(steps):
            self.rect.x -= (target_x - original_x) / steps  # Move back to original position
            self.draw(screen)
            pygame.display.update()
            pygame.time.wait(10)
    
    def defend_animation(self, screen):
        original_y = self.rect.y
        target_y = original_y - 20  # Move 20 pixels up
        steps = 10  # Number of steps in the animation
        for step in range(steps):
            self.rect.y += (target_y - original_y) / steps  # Move up
            self.draw(screen)
            pygame.display.update()
            pygame.time.wait(10)  # Wait 10 milliseconds between steps
        for step in range(steps):
            self.rect.y -= (target_y - original_y) / steps  # Move back to original position
            self.draw(screen)
            pygame.display.update()
            pygame.time.wait(10)  # Wait 10 milliseconds between steps

    def update_mana(self, amount):
        self.mana += amount
        if self.mana > self.max_mana:
            self.mana = self.max_mana
        elif self.mana < 0:
            self.mana = 0

    def update_shield(self, amount):
        self.shield += amount
        if self.shield < 0:
            self.shield = 0

    #def emotion_buff(self, buff):

