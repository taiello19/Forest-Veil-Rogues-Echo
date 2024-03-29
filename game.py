import pygame
import random
import time
from tkinter import *
from tkinter import messagebox
import sys
from player import Player
from enemy import Enemy
from menu import main_menu
from popups import Popups
pygame.init()

#set the screen variable size
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

title_font = pygame.font.Font(None, 72)
font = pygame.font.Font(None, 30)

emotion_images = [pygame.image.load(f'Images/emotion{i}.png') for i in range(1, 7)]
emotion_descriptions = {
    0: "Excited, description here",
    1: "Nervous, description here",
    2: "Depressed, description here",
    3: "Vengeful, description here",
    4: "Optimistic, description here",
    5: "Tired, description here"
    # Ensure there's an entry for every emotion index
}

#-------------------------------------------------------------------------------
#PLAYERS
player = Player()




#ENEMY
enemy_types = ["wizard", "caveman", "wraith"]
enemy_type = random.choice(enemy_types)
enemy = Enemy(enemy_type)
#enemy_types.remove(enemy_type)
#print(enemy_types)

#health bars
health_bar_width = 150
health_bar_height = 15

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#MANA

font = pygame.font.Font(None, 30)


#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#CARDS
cards = [{'type': 'Attack', 'value': 5, 'mana': 1, 'name': 'Attack'},
         {'type': 'Attack', 'value': 5, 'mana': 1, 'name': 'Attack'},
         {'type': 'Attack', 'value': 5, 'mana': 1, 'name': 'Attack'},
         {'type': 'Attack', 'value': 5, 'mana': 1, 'name': 'Attack'},
         {'type': 'Attack', 'value': 5, 'mana': 1, 'name': 'Attack'},
         {'type': 'Attack', 'value': 5, 'mana': 1, 'name': 'Attack'},
         {'type': 'Attack', 'value': 5, 'mana': 1, 'name': 'Attack'},
         {'type': 'Attack', 'value': 5, 'mana': 1, 'name': 'Attack'},
         {'type': 'Defend', 'value': 5, 'mana': 1, 'name': 'Defend'},
         {'type': 'Defend', 'value': 5, 'mana': 1, 'name': 'Defend'},
         {'type': 'Defend', 'value': 5, 'mana': 1, 'name': 'Defend'},
         {'type': 'Defend', 'value': 5, 'mana': 1, 'name': 'Defend'},
         {'type': 'Defend', 'value': 5, 'mana': 1, 'name': 'Defend'},
         {'type': 'Defend', 'value': 5, 'mana': 1, 'name': 'Defend'}]


draw_pile = list(cards)  #initial draw pile 
random.shuffle(draw_pile) #shuffle the initial deck
discard_pile = [] 

player_hand = []

def draw_hand():
    card_width, card_height = 150, 180  
    for _ in range(4):
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
        0: [{'type': 'Attack', 'value': 8, 'mana': 1, 'name': 'Knife'}, {'type': 'Stun', 'value': 1, 'mana': 1, 'name': 'Stun'}],  #excited
        1: [{'type': 'Attack', 'value': 7, 'mana': 0, 'name': 'Wooden Spear'}, {'type': 'Defend', 'value': 6, 'mana': 0, 'name': 'Wooden Wall'}],  #nervous
        2: [{'type': 'Defend', 'value': 10, 'mana': 2, 'name': 'Large Shield'}, {'type': 'Dual', 'value': 8, 'mana': 1, 'name': 'Lash Out'}],  #depressed - dual = deal damage and gain half that in shield
        3: [{'type': 'Self', 'value': 2, 'mana': 2, 'name': 'Double-Edge'}, {'type': 'Dual', 'value': 6, 'mana': 1, 'name': 'Rampage'}],  #vengeful - Self = take 2 damage
        4: [{'type': 'Attack', 'value': 7, 'mana': 0, 'name': 'Slash'}, {'type': 'Defend', 'value': 7, 'mana': 0, 'name': 'Lock Down'}, {'type': 'Attack', 'value': 9, 'mana': 1, 'name': 'Bash'}],  #optimistic
        5: [{'type': 'SleepDMG', 'value': 20, 'mana': 0, 'name': 'Sleep Attack'}, {'type': 'SleepBlock', 'value': 2, 'mana': 1, 'name': 'Long Slumber'}],  #tired
        
    }

    #add the cards for the selected emotion to the deck
    if emotion_index in emotion_specific_cards:
        deck.extend(emotion_specific_cards[emotion_index])

    return deck
#-------------------------------------------------------------------------------
            

#-------------------------------------------------------------------------------
#GAME STATE         
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
enemy_turn_duration = 3  #in seconds

enemy_turn_text = None


#Emotions
#this shows that emotion class excited has been selected
activate_excited = False
#this determines the +1 dmg to atk
excited_mode = False
#this allows for the stun card to work
stun = False
#-------------------------------------------------------------------------------
 

selected_emoji_index = main_menu(screen, title_font, font, emotion_images, emotion_descriptions)
draw_pile = add_emotion_cards(draw_pile, selected_emoji_index)

if selected_emoji_index == -1:
    pygame.quit()
    sys.exit()

