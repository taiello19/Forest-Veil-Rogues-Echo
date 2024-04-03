import pygame
import random
import time
import math
from tkinter import *
from tkinter import messagebox
import sys
from player import Player
from enemy import Enemy
from menu import main_menu
from popups import Popups
from map import Map
from map import MapNode
pygame.init()

#set the screen variable size
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

title_font = pygame.font.Font('Fonts/Kingthings_Calligraphica_2.ttf', 72)
font = pygame.font.Font('Fonts/Kingthings_Calligraphica_Light.ttf', 30)
info_font = pygame.font.Font('Fonts/Kingthings_Calligraphica_Light.ttf', 20)
shake_font = pygame.font.Font('Fonts/Kingthings_Calligraphica_Light.ttf', 50)

emotion_images = [pygame.image.load(f'Images/emotion{i}.png') for i in range(1, 7)]
emotion_descriptions = {
    0: "Excited, Get excited and deal extra damage when playing subsequent attack cards!",
    1: "Nervous, At the end of you panic and deal damage to yourself or the enemy!",
    2: "Depressed, Curl up into your shell when you take damage and gain a shield based on damage taken!",
    3: "Vengeful, When you take damage get angry and lash out damaging the enemy!",
    4: "Optimistic, Because of your positive attitude the game admins have blessed you with bonus rewards!",
    5: "Tired, You are super sleepy, play sleep cards to take a nap and restore some health!"
}
def render_multiline_text(screen, font, text, position):
    lines = text.split("\n")
    x, y = position
    screen.fill((0, 0, 0))  
    for line in lines:
        rendered_line = font.render(line, True, (255, 255, 255))
        screen.blit(rendered_line, (x, y))
        y += font.get_height()

def render_text_with_shadow(screen, font, message, position, text_color, shadow_color=(0, 0, 0), offset=(2, 2), shadow_thickness=2):
    for x in range(-shadow_thickness, shadow_thickness+1):
        for y in range(-shadow_thickness, shadow_thickness+1):
            shadow_pos = (position[0] + x, position[1] + y)
            shadow_surface = font.render(message, True, shadow_color)
            screen.blit(shadow_surface, shadow_pos)
    text_surface = font.render(message, True, text_color)
    screen.blit(text_surface, position)

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] > max_width:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    lines.append(current_line)  
    return lines

def display_intro_text(screen, font, text, pace, background_path=None):
    def render_skip_button():
        # Draw button background
        pygame.draw.rect(screen, (0, 0, 0), skip_button_rect)
        #draw white outline around the button
        pygame.draw.rect(screen, (255, 255, 255), skip_button_rect, 2)
        #draw the skip text on the button
        screen.blit(skip_button_text, (skip_button_rect.x + 25, skip_button_rect.y + 8))

    #setup for the skip button
    skip_button_font = pygame.font.Font(None, 30) 
    skip_button_text = skip_button_font.render('Skip', True, (255, 255, 255))
    skip_button_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 70, 100, 40)  

    if background_path != None:
        background = pygame.image.load(background_path).convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background, (0, 0)) 
    else: 
        screen.fill((0, 0, 0))
    render_skip_button()  

    #function to immediately render all text and wait for skip
    def render_all_text_and_wait_for_skip():
        screen.fill((0, 0, 0))
        wrapped_lines = wrap_text(text, font, max_width)
        y_position = y_start_position
        for wrapped_line in wrapped_lines:
            text_surface = font.render(wrapped_line, True, (255, 255, 255))
            screen.blit(text_surface, (50, y_position))
            y_position += font.get_height()
        render_skip_button()
        pygame.display.flip()

        #wait for a second skip to proceed
        waiting_for_skip = True
        while waiting_for_skip:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and skip_button_rect.collidepoint(pygame.mouse.get_pos()):
                    waiting_for_skip = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.time.wait(100)

    words = text.split()
    line = ""
    max_width = screen.get_width() - 100
    y_start_position = SCREEN_HEIGHT // 2 - 200

    for word in words:
        temp_line = f"{line}{word} "
        line_width, _ = font.size(temp_line)
        
        if line_width >= max_width:
            #when exceeding max width, prepare for a new line
            screen.fill((0, 0, 0))
            render_skip_button()
            line = word + " "
        else:
            line = temp_line

        #render the current line and the skip button
        screen.fill((0, 0, 0))
        render_multiline_text(screen, font, line, (50, y_start_position))
        render_skip_button()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and skip_button_rect.collidepoint(pygame.mouse.get_pos()):
                render_all_text_and_wait_for_skip()
                return
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        time.sleep(pace)

    render_all_text_and_wait_for_skip()

