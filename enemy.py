import pygame

class Enemy(pygame.sprite.Sprite):
    ENEMY_STATS = {
        "wizard": {"max_health": 50, "max_shield": 20,"damage": 10},
        "wraith": {"max_health": 20, "max_shield": 0,"damage": 5},
        "caveman": {"max_health": 70, "max_shield": 0,"damage": 12},
        "bat": {"max_health": 30, "max_shield": 0,"damage": 5},
        "bee": {"max_health": 30, "max_shield": 5,"damage": 5},
        "warrior": {"max_health": 80, "max_shield": 30,"damage": 12},
        "demon": {"max_health": 100, "max_shield": 50,"damage": 12},
        "terrorbird": {"max_health": 60, "max_shield": 20,"damage": 12},
        "bigbird": {"max_health": 90, "max_shield": 40,"damage": 12},
        "goop": {"max_health": 40, "max_shield": 15,"damage": 10}
    }

    def __init__(self, enemy_type, x=900, y=100):
        super().__init__()
        image_path = (f'Images/enemies/{enemy_type}.png')
        self.image = pygame.transform.scale(pygame.image.load(image_path), (400, 400))
        self.rect = self.image.get_rect(topleft=(x, y))
        enemy_stats = self.ENEMY_STATS.get(enemy_type, {})
        self.damage = enemy_stats.get("damage")
        self.health = enemy_stats.get("max_health")
        self.max_health = enemy_stats.get("max_health")
        self.shield = enemy_stats.get("max_shield")  # Add this if you plan on having enemy shielding mechanics

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
    