run = True
while run:

    #Main Menu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    key = pygame.key.get_pressed()
    screen.fill((255, 255, 255))




    #display players
    player.draw(screen)
    enemy.draw(screen)

    #display mana
    mana_text = font.render(f"{player.mana}/{player.max_mana}", True, (0, 0, 0))
    screen.blit(mana_text, (20, SCREEN_HEIGHT - 100))
    mana_rect = pygame.Rect(10, SCREEN_HEIGHT - 110, 50, 50)
    pygame.draw.rect(screen, (0, 0, 0), mana_rect, 2)

    #display player's shield and health
    player_shield_text = font.render(f"Shield: {player.shield}", True, (0, 0, 0))
    screen.blit(player_shield_text, (50, player.rect.bottom + 70))

    #enemy shield
    enemy_shield_text = font.render(f"Enemy Shield: {enemy.shield}", True, (0, 0, 0))
    screen.blit(enemy_shield_text, (SCREEN_WIDTH - 240, enemy.rect.bottom + 70))
    
    player_health_bar = pygame.Rect(50, player.rect.bottom + 10, health_bar_width * (player.health / player.max_health), health_bar_height)
    enemy_health_bar = pygame.Rect(SCREEN_WIDTH - 80 - health_bar_width * (enemy.health / enemy.max_health), enemy.rect.bottom + 10, health_bar_width * (enemy.health / enemy.max_health), health_bar_height)

    pygame.draw.rect(screen, (0, 255, 0), player_health_bar)
    pygame.draw.rect(screen, (255, 0, 0), enemy_health_bar)

    player_health_text = font.render(f"Player Health: {player.health}", True, (0, 0, 0))
    enemy_health_text = font.render(f"Enemy Health: {enemy.health}", True, (0, 0, 0))

    #display health values in text
    screen.blit(player_health_text, (50, player.rect.bottom + 40))
    screen.blit(enemy_health_text, (SCREEN_WIDTH - 240, enemy.rect.bottom + 40))

    #emotion buff in text
    if selected_emoji_index is not None:
        emotion_index = selected_emoji_index
        #different emotions giving different buffs
        if emotion_index == 0:
            additional_text = "Excited"
            activate_excited = True
        elif emotion_index == 1:
            additional_text = "Nervous"
        elif emotion_index == 2:
            additional_text = "Depressed"
        elif emotion_index == 3:
            additional_text = "Vengeful"
        elif emotion_index == 4:
            additional_text = "Optimistic"
        elif emotion_index == 5:
            additional_text = "Tired"
        else:
            additional_text = "Woopsie, something messed up, you shouldn't be here!!"
            #add code to kick them to main menu

        #display the text
        additional_text_rendered = font.render(additional_text, True, (0, 0, 0))
        screen.blit(additional_text_rendered, (50, player.rect.bottom + 100))
    

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
    start_x = (SCREEN_WIDTH - total_hand_width) // 2

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
            card_text = font.render(f"{card['name']} {card['value']}", True, (0, 0, 0))
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
            
            #go to player turn
            if pygame.time.get_ticks() - stun_message_start_time >= 1000:
                show_stun_message = False
                stun = False  
                turn_active = True  
                enemy_turn_text = None  
        else:
            if random.choice([True, False]):  #simulate enemy's decision to attack or defend
                enemy_attack_value = enemy.damage
                effective_player_damage = max(0, enemy_attack_value - player.shield)
                player.update_health(-effective_player_damage)
                player.update_shield(-enemy_attack_value)  
                enemy_turn_text = f'Enemy attacked for {enemy_attack_value}!'
                
            else:
                enemy_defend_value = 5
                enemy.update_shield(enemy_defend_value)
                enemy_turn_text = f'Enemy shielded for {enemy_defend_value}!'
            

    if enemy_turn_text is not None:
        enemy_turn_text_rendered = font.render(enemy_turn_text, True, (255, 0, 0)) 
        screen.blit(enemy_turn_text_rendered, ((SCREEN_WIDTH - enemy_turn_text_rendered.get_width()) // 2, 150))

    if turn_active:  # This condition can be adjusted based on your game's flow
        enemy_turn_text = None
    #-------------------------------------------------------------------------------------------------------------------------------------------
    #PLAYER TURN
        
    #Player turn 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

            if turn_active:
                #discard players hand and draw new cards
                discard_pile.extend(player_hand)
                player_hand.clear()
                draw_hand()
                excited_mode = False
                turn_active = False
                player.shield = 0
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
                    player.mana = player.max_mana
                    enemy.shield = 0
                    excited_mode = False
                    discard_pile.extend(player_hand)
                    player_hand.clear()
                    draw_hand()
                    turn_active = False
                    start_enemy_turn_time = time.time()


                elif use_button_rect.collidepoint(event.pos):
                    #check if a card is selected
                    if selected_card is not None and player.mana != 0:
                        #card type will determine the action taken on use button click
                        if selected_card['type'] == 'Attack':
                            #deal damage to the enemy
                            effective_damage = selected_card['value'] - enemy.shield
                            enemy.update_shield(-selected_card['value'])
                            #excited mode
                            if excited_mode == True:
                                effective_damage += 1

                            if effective_damage > 0:
                                enemy.update_health(-effective_damage)
                            if activate_excited == True and not excited_mode:
                                excited_mode = True
                        elif selected_card['type'] == 'Defend':
                            #add shield to the player
                            player.update_shield(selected_card['value'])
                        elif selected_card['type'] == 'Self':
                            print('Self type used')
                        elif selected_card['type'] == 'SleepDMG':
                            print('SleepDMG type used')
                        elif selected_card['type'] == 'Stun':
                            stun = True
                        elif selected_card['type'] == 'Dual':
                            print('Dual type used')
                        elif selected_card['type'] == 'SleepBlock':
                            print('SleepBlock type used')

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
    
    if enemy.health <= 0:
        screen.fill((255, 255, 255))  #clear the screen
        victory_text = font.render("Enemy Defeated! Click the 'X' in the top right to exit!", True, (0, 0, 0))
        screen.blit(victory_text, ((SCREEN_WIDTH - victory_text.get_width()) // 2, SCREEN_HEIGHT // 2))




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()