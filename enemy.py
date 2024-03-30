import pygame
import random

class Enemy(pygame.sprite.Sprite):
    ENEMY_STATS = {
        "wizard": {"max_health": 50, "max_shield": 20,"damage": 20, "defend": 5},
        "wraith": {"max_health": 20, "max_shield": 0,"damage": 5, "defend":5},
        "caveman": {"max_health": 70, "max_shield": 0,"damage": 12, "defend":0},
        "bat": {"max_health": 30, "max_shield": 0,"damage": 5},
        "bees": {"max_health": 30, "max_shield": 5,"damage": 5,"defend": 5,"dot":3, "dot_duration":2},
        "warrior": {"max_health": 80, "max_shield": 30,"damage": 12},
        "demon": {"max_health": 100, "max_shield": 50,"damage": 12},
        "terrorbird": {"max_health": 60, "max_shield": 20,"damage": 12},
        "bigbird": {"max_health": 90, "max_shield": 40,"damage": 12},
        "goop": {"max_health": 40, "max_shield": 15,"damage": 10}
    }

    def __init__(self, enemy_type, x=900, y=100):
        super().__init__()
        image_path = (f'Images/enemies/{enemy_type}.png')
        self.enemy_type = enemy_type
        self.image = pygame.transform.scale(pygame.image.load(image_path), (400, 400))
        self.rect = self.image.get_rect(topleft=(x, y))
        enemy_stats = self.ENEMY_STATS.get(enemy_type, {})
        self.damage = enemy_stats.get("damage")
        self.defend = enemy_stats.get("defend")
        self.dot = enemy_stats.get("dot")
        self.dot_dur = enemy_stats.get("dot_duration")
        self.current_dur = 0
        self.health = enemy_stats.get("max_health")
        self.max_health = enemy_stats.get("max_health")
        self.shield = enemy_stats.get("max_shield")  # Add this if you plan on having enemy shielding mechanics
        self.turn_counter = 0

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

    def perform_action(self, player):
        chance = random.random()
        # Perform action based on enemy type
        if self.enemy_type == "wizard":
            # Wizard's action pattern: randomly choose between attack and defend
            if random.choice([True, False]):
                self.turn_counter +=1
                if self.turn_counter % 3 == 0:  # Every 3rd turn
                    return self.beam(player)
                else:
                    return f"Enemy wizard is charging up a powerful beam!", None
            else:
                return self.defend_self()
            
        elif self.enemy_type == "caveman":
            # Caveman's action pattern: always attack
            return self.attack_player(player)

        elif self.enemy_type == "wraith":
            # Wraith's action pattern:
            if chance < 0.6:
                return self.attack_player(player)
            else:
                return self.defend_self()
                
        elif self.enemy_type == "bees":
            # Bee's action pattern:
            if self.current_dur > 0 and self.turn_counter % 3 == 0 :
                print('atk2')
                return self.dot_damage(player, "poison")
            elif chance < 0.7:
                print('atk')
                self.turn_counter +=1
                if self.turn_counter % 3 == 0:  # Every 3rd turn
                    self.current_dur = self.dot_dur
                    return self.dot_damage(player, "poison")
                else:
                    return self.attack_player(player)
            else:
                return self.defend_self()

    def attack_player(self, player):
        enemy_attack_value = self.damage
        effective_player_damage = max(0, enemy_attack_value - player.shield)
        player.update_health(-effective_player_damage)
        player.update_shield(-enemy_attack_value)
        return f'Enemy attacked for {enemy_attack_value}!', effective_player_damage
    
    def beam(self, player):
        enemy_attack_value = self.damage
        effective_player_damage = max(0, enemy_attack_value - player.shield)
        player.update_health(-effective_player_damage)
        player.update_shield(-enemy_attack_value)
        self.turn_counter = 0
        return f'Wizard cast an extremely strong beam for {enemy_attack_value}!', effective_player_damage        

    def dot_damage(self, player, type):
        enemy_dot_value = self.dot
        effective_player_damage = max(0, enemy_dot_value - player.shield)
        player.update_health(-effective_player_damage)
        player.update_shield(-enemy_dot_value)
        self.current_dur -=1
        if self.current_dur == 0 and self.turn_counter % 3 ==0:
            self.turn_counter =0
        return f'Enemy inflicted {type} on you and it will deal {enemy_dot_value} for the next {self.current_dur} turns!', effective_player_damage
    
    def defend_self(self):
        enemy_defend_value = self.defend
        self.update_shield(enemy_defend_value)
        return f'Enemy shielded for {enemy_defend_value}!',None