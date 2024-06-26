import pygame
import random
import math

class Enemy(pygame.sprite.Sprite):
    ENEMY_STATS = {
        #Level 1 Enemies
        "spider": {"max_health": 28, "max_shield": 5,"damage": 4,"defend": 7,"dot":2, "dot_duration":2, "reduction": 0},
        "caveman": {"max_health": 35, "max_shield": 0,"damage": 8,"defend": 0,"dot":0, "dot_duration":0, "reduction": 0.2},
        "bat": {"max_health":28, "max_shield": 0,"damage": 5,"defend": 5,"dot":0.2, "dot_duration":1, "reduction": 0},
        "goop": {"max_health": 35, "max_shield": 5,"damage": 15,"defend": 8,"dot":0, "dot_duration":2, "reduction": 0.1},
        "crab": {"max_health": 30, "max_shield": 0,"damage": 6,"defend": 2,"dot":2, "dot_duration":2, "reduction": 0.2},

        #Level 2 Enemies
        "bee": {"max_health": 50, "max_shield": 5,"damage": 6,"defend": 5,"dot":4, "dot_duration":3, "reduction": 0},
        "abominable": {"max_health": 50, "max_shield": 0,"damage": 10,"defend": 0,"dot":0, "dot_duration":0, "reduction": 0.2},
        "crabduo": {"max_health": 55, "max_shield": 0,"damage": 8,"defend": 4,"dot":0, "dot_duration":3, "reduction": 0.1},
        "wraith": {"max_health": 50, "max_shield": 0,"damage": 20,"defend": 8,"dot":0, "dot_duration":2, "reduction": 0},
        "craggle": {"max_health": 55, "max_shield": 0,"damage": 5,"defend": 5,"dot":0.4, "dot_duration":1, "reduction": 0},
        
        #Level 3 Enemies
        "bees": {"max_health": 60, "max_shield": 5,"damage": 7,"defend": 8,"dot":6, "dot_duration":3, "reduction": 0},
        "terrorbird": {"max_health": 60, "max_shield": 10,"damage": 10,"defend": 0,"dot":0, "dot_duration":0, "reduction": 0.2},
        "orcduo": {"max_health": 70, "max_shield": 0,"damage": 8,"defend": 4,"dot":0, "dot_duration":4, "reduction": 0.2},
        "wraithtrio": {"max_health": 70, "max_shield": 0,"damage": 8,"defend": 8,"dot":0.2, "dot_duration":1, "reduction": 0},
        "wizard": {"max_health": 80, "max_shield": 20,"damage": 30,"defend": 12,"dot":0, "dot_duration":3, "reduction": 0},
        
        #Bosses
        "warrior": {"max_health": 105, "max_shield": 0,"damage": 15,"defend": 4,"dot":0, "dot_duration":5, "reduction": 0.4},
        "demon": {"max_health": 120, "max_shield": 30,"damage": 15,"defend": 6,"dot":4, "dot_duration":3, "reduction": 0.2},
        "bigbird": {"max_health": 110, "max_shield": 20,"damage": 15,"defend": 4,"dot":0.6, "dot_duration":2, "reduction": 0},
        
        
        
        
    }

    def __init__(self, enemy_type, x=900, y=200):
        super().__init__()
        image_path = (f'Images/enemies/{enemy_type}.png')
        self.enemy_type = enemy_type
        self.image = pygame.transform.scale(pygame.image.load(image_path), (300, 300))
        self.rect = self.image.get_rect(topleft=(x, y))
        enemy_stats = self.ENEMY_STATS.get(enemy_type, {})

        self.damage = enemy_stats.get("damage")
        self.defend = enemy_stats.get("defend")
        self.health = enemy_stats.get("max_health")
        self.max_health = enemy_stats.get("max_health")
        self.shield = enemy_stats.get("max_shield")

        self.dot = enemy_stats.get("dot")
        self.dot_dur = enemy_stats.get("dot_duration")
        self.current_dur = 0
        self.turn_counter = 0

        self.damage_red = enemy_stats.get("reduction")
    
    def get_reduction_percentage(self):

        return self.damage_red * 100
    
    def enemy_animation(self, screen, font):
        original_x = self.rect.x
        left_target_x = original_x - 20  # Move 20 pixels left
        right_target_x = original_x + 20  # Move 20 pixels right
        steps = 10  # Number of steps for each movement
        
        # Move to the left
        for step in range(steps):
            self.rect.x += (left_target_x - original_x) / steps
            self.draw(screen, font)  # Assuming you have a draw method to render the sprite
            pygame.display.update()
            pygame.time.wait(10)  # Delay between steps
        
        # Move to the right
        for step in range(steps * 2):  # Double steps to move to the right and then back
            self.rect.x += (right_target_x - left_target_x) / (steps * 2)
            self.draw(screen, font)
            pygame.display.update()
            pygame.time.wait(10)
        
        # Move back to original position
        for step in range(steps):
            self.rect.x -= (right_target_x - original_x) / steps
            self.draw(screen, font)
            pygame.display.update()
            pygame.time.wait(10)

    def draw(self, surface, font):
    # Draw the enemy image
        surface.blit(self.image, self.rect)
        
        # Create a text surface with the enemy's name
        text_surface = font.render(self.enemy_type.capitalize(), True, (255, 255, 255))
        
        # Calculate the position for the text (centered above the enemy image)
        text_x = self.rect.centerx - text_surface.get_width() / 2
        text_y = self.rect.top - text_surface.get_height() - 5  # 5 pixels above the enemy
        
        # Blit the text surface to the screen
        surface.blit(text_surface, (text_x, text_y))

    def update_health(self, amount):
        if amount > 0:
            amount
        else:
            amount = math.ceil(amount * (1 - self.damage_red))
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        elif self.health < 0:
            self.health = 0

    def update_shield(self, amount):
        # if amount > 0:
        #     amount
        # else:
        #     amount = math.ceil(amount * (1 - self.damage_red))
        self.shield += amount
        if self.shield < 0:
            self.shield = 0

    def perform_action(self, player):
        chance = random.random()
        # Perform action based on enemy type
        if self.enemy_type == "wizard" or self.enemy_type == "goop" or self.enemy_type == "wraith":
            # Wizard's action pattern: randomly choose between attack and defend
            if chance < 0.7:
                self.turn_counter +=1
                if self.turn_counter % self.dot_dur == 0:  # Every 3rd turn
                    return self.beam(player)
                else:
                    return f"{self.enemy_type} is charging up a powerful beam!", None
            else:
                return self.defend_self()
            
        elif self.enemy_type == "caveman" or self.enemy_type =="abominable" or self.enemy_type =="terrorbird":
            # Caveman's action pattern: always attack
            return self.attack_player(player)

        elif self.enemy_type == "craggle" or self.enemy_type =="wraithtrio" or self.enemy_type =="bat" or self.enemy_type =="bigbird":
            # Wraith's action pattern:
            if self.current_dur > 0:
                    self.current_dur -=1
                    #print(self.current_dur)
                    if self.current_dur == 0:
                        self.damage_red = 0
            elif self.current_dur == 0:
                    self.damage_red = 0

            if chance < 0.7:
                self.turn_counter +=1
                if self.turn_counter % 3 == 0:  # Every 3rd attack
                    self.current_dur = self.dot_dur
                    self.damage_red = self.dot
                    self.attack_player(player)
                    return f'{self.enemy_type} weakened you and you now deal {self.damage_red * 100}% less damage for {self.dot_dur} turns!', max(0, self.damage - player.shield)
                else:
                    return self.attack_player(player)
            else:
                return self.defend_self()
                
        elif self.enemy_type == "bee" or self.enemy_type == "spider" or self.enemy_type == "bees":
            # Bee's action pattern:
            if self.current_dur > 0 and self.turn_counter % 3 == 0 :
                self.dot_damage(player, "poison")
                return self.attack_player(player)
            elif chance < 0.8:
                self.turn_counter +=1
                if self.turn_counter % 3 == 0:  # Every 3rd turn
                    self.current_dur = self.dot_dur
                    self.attack_player(player)
                    return self.dot_damage(player, "poison")
                else:
                    return self.attack_player(player)
            else:
                return self.defend_self()
        
        elif self.enemy_type == "crab" or self.enemy_type == "crabduo" or self.enemy_type == "orcduo" or self.enemy_type == "warrior":
            # Caveman's action pattern: always attack
            if self.current_dur > 0:
                    self.current_dur -=1
                    print(self.current_dur)
                    if self.current_dur == 0:
                        self.damage -= self.defend
            self.turn_counter +=1
            if self.turn_counter % 3 == 0:  # Every 3rd attack
                self.current_dur = self.dot_dur
                self.damage += self.defend
                self.attack_player(player)
                return f'The Enemies are enraged and dealt {self.defend} bonus damage and will for the next {self.dot_dur-1} turns!', max(0, self.damage - player.shield)
            else:
                return self.attack_player(player)
        
        elif self.enemy_type == "demon":
            # Bee's action pattern:
            if self.current_dur > 0 and self.turn_counter % 3 == 0 :
                self.dot_damage(player, "burn")
                return self.attack_player(player)
            elif chance < 0.7:
                self.turn_counter +=1
                if self.turn_counter % 3 == 0:  # Every 3rd turn
                    self.current_dur = self.dot_dur
                    self.attack_player(player)
                    return self.dot_damage(player, "burn")
                else:
                    return self.attack_player(player)
            else:
                return self.defend_self()
            
    def attack_player(self, player):
        enemy_attack_value = self.damage
        effective_player_damage = max(0, enemy_attack_value - player.shield)
        player.update_health(-effective_player_damage)
        player.update_shield(-enemy_attack_value)
        return f'{self.enemy_type} attacked for {enemy_attack_value}!', effective_player_damage
    
    def beam(self, player):
        enemy_attack_value = self.damage
        effective_player_damage = max(0, enemy_attack_value - player.shield)
        player.update_health(-effective_player_damage)
        player.update_shield(-enemy_attack_value)
        self.turn_counter = 0
        return f'{self.enemy_type} cast an extremely strong beam for {enemy_attack_value}!', effective_player_damage        

    def dot_damage(self, player, type):
        enemy_dot_value = self.dot
        effective_player_damage = max(0, enemy_dot_value - player.shield)
        player.update_health(-effective_player_damage)
        player.update_shield(-enemy_dot_value)
        self.current_dur -=1
        if self.current_dur == 0 and self.turn_counter % 3 ==0:
            self.turn_counter =0
        return f'{self.enemy_type} inflicted {type} on you and it will deal {enemy_dot_value} for the next {self.current_dur} turns!', effective_player_damage + self.damage
    
    def defend_self(self):
        enemy_defend_value = self.defend
        self.update_shield(enemy_defend_value)
        return f'{self.enemy_type} shielded for {enemy_defend_value}!',None