def show_cutscene(screen, background_path, text_color, message):
    background = pygame.image.load(background_path).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background, (0, 0))

    font = pygame.font.Font('Fonts/Kingthings_Calligraphica_Light.ttf', 50)
    wrapped_text = wrap_text(message, font, SCREEN_WIDTH - 100)

    y_pos_start = (SCREEN_HEIGHT // 2) - (len(wrapped_text) * font.get_height() // 2)
    for line in wrapped_text:
        text_width, text_height = font.size(line)
        position = ((SCREEN_WIDTH - text_width) // 2, y_pos_start)
        render_text_with_shadow(screen, font, line, position, text_color, shadow_color=(0, 0, 0), offset=(2, 2), shadow_thickness=2)
        y_pos_start += text_height

    # Setup for the "Continue" button, similar to your skip button setup
    continue_button_font = pygame.font.Font(None, 30) 
    continue_button_text = continue_button_font.render('Continue', True, (255, 255, 255))
    continue_button_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 70, 100, 40)
    # Draw button background and outline
    pygame.draw.rect(screen, (0, 0, 0), continue_button_rect)
    pygame.draw.rect(screen, (255, 255, 255), continue_button_rect, 2)
    # Center the "Continue" text within the button
    text_rect = continue_button_text.get_rect(center=continue_button_rect.center)
    screen.blit(continue_button_text, text_rect)

    pygame.display.flip()

    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and continue_button_rect.collidepoint(pygame.mouse.get_pos()):
                waiting_for_click = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def draw_shaking_text(screen, background_path, font, message, original_position, text_color, shake_intensity=5, duration=5):
    start_time = pygame.time.get_ticks()  # Get the start time in milliseconds
    end_time = start_time + duration * 1000  # Duration converted to milliseconds

    while pygame.time.get_ticks() < end_time:
        background = pygame.image.load(background_path).convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background, (0, 0))  
        
        # Shaking effect
        x_shake = original_position[0] + random.randint(-shake_intensity, shake_intensity)
        y_shake = original_position[1] + random.randint(-shake_intensity, shake_intensity)
        
        # Create a surface for text
        text_surface = font.render(message, True, text_color)
        screen.blit(text_surface, (x_shake, y_shake))
        
        pygame.display.flip()  # Update the display
        
        # Event loop to keep the application responsive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.time.delay(20)

