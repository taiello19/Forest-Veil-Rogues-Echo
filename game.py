import pygame
import random
import time
from tkinter import *
from tkinter import messagebox
import sys

pygame.init()

#set the screen variable size
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1200

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#-------------------------------------------------------------------------------
#MAIN SCREEN
#load images
emotion_images = [pygame.image.load(f'Images/emotion{i}.jpg') for i in range(1, 5)]


#main menu variables
title_font = pygame.font.Font(None, 72)
player_box_width = 120
player_box_height = 120
player_box_spacing = 20
play_button_width = 200
play_button_height = 80
in_main_menu = True


emotion_descriptions = {
    0: "Happiness, when playing an attack gain a strength buff for that turn!",
    1: "Emotion not available",
    2: "Emotion not available",
    3: "Emotion not available"
}

selected_emoji_index = -1

def main_menu():
    global selected_emoji_index  

    while in_main_menu:
        screen.fill((255, 255, 255))  #clear the screen

        #title
        title_text = title_font.render("Forest Veil: Rogue's Echo", True, (0, 0, 0))
        screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, 50))

        #intro blurb
        welcome_text = font.render("Welcome to the demo of Forest Veil: Rogue's Echo, Please select one of the emotions below and hit play to begin.", True, (0, 0, 0))
        screen.blit(welcome_text, ((SCREEN_WIDTH - welcome_text.get_width()) // 2, 450))

        welcome_text2 = font.render("Please note some emotions might not be available as the game is still in development, thank you for your patience!", True, (0, 0, 0))
        screen.blit(welcome_text2, ((SCREEN_WIDTH - welcome_text.get_width()) // 2, 500))

        #emotion boxes
        for i, emotion_img in enumerate(emotion_images):
            player_box_rect = pygame.Rect(
                (SCREEN_WIDTH - (4 * (player_box_width + player_box_spacing))) // 2 + i * (player_box_width + player_box_spacing),
                SCREEN_HEIGHT - player_box_height - 250,
                player_box_width,
                player_box_height
            )

            #border
            pygame.draw.rect(screen, (0, 0, 0), player_box_rect, 3)

            #images
            screen.blit(pygame.transform.scale(emotion_img, (player_box_width, player_box_height)), player_box_rect.topleft)

            #draw outlines
            if i == selected_emoji_index:
                pygame.draw.rect(screen, (0, 255, 0), player_box_rect, 3)

            if player_box_rect.collidepoint(pygame.mouse.get_pos()):
                #display description text
                description_text = font.render(emotion_descriptions[i], True, (0, 0, 0))
                screen.blit(description_text, ((SCREEN_WIDTH - description_text.get_width()) // 2, SCREEN_HEIGHT - 100))


        #play button
        play_button_rect = pygame.Rect(
            SCREEN_WIDTH - play_button_width - 20,
            SCREEN_HEIGHT - play_button_height - 20,
            play_button_width,
            play_button_height
        )

        #play button only allows first emotion
        if selected_emoji_index == 0:
            pygame.draw.rect(screen, (100, 200, 100), play_button_rect)
        else:
            pygame.draw.rect(screen, (150, 150, 150), play_button_rect)  

        play_button_text = title_font.render("Play", True, (0, 0, 0))
        screen.blit(play_button_text, (play_button_rect.x + 20, play_button_rect.y + 20))

        #update
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, player_box in enumerate(emotion_images):
                    player_box_rect = pygame.Rect(
                        (SCREEN_WIDTH - (4 * (player_box_width + player_box_spacing))) // 2 + i * (player_box_width + player_box_spacing),
                        SCREEN_HEIGHT - player_box_height - 250,
                        player_box_width,
                        player_box_height
                    )
                    if player_box_rect.collidepoint(event.pos):
                        selected_emoji_index = i

                if play_button_rect.collidepoint(event.pos) and selected_emoji_index == 0:
                    return  #exit the main menu loop and start the game
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#PLAYERS
player_x, player_y = 50, 250  #left side coords
enemy_x, enemy_y = 1000, 250    #right side coords

player_image = pygame.image.load('Images/Player.png')
player_image = pygame.transform.scale(player_image, (400, 400))
player_rect = player_image.get_rect(topleft=(player_x, player_y))

#ENEMY
enemy_image = pygame.image.load('Images/Enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (400, 400))
enemy_rect = enemy_image.get_rect(topleft=(enemy_x, enemy_y))


#health bars
player_health = 80
player_max_health = 80
enemy_health = 30
enemy_max_health = 80
health_bar_width = 200
health_bar_height = 20

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#MANA
current_mana = 3
max_mana = 3

font = pygame.font.Font(None, 36)


#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#CARDS
cards = [{'type': 'Attack', 'value': 5, 'mana': 1},
         {'type': 'Attack', 'value': 5, 'mana': 1},
         {'type': 'Attack', 'value': 5, 'mana': 1},
         {'type': 'Attack', 'value': 5, 'mana': 1},
         {'type': 'Attack', 'value': 5, 'mana': 1},
         {'type': 'Attack', 'value': 5, 'mana': 1},
         {'type': 'Attack', 'value': 5, 'mana': 1},
         {'type': 'Attack', 'value': 5, 'mana': 1},
         {'type': 'Defend', 'value': 5, 'mana': 1},
         {'type': 'Defend', 'value': 5, 'mana': 1},
         {'type': 'Defend', 'value': 5, 'mana': 1},
         {'type': 'Defend', 'value': 5, 'mana': 1},
         {'type': 'Defend', 'value': 5, 'mana': 1},
         {'type': 'Defend', 'value': 5, 'mana': 1}]


draw_pile = list(cards)  #initial draw pile 
random.shuffle(draw_pile) #shuffle the initial deck
discard_pile = [] 

player_hand = []

def draw_hand():
    card_width, card_height = 250, 250  
    for _ in range(4):
        if not draw_pile:
            #shuffle discard pile back into draw pile when empty
            draw_pile.extend(discard_pile)
            discard_pile.clear()
            random.shuffle(draw_pile)

        card = draw_pile.pop()
        card['rect'] = pygame.Rect(0, 0, card_width, card_height)  
        player_hand.append(card)
    

#-------------------------------------------------------------------------------
            

#-------------------------------------------------------------------------------
#GAME STATE         
draw_hand()  # player draws initial hand
turn_active = True
enemy_turn_active = False
end_turn_button_rect = pygame.Rect(SCREEN_WIDTH - 150, 10, 140, 40)
end_turn_button_text = font.render("End Turn", True, (0, 0, 0))
use_button_rect = pygame.Rect(SCREEN_WIDTH - 300, SCREEN_HEIGHT - 120, 140, 40)
use_button_text = font.render("Use", True, (0, 0, 0))
selected_card = None
player_shield = 0
enemy_shield = 0

#remove later, temporary enemy turn sim before enemy AI is added
start_enemy_turn_time = 0
enemy_turn_duration = 3  #in seconds

enemy_turn_text = None

happiness_modifier_active = False
happy_mode = False
#-------------------------------------------------------------------------------
 

run = True
while run:

    main_menu()
    in_main_menu = False

    key = pygame.key.get_pressed()
    screen.fill((255, 255, 255))




    #display players
    screen.blit(player_image, player_rect)
    screen.blit(enemy_image, enemy_rect)

    #display mana
    #print(current_mana)
    mana_text = font.render(f"{current_mana}/{max_mana}", True, (0, 0, 0))
    screen.blit(mana_text, (20, SCREEN_HEIGHT - 130))
    mana_rect = pygame.Rect(10, SCREEN_HEIGHT - 140, 50, 50)
    pygame.draw.rect(screen, (0, 0, 0), mana_rect, 2)

    #display player's shield and health
    player_shield_text = font.render(f"Shield: {player_shield}", True, (0, 0, 0))
    screen.blit(player_shield_text, (50, player_rect.bottom + 70))

    #enemy shield
    enemy_shield_text = font.render(f"Enemy Shield: {enemy_shield}", True, (0, 0, 0))
    screen.blit(enemy_shield_text, (SCREEN_WIDTH - 400, enemy_rect.bottom + 70))
    
    player_health_bar = pygame.Rect(50, player_rect.bottom + 10, health_bar_width * (player_health / player_max_health), health_bar_height)
    enemy_health_bar = pygame.Rect(SCREEN_WIDTH - 400 - health_bar_width * (enemy_health / enemy_max_health), enemy_rect.bottom + 10, health_bar_width * (enemy_health / enemy_max_health), health_bar_height)

    pygame.draw.rect(screen, (0, 255, 0), player_health_bar)
    pygame.draw.rect(screen, (255, 0, 0), enemy_health_bar)

    player_health_text = font.render(f"Player Health: {player_health}", True, (0, 0, 0))
    enemy_health_text = font.render(f"Enemy Health: {enemy_health}", True, (0, 0, 0))

    #display health values in text
    screen.blit(player_health_text, (50, player_rect.bottom + 40))
    screen.blit(enemy_health_text, (SCREEN_WIDTH - 400, enemy_rect.bottom + 40))

    #emotion buff in text
    if selected_emoji_index is not None:
        emotion_index = selected_emoji_index
        #different emotions giving different buffs
        if emotion_index == 0:
            additional_text = "+1 Strength after playing an attack card"
            happiness_modifier_active = True
        elif emotion_index == 1:
            additional_text = "Coming soon..."
        elif emotion_index == 2:
            additional_text = "Coming soon..."
        elif emotion_index == 3:
            additional_text = "Coming soon..."
        else:
            additional_text = "Woopsie, something messed up, you shouldn't be here!!"
            #add code to kick them to main menu

        #display the text
        additional_text_rendered = font.render(additional_text, True, (0, 0, 0))
        screen.blit(additional_text_rendered, (50, player_rect.bottom + 100))
    

    #draw pile and discard pile
    draw_pile_text = font.render(f"Draw Pile: {len(draw_pile)}", True, (0, 0, 0))
    discard_pile_text = font.render(f"Discard Pile: {len(discard_pile)}", True, (0, 0, 0))
    screen.blit(draw_pile_text, (10, SCREEN_HEIGHT - 80))
    screen.blit(discard_pile_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 80))

    pygame.draw.rect(screen, (100, 200, 100), use_button_rect)
    screen.blit(use_button_text, (SCREEN_WIDTH - 290, SCREEN_HEIGHT - 110))

    #card sizes
    card_width, card_height = 200, 200
    card_spacing = 20
    total_hand_width = len(player_hand) * card_width + (len(player_hand) - 1) * card_spacing
    start_x = (SCREEN_WIDTH - total_hand_width) // 2

    for i, card in enumerate(player_hand):
        card_rect = pygame.Rect(start_x + i * (card_width + card_spacing), SCREEN_HEIGHT - card_height - 20, card_width, card_height)
        card['rect'] = card_rect

        if card == selected_card:
            pygame.draw.rect(screen, (255, 255, 0), card_rect, 3)
            card_rect.y -= 5
        
        if turn_active:
            pygame.draw.rect(screen, (200, 200, 200), card_rect)
            card_text = font.render(f"{card['type']} {card['value']}", True, (0, 0, 0))
            screen.blit(card_text, (card_rect.x + 10, card_rect.y + 10))
            
            #display mana value in the top right corner of each card
            mana_text = font.render(str(card['mana']), True, (0, 0, 0))
            
            circle = pygame.Rect(card_rect.x + card_rect.width - 30, card_rect.y + 5, 24, 24)
            
            pygame.draw.ellipse(screen, (0, 0, 0), circle, 2)
            
            #display mana value
            screen.blit(mana_text, (card_rect.x + card_rect.width - 25, card_rect.y + 5))




    #display whos turn it is
    turn_text = font.render("Your Turn" if turn_active else "Enemy Turn", True, (0, 0, 0))
    screen.blit(turn_text, ((SCREEN_WIDTH - turn_text.get_width()) // 2, 10))

    if turn_active:
        pygame.draw.rect(screen, (100, 200, 100), end_turn_button_rect)
        screen.blit(end_turn_button_text, (SCREEN_WIDTH - 140, 20))

    #enemy turn
    if not turn_active and enemy_turn_text is None:
        if random.choice([True, False]):  #simulate enemy's decision to attack or defend
            enemy_attack_value = 5
            effective_player_damage = max(0, enemy_attack_value - player_shield)
            player_health -= effective_player_damage 
            player_shield = max(0, player_shield - enemy_attack_value)   
            enemy_turn_text = "Enemy attacked for 5!"
            
        else:
            enemy_defend_value = 5
            enemy_shield += enemy_defend_value
            enemy_turn_text = "Enemy shielded for 5!"
            

    if enemy_turn_text is not None:
        enemy_turn_text_rendered = font.render(enemy_turn_text, True, (255, 0, 0)) 
        screen.blit(enemy_turn_text_rendered, ((SCREEN_WIDTH - enemy_turn_text_rendered.get_width()) // 2, 150))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

            if turn_active:
                #discard players hand and draw new cards
                discard_pile.extend(player_hand)
                player_hand.clear()
                draw_hand()
                turn_active = False
                player_shield = 0
                enemy_turn_text = None
                #remove later
                start_enemy_turn_time = time.time()
            else:
                #start the player's turn again
                turn_active = True

        #check if 'End Turn' button is clicked during players turn
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if turn_active:
                if end_turn_button_rect.collidepoint(event.pos):
                    current_mana = max_mana
                    enemy_shield = 0
                    happy_mode = False
                    discard_pile.extend(player_hand)
                    player_hand.clear()
                    draw_hand()
                    turn_active = False
                    start_enemy_turn_time = time.time()


                elif use_button_rect.collidepoint(event.pos):
                    #check if a card is selected
                    if selected_card is not None and current_mana != 0:
                        #card type will determine the action taken on use button click
                        if selected_card['type'] == 'Attack':
                            #deal damage to the enemy
                            effective_enemy_damage = max(0, selected_card['value'] - enemy_shield)
                            if happy_mode:
                                effective_enemy_damage += 1
                            enemy_health -= effective_enemy_damage
                            enemy_shield = max(0, enemy_shield - selected_card['value'])
                            happy_mode = True
                        elif selected_card['type'] == 'Defend':
                            #add shield to the player
                            player_shield += selected_card['value']

                        #update mana and discard the card
                        current_mana -= selected_card['mana']
                        discard_pile.append(selected_card)
                        player_hand.remove(selected_card)
                        selected_card = None

                    else:
                        #not enough mana message, should be changed to an animation later
                        Tk().wm_withdraw()
                        messagebox.showinfo('Not enough Mana!', 'You dont have enough mana to perform this action, please hit "End Turn"')
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
            player_shield = 0
            enemy_turn_text = None
            start_enemy_turn_time = 0
    
    if enemy_health <= 0:
        screen.fill((255, 255, 255))  #clear the screen
        victory_text = font.render("Enemy Defeated! Click the 'X' in the top right to exit!", True, (0, 0, 0))
        screen.blit(victory_text, ((SCREEN_WIDTH - victory_text.get_width()) // 2, SCREEN_HEIGHT // 2))




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()