def endgame():
    show_cutscene(screen, 'Images/wizardtower.jpg', (255, 255, 255), "You break through a clearing in the forest to find a msytical looking tower. You walk inside to find a half open chest, inside you see a crystal, you pick it up and are restored of your emotions when all of a sudden you hear a voice in your head...")
    final_message = ". . . you weren't supposed to make it this far. I'm sorry it has come to this . . . goodbye . . . "
    display_intro_text(screen, font, final_message , 0.5)
    draw_shaking_text(screen, 'Images/cave.jpg', shake_font, ". . .  F a l l i n g  . . .", (SCREEN_WIDTH - 1000, SCREEN_HEIGHT//2), (255, 255, 255), shake_intensity=5, duration=4)

def player_death():
    display_intro_text(screen, font, "You've taken a lot of damage . . . you start stumbling around and you feel light headed . . . The voice inside your head says . . . maybe next time young one . . . you start to black out . . ." , 0.5, 'Images/deathforest.jpg')
    draw_shaking_text(screen, 'Images/graveyard.jpg', shake_font, ". . .  Y o u   a r e   d e a d  . . .", (SCREEN_WIDTH - 900, SCREEN_HEIGHT//2), (138, 3, 3), shake_intensity=5, duration=4)
    
#-------------------------------------------------------------------------------
#PLAYERS
player = Player()



#ENEMY
enemy_types = [["spider", "caveman", "bat","goop", "crab"] , #enemy_types[0]
               ["bee","abominable","crabduo", "wraith","craggle"], #enemy_types[1]
               ["bees","terrorbird", "orcduo", "wraithtrio","wizard"], #enemy_types[2]
               ["demon","warrior", "bigbird"]] #enemy_types[3]
enemy_type = random.choice(enemy_types[0])
enemy = Enemy(enemy_type)
#enemy_types[0].remove(enemy_type)
#print(enemy_types)

enemy_counter = 0

#health bars
health_bar_width = 150
health_bar_height = 15

level_2 = False
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#CARDS
cards = [{'type': 'Attack', 'value': 5, 'mana': 1, 'name': 'Attack', 'info': 'Deal 5 Damage'},
         {'type': 'Attack', 'value': 5, 'mana': 1, 'name': 'Attack', 'info': 'Deal 5 Damage'},
         {'type': 'Attack', 'value': 5, 'mana': 1, 'name': 'Attack', 'info': 'Deal 5 Damage'},
         {'type': 'Attack', 'value': 5, 'mana': 1, 'name': 'Attack', 'info': 'Deal 5 Damage'},
         {'type': 'Attack', 'value': 5, 'mana': 1, 'name': 'Attack', 'info': 'Deal 5 Damage'},
         {'type': 'Attack', 'value': 5, 'mana': 1, 'name': 'Attack', 'info': 'Deal 5 Damage'},
         {'type': 'Attack', 'value': 5, 'mana': 1, 'name': 'Attack', 'info': 'Deal 5 Damage'},
         {'type': 'Attack', 'value': 5, 'mana': 1, 'name': 'Attack', 'info': 'Deal 5 Damage'},
         {'type': 'Defend', 'value': 5, 'mana': 1, 'name': 'Defend', 'info': 'Block 5 Damage'},
         {'type': 'Defend', 'value': 5, 'mana': 1, 'name': 'Defend', 'info': 'Block 5 Damage'},
         {'type': 'Defend', 'value': 5, 'mana': 1, 'name': 'Defend', 'info': 'Block 5 Damage'},
         {'type': 'Defend', 'value': 5, 'mana': 1, 'name': 'Defend', 'info': 'Block 5 Damage'},
         {'type': 'Defend', 'value': 5, 'mana': 1, 'name': 'Defend', 'info': 'Block 5 Damage'},
         {'type': 'Defend', 'value': 5, 'mana': 1, 'name': 'Defend', 'info': 'Block 5 Damage'}]


draw_pile = list(cards)  #initial draw pile 
random.shuffle(draw_pile) #shuffle the initial deck
discard_pile = [] 

player_hand = []

def draw_hand(extra_card=False):
    card_width, card_height = 150, 180  
    draw_number = 5 if extra_card else 4
    if level_2:
        draw_number += 1
    for _ in range(draw_number):
        if not draw_pile:
            #shuffle discard pile back into draw pile when empty
            draw_pile.extend(discard_pile)
            discard_pile.clear()
            random.shuffle(draw_pile)

        card = draw_pile.pop()
        card['rect'] = pygame.Rect(0, 0, card_width, card_height)  
        player_hand.append(card)



def add_emotion_cards(deck, emotion_index):
    emotion_specific_cards = {
        0: [{'type': 'Attack', 'value': 8, 'mana': 1, 'name': 'Knife', 'info': 'Deal 8 Damage'}, 
            {'type': 'Stun', 'value': 1, 'mana': 1, 'name': 'Stun', 'info': 'Stun the enemy,\n forcing them to \nskip a turn'}],  #excited

        1: [{'type': 'Attack', 'value': 7, 'mana': 0, 'name': 'Wood Spear', 'info': 'Deal 5 Damage'}, 
            {'type': 'Defend', 'value': 6, 'mana': 0, 'name': 'Wood Wall', 'info': 'Block 6 Damage'}],  #nervous

        2: [{'type': 'Defend', 'value': 12, 'mana': 2, 'name': 'Large Shield', 'info': 'Block 10 Damage'}, 
            {'type': 'Dual', 'value': 7, 'shield': 3, 'mana': 1, 'name': 'Lash Out', 'info': 'Deal 7 Damage,\n Block 3 Damage'}],  #depressed - dual = deal damage and gain half that in shield

        3: [{'type': 'Self', 'value': 2, 'shield': 6, 'mana': 2, 'name': 'Double-Edge', 'info': 'Deal 2 Damage\n to yourself'}, 
            {'type': 'Dual', 'value': 6, 'shield': 3, 'mana': 1, 'name': 'Rampage',  'info': 'Deal 7 Damage,\n Block 3 Damage'}],  #vengeful - Self = take 2 damage

        4: [{'type': 'Attack', 'value': 5, 'mana': 0, 'name': 'Slash', 'info': 'Deal 5 Damage'}, 
            {'type': 'Defend', 'value': 7, 'mana': 0, 'name': 'Lock Down', 'info': 'Block 7 Damage'}, 
            {'type': 'Attack', 'value': 8, 'mana': 1, 'name': 'Bash', 'info': 'Deal 8 Damage'}],  #optimistic
            
        5: [{'type': 'SleepDMG', 'value': 3, 'mana': 0, 'sleepyTime': 5, 'name': 'Sleep Attack', 'info': 'Deal 3 Damage,\n Heal 5 Health'}, 
            {'type': 'SleepBlock', 'value': 0, 'mana': 2, 'sleepyTime': 10, 'name': 'Long Slumber', 'info': 'Heal 10 Health'}],  #tired
        
    }

    #add the cards for the selected emotion to the deck
    if emotion_index in emotion_specific_cards:
        deck.extend(emotion_specific_cards[emotion_index])

    return deck


def add_new_cards():
        if emotion_index == 4:  # If the selected emotion is Optimistic
            new_cards = [
                {'type': 'Dual', 'value': 8, 'shield': 4, 'mana': 1, 'name': 'Bludgeon',  'info': 'Deal 8 Damage,\n Block 4 Damage'}, 
                {'type': 'Dual', 'value': 4, 'shield': 9, 'mana': 1, 'name': 'Deny',  'info': 'Deal 4 Damage,\n Block 9 Damage'}
            ]
            draw_pile.extend(new_cards)  # Add new cards directly to the draw pile
            random.shuffle(draw_pile)

def add_new_cards_2():
        if emotion_index == 4:  # If the selected emotion is Optimistic
            new_cards = [
                {'type': 'Dual', 'value': 8, 'shield': 4, 'mana': 1, 'name': 'Bludgeon',  'info': 'Deal 7 Damage,\n Block 3 Damage'}, 
                {'type': 'Dual', 'value': 4, 'shield': 9, 'mana': 1, 'name': 'Deny',  'info': 'Deal 7 Damage,\n Block 3 Damage'}
            ]
            draw_pile.extend(new_cards)  # Add new cards directly to the draw pile
            random.shuffle(draw_pile)
        elif emotion_index == 5:
            new_cards = [
                {'type': 'SleepDMG', 'value': 8, 'mana': 0, 'sleepyTime': 5, 'name': 'Sleepy Slam', 'info': 'Deal 8 Damage,\n Heal 5 Health'}
            ]
            draw_pile.extend(new_cards)  # Add new cards directly to the draw pile
            random.shuffle(draw_pile)

def draw_card_info(surface, text, pos, font, color=(0,0,0), max_width=None):
    lines = text.split('\n')
    y_offset = 0
    for line in lines:
        line_surface = font.render(line, True, color)
        if max_width and line_surface.get_width() > max_width:
            # Optional: If a single line is too wide, you can split it further here
            # This is a more advanced feature and requires a similar approach to the draw_text_wrapped function
            pass
        surface.blit(line_surface, (pos[0], pos[1] + y_offset))
        y_offset += font.get_height()
#-------------------------------------------------------------------------------
            

#-------------------------------------------------------------------------------
#GAME STATE    
selected_emoji_index = main_menu(screen, title_font, font, emotion_images, emotion_descriptions) 
draw_pile = add_emotion_cards(draw_pile, selected_emoji_index)  
random.shuffle(draw_pile)  
#optimistic extra draw
if selected_emoji_index == 4:
    draw_hand(extra_card=True)
else:
    draw_hand()  # player draws initial hand

turn_active = True
enemy_turn_active = False
end_turn_button_rect = pygame.Rect(SCREEN_WIDTH - 150, 10, 140, 40)
end_turn_button_text = font.render("End Turn", True, (0, 0, 0))
use_button_rect = pygame.Rect(SCREEN_WIDTH - 180, SCREEN_HEIGHT - 100, 120, 40)
use_button_text = font.render("Use", True, (0, 0, 0))
selected_card = None

#remove later, temporary enemy turn sim before enemy AI is added
start_enemy_turn_time = 0
enemy_turn_duration = 5  #in seconds

enemy_turn_text = None
system_text = None
sleep_text = None

#-------------------------------------------------------------------------------
#EMOTIONS

#Excited
activate_excited = False
#this determines the +1 dmg to atk
excited_mode = False
#this allows for the stun card to work
stun = False
#excited mode damage boost
excited_damage = 1

#Nervous
activate_nervous = False
#variables to do dmg 
nervous_selfdmg = 1
nervous_dmg = 3

#Depressed
activate_depressed = False
depressed_multiplier = 3
damage_taken_last_turn = 0

#Vengeful
activate_vengeful = False
vengeful_multiplier = 0.50

#Optimistic
activate_optimistic = False

#Tired
activate_tired = False
sleep = 0
#-------------------------------------------------------------------------------
 
#GAME LOOP

if selected_emoji_index == -1:
    pygame.quit()
    sys.exit()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
game_map = Map()
game_map.generate_map()
nodeVar = False
display_map = True
level_count = 0

intro_variable = ''
intro_colour = ''
if selected_emoji_index is not None:
    emotion_index = selected_emoji_index
    if emotion_index == 0:
        intro_variable = 'exitement'
        intro_colour = 'green'
    elif emotion_index == 1:
        intro_variable = 'nervousness'
        intro_colour = 'orange'
    elif emotion_index == 2:
        intro_variable = 'depression'
        intro_colour = 'blue'
    elif emotion_index == 3:
        intro_variable = 'vengance'
        intro_colour = 'red'
    elif emotion_index == 4:
        intro_variable = 'optimism'
        intro_colour = 'yellow'
    elif emotion_index == 5:
        intro_variable = 'sleepiness'
        intro_colour = 'purple'

intro_text_skip = 'skip'
intro_text = f"You wake up in an unfamiliar location, with no memories or idea of who you are . . . you look around but all you can see is trees for miles . . . You stand up dazed and confused but all of a sudden a chest appears out of nowhere . . . You walk up to the chest and it opens automatically displaying 6 different masks . . . You reach in and pull out the {intro_colour} mask . . . You feel a strong force pulling you to equip the mask . . . You put the mask on and a strong wave of {intro_variable} fills your soul . . . You look up and see three pathways form in front of you, choose wisely . . . "
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
display_intro_text(screen, font, intro_text, 0.4)

run = True
while run:
    #IMPLEMENT
    #Main Menu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



    if display_map:
        screen.fill((255, 255, 255))
        background = pygame.image.load('Images/map.jpeg').convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background, (0,0))
        mouse_pos = pygame.mouse.get_pos()
        game_map.render(screen, mouse_pos)  
        game_map.draw_legend(screen, font)
        pygame.display.update()
        node_clicked = False 
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                node_clicked = game_map.handle_click(mouse_pos)

                if node_clicked == 'battle' or node_clicked == 'battle2' or node_clicked == 'battle3' or node_clicked == 'boss':
                    display_map = False
                    break
                elif node_clicked == 'heal':
                    health_gain = player.max_health - player.health
                    player.update_health(health_gain)
                    show_cutscene(screen, 'Images/campfire.png', (255 ,255 ,255) , f"You notice a campfire out of the corner of your eye, you sit down and have a quick snack. Heal {health_gain} health!")
                    break
            elif event.type == pygame.QUIT:
                run = False

    else:
        key = pygame.key.get_pressed()
        screen.fill((255, 255, 255))
        background = pygame.image.load('Images/fightbackground.png').convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background, (0,0))

        #display players
        player.draw(screen)
        enemy.draw(screen, font)

        #display mana
        mana_text = font.render(f"{player.mana}/{player.max_mana}", True, (0, 0, 255))
        screen.blit(mana_text, (20, SCREEN_HEIGHT - 100))
        mana_rect = pygame.Rect(10, SCREEN_HEIGHT - 110, 50, 50)
        pygame.draw.rect(screen, (0, 0, 255), mana_rect, 2)

        #display player's shield and health
        player_shield_text = font.render(f"Shield: {player.shield}", True, (0, 0, 0))
        screen.blit(player_shield_text, (10, player.rect.bottom + 70))

        #enemy shield
        enemy_shield_text = font.render(f"Enemy Shield: {enemy.shield}", True, (0, 0, 0))
        screen.blit(enemy_shield_text, (SCREEN_WIDTH - 200, enemy.rect.bottom + 70))

        #enemy resist
        enemy_resist_text = font.render(f"Enemy Resist: {enemy.get_reduction_percentage()}%", True, (0, 0, 0))
        screen.blit(enemy_resist_text, (SCREEN_WIDTH - 200, enemy.rect.bottom + 100))
        
        player_health_bar = pygame.Rect(10, player.rect.bottom + 10, health_bar_width * (player.health / player.max_health), health_bar_height)
        enemy_health_bar = pygame.Rect(SCREEN_WIDTH - 40 - health_bar_width * (enemy.health / enemy.max_health), enemy.rect.bottom + 10, health_bar_width * (enemy.health / enemy.max_health), health_bar_height)

        pygame.draw.rect(screen, (0, 255, 0), player_health_bar)
        pygame.draw.rect(screen, (255, 0, 0), enemy_health_bar)

        player_health_text = font.render(f"Player Health: {player.health}", True, (0, 0, 0))
        enemy_health_text = font.render(f"Enemy Health: {enemy.health}", True, (0, 0, 0))

        #display health values in text
        screen.blit(player_health_text, (10, player.rect.bottom + 40))
        screen.blit(enemy_health_text, (SCREEN_WIDTH - 200, enemy.rect.bottom + 40))

        #emotion buff in text
        if selected_emoji_index is not None:
            emotion_index = selected_emoji_index
            #different emotions giving different buffs
            if emotion_index == 0:
                additional_text = "Excited"
                activate_excited = True
            elif emotion_index == 1:
                additional_text = "Nervous"
                activate_nervous = True
            elif emotion_index == 2:
                additional_text = "Depressed"
                activate_depressed = True
            elif emotion_index == 3:
                additional_text = "Vengeful"
                activate_vengeful = True
            elif emotion_index == 4:
                additional_text = "Optimistic"
                activate_optimistic = True
            elif emotion_index == 5:
                additional_text = "Tired"
                activate_tired == True
            else:
                additional_text = "Woopsie, something messed up, you shouldn't be here!!"
                #add code to kick them to main menu

            #display the text
            additional_text_rendered = font.render(additional_text, True, (0, 0, 0))
            screen.blit(additional_text_rendered, (10, player.rect.bottom + 100))
        

        #draw pile and discard pile
        draw_pile_text = font.render(f"Draw Pile: {len(draw_pile)}", True, (0, 0, 0))
        discard_pile_text = font.render(f"Discard Pile: {len(discard_pile)}", True, (0, 0, 0))
        screen.blit(draw_pile_text, (10, SCREEN_HEIGHT - 40))
        screen.blit(discard_pile_text, (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 40))

        pygame.draw.rect(screen, (100, 200, 100), use_button_rect)
        screen.blit(use_button_text, (SCREEN_WIDTH - 140, SCREEN_HEIGHT - 90))

        #card sizes
        card_width, card_height = 150, 180
        card_spacing = 15
        total_hand_width = len(player_hand) * card_width + (len(player_hand) - 1) * card_spacing
        start_x = ((SCREEN_WIDTH - total_hand_width) // 2) - 40

        #-------------------------------------------------------------------------------------------------------------------------------------------
        #Active Game loop

        #Draw the deck onto screen
        for i, card in enumerate(player_hand):
            card_rect = pygame.Rect(start_x + i * (card_width + card_spacing), SCREEN_HEIGHT - card_height - 20, card_width, card_height)
            card['rect'] = card_rect
            

            if card == selected_card:
                pygame.draw.rect(screen, (255, 255, 0), card_rect, 3)
                card_rect.y -= 5
            
            if turn_active:
                pygame.draw.rect(screen, (200, 200, 200), card_rect)
                card_text = font.render(f"{card['name']}", True, (0, 0, 0))
                screen.blit(card_text, (card_rect.x + 10, card_rect.y + 10))
                
                #display mana value in the top right corner of each card
                mana_text = font.render(str(card['mana']), True, (0, 0, 255))
                
                circle = pygame.Rect(card_rect.x + card_rect.width - 30, card_rect.y + 5, 24, 24)
                
                pygame.draw.ellipse(screen, (0, 0, 0), circle, 2)
                
                #display mana value
                screen.blit(mana_text, (card_rect.x + card_rect.width - 25, card_rect.y - 5))

                #display card information
                draw_card_info(screen, card['info'], (card_rect.x + 5, card_rect.y + 100), info_font)        


        #display whos turn it is
        turn_text = font.render("Your Turn" if turn_active else "Enemy Turn", True, (255, 255, 255))
        screen.blit(turn_text, ((SCREEN_WIDTH - turn_text.get_width()) // 2, 10))

        if turn_active:
            pygame.draw.rect(screen, (100, 200, 100), end_turn_button_rect)
            screen.blit(end_turn_button_text, (SCREEN_WIDTH - 140, 20))

        show_stun_message = False
        stun_message_start_time = 0
        #-------------------------------------------------------------------------------------------------------------------------------------------
        #ENEMY TURN

        #enemy turn
        if not turn_active and enemy_turn_text is None:
            if stun:
                #start the stun timer
                if not show_stun_message:
                    show_stun_message = True
                    stun_message_start_time = pygame.time.get_ticks()
                    enemy_turn_text = "Enemy is stunned for one turn"
                    stun = False
                
                #go to player turn
                if pygame.time.get_ticks() - stun_message_start_time >= 1000:
                    show_stun_message = False
                    stun = False  
                    turn_active = True  
                    enemy_turn_text = None  
            else:
                enemy_turn_text,effective_player_damage = enemy.perform_action(player)
                if effective_player_damage is not None:
                    #depressed mode
                    damage_taken_last_turn += effective_player_damage
                    vengeful_damage = math.ceil(effective_player_damage * vengeful_multiplier)
                    if effective_player_damage > 0 and activate_vengeful == True:
                        enemy.update_health(-vengeful_damage)
                #     #depressed mode
                #     damage_taken_last_turn += effective_player_damage

        if enemy_turn_text:
            enemy_turn_text_rendered = font.render(enemy_turn_text, True, (255, 255, 255)) 
            screen.blit(enemy_turn_text_rendered, ((SCREEN_WIDTH - enemy_turn_text_rendered.get_width()) // 2, 150))
        
        if system_text:
            system_text_rendered = font.render(system_text, True, (255, 255, 255))
            screen.blit(system_text_rendered, ((SCREEN_WIDTH - system_text_rendered.get_width()) // 2, 180))  

        if turn_active:  
            enemy_turn_text = None
            system_text = None
        #-------------------------------------------------------------------------------------------------------------------------------------------
        #PLAYER TURN
        #Depressed mode
        if activate_depressed and turn_active:
            shield_to_add = math.ceil(damage_taken_last_turn / depressed_multiplier)
            player.update_shield(shield_to_add)
            damage_taken_last_turn = 0  

        if system_text is not None:
            system_text_rendered = font.render(system_text, True, (255, 255, 255))
            screen.blit(system_text_rendered, ((SCREEN_WIDTH - system_text_rendered.get_width()) // 2, 180))
        
        if not turn_active and sleep_text:
            sleep_text = None

        if not turn_active and activate_depressed:
            system_text = None
        
        #Player turn 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                if turn_active:
                    #discard players hand and draw new cards
                    discard_pile.extend(player_hand)
                    player_hand.clear()
                    if selected_emoji_index == 4:
                        draw_hand(extra_card=True)
                    else:
                        draw_hand()
                    excited_mode = False
                    turn_active = False
                    player.shield = 0
                    system_text = None
                    start_enemy_turn_time = time.time()
                else:
                    #start the player's turn again
                    turn_active = True

            #check if 'End Turn' button is clicked during players turn
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if turn_active:
                    if end_turn_button_rect.collidepoint(event.pos):
                        player.mana = player.max_mana
                        enemy.shield = 0
                        excited_mode = False
                        selected_card = None
                        discard_pile.extend(player_hand)
                        player_hand.clear()
                        if selected_emoji_index == 4:
                            draw_hand(extra_card=True)
                        else:
                            draw_hand()
                        turn_active = False
                        start_enemy_turn_time = time.time()

                        #nervous ability
                        chance = random.random()
                        if activate_nervous == True:
                            if chance < 0.6:
                                enemy.update_health(-nervous_dmg)
                                system_text = f'You thrash out and deal {nervous_dmg} damage to the enemy!'
                            else:
                                player.update_health(-nervous_selfdmg)
                                system_text = f'You stub your toe, take {nervous_selfdmg} damage.'

                    elif use_button_rect.collidepoint(event.pos):
                        #check if a card is selected
                        if selected_card is not None and player.mana >= selected_card['mana']:
                            #card type will determine the action taken on use button click
                            if selected_card['type'] == 'Attack':
                                #deal damage to the enemy
                                effective_damage = selected_card['value'] - enemy.shield
                                enemy.update_shield(-selected_card['value'])
                                #excited mode
                                if excited_mode == True:
                                    effective_damage += excited_damage

                                if effective_damage > 0:
                                    enemy.update_health(-effective_damage)
                                if activate_excited == True and not excited_mode:
                                    excited_mode = True
                            elif selected_card['type'] == 'Defend':
                                #add shield to the player
                                player.update_shield(selected_card['value'])
                            elif selected_card['type'] == 'Self':
                                player_damage = selected_card['value']
                                player.update_health(-player_damage)
                                if activate_vengeful == True:
                                    vengeful_damage = math.ceil(player_damage + 6)
                                    effective_damage = vengeful_damage - enemy.shield
                                    enemy.update_shield(-vengeful_damage)
                                    if effective_damage > 0:
                                        enemy.update_health(-effective_damage)
                                player.update_shield(selected_card['shield'])

                            elif selected_card['type'] == 'SleepDMG':
                                effective_damage = selected_card['value'] - enemy.shield
                                enemy.update_shield(-selected_card['value'])
                                enemy.update_health(-effective_damage)
                                restore = selected_card['sleepyTime']
                                player.update_health(restore)
                                sleep_text = f'You restored {restore} health!'

                            elif selected_card['type'] == 'Stun':
                                stun = True
                            elif selected_card['type'] == 'Dual':
                                effective_damage = selected_card['value'] - enemy.shield
                                enemy.update_shield(-selected_card['value'])
                                enemy.update_health(-effective_damage)
                                shield = selected_card['shield']
                                player.update_shield(shield)
                            elif selected_card['type'] == 'SleepBlock':
                                restore = selected_card['sleepyTime']
                                player.update_health(restore)
                                sleep_text = f'You restored {restore} health!'

                            #update mana and discard the card
                            player.mana -= selected_card['mana']
                            discard_pile.append(selected_card)
                            player_hand.remove(selected_card)
                            selected_card = None

                        else:
                            #not enough mana message, should be changed to an animation later
                            mana_popup = Popups(screen, 'You dont have enough mana to perform this action, please hit "End Turn"')
                            mana_popup.show()
                            selected_card = None




                    elif event.button == 1:  #left mouse button
                        for card in player_hand:
                            if card['rect'].collidepoint(event.pos):
                                if selected_card is None:
                                    selected_card = card
                                elif selected_card == card:
                                    selected_card = None

                    

        #check if it's the enemys turn and end after X seconds
        if not turn_active and enemy_turn_text is not None:
            if time.time() - start_enemy_turn_time >= enemy_turn_duration:
                turn_active = True
                player.shield = 0
                enemy_turn_text = None
                start_enemy_turn_time = 0
        
        if sleep_text:
            x = player.rect.centerx - font.size(sleep_text)[0] / 2
            y = player.rect.top - 20 
            rendered_text = font.render(sleep_text, True, (255, 255, 255))
            screen.blit(rendered_text, (x, y))

        if player.health <= 0:
            player_death()
            break
        #handle level increase
        if enemy.health <= 0:
            if enemy.enemy_type == "warrior" or enemy.enemy_type == "demon" or enemy.enemy_type == "bigbird":
                endgame()
                break
            
            show_cutscene(screen,  'Images/forestpath.jpg', (255 ,255 ,255) , "You continue down the path...")
            player.mana = player.max_mana
            player.shield = 0
            excited_mode = False
            selected_card = None
            discard_pile.extend(player_hand)
            player_hand.clear()
            if selected_emoji_index == 4:
                draw_hand(extra_card=True)
            else:
                draw_hand()
            display_map = True 

            enemy_counter +=1
            if enemy_counter % 3 == 0:
                level_count +=1
                enemy_types[level_count-1].remove(enemy_type)
                enemy_type = random.choice(enemy_types[level_count])
                enemy = Enemy(enemy_type)
                #def show_cutscene(screen, background_path, text_color, message, duration=5):
                if level_count == 1:
                    health_gain = 5
                    player.update_health(health_gain)
                    show_cutscene(screen,  'Images/levelup.jpg', (255 ,255 ,255) , f"You leveled up! You feel your emotions swirling inside, you feel you have more control over your emotions. Gain a small boost to your emotional buff and heal {health_gain} health!")
                    if activate_excited:
                        #Extra dmg per attack
                        excited_damage = 4
                    if activate_nervous:
                        #Each turn deal dmg
                        nervous_dmg = 5
                        nervous_selfdmg = 2
                    if activate_depressed:
                        #shield based on dmg taken
                        depressed_multiplier = 2
                    if activate_vengeful:
                        #Return percent of dmg taken
                        vengeful_multiplier = 1.50
                    if activate_optimistic:
                        add_new_cards()
                    if activate_tired:
                        player.update_health(8)


                elif level_count == 2:
                    show_cutscene(screen, 'Images/levelup.jpg', (255 ,255 ,255) , "You leveled up! You look to your left and see a small gem stone hidden in a tree. You grab it out and feel it absorb into your body. You now have +1 max mana and card draw!")
                    player.max_mana += 1
                    level_2 = True
                elif level_count == 3:
                    show_cutscene(screen, 'Images/levelup.jpg', (255 ,255 ,255), 'You leveled up! You feel your emotions swirling inside, you feel you have more control over your emotions. Gain a small boost to your emotional buff!')
                    if activate_excited:
                        excited_damage = 6
                    if activate_nervous:
                        nervous_dmg = 7
                    if activate_depressed:
                        depressed_multiplier = 1
                    if activate_vengeful:
                        vengeful_multiplier = 0.80
                    if activate_optimistic:
                        add_new_cards_2()
                    if activate_tired:
                        player.update_health(10)
                        add_new_cards_2()
            else:
                #print(enemy_types)
                enemy_types[level_count].remove(enemy_type)
                enemy_type = random.choice(enemy_types[level_count])
                #print(enemy_types)
                enemy = Enemy(enemy_type)

            print(f"Current Level: {level_count+1}")
            print(f"Selected Enemy Type: {enemy_type}")
            print(f"Enemy Types Available: {enemy_types[level_count]}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

pygame.quit()