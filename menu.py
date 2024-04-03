import pygame
import sys
import time

def render_text_with_shadow(screen, font, message, position, text_color, shadow_color=(0, 0, 0), offset=(2, 2), shadow_thickness=2):
    for x in range(-shadow_thickness, shadow_thickness+1):
        for y in range(-shadow_thickness, shadow_thickness+1):
            shadow_pos = (position[0] + x, position[1] + y)
            shadow_surface = font.render(message, True, shadow_color)
            screen.blit(shadow_surface, shadow_pos)
    text_surface = font.render(message, True, text_color)
    screen.blit(text_surface, position)

def main_menu(screen, title_font, font, emotion_images, emotion_descriptions):
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    player_box_width = 150
    player_box_height = 150
    player_box_spacing = 20
    play_button_width = 200
    play_button_height = 80
    selected_emoji_index = -1
    in_main_menu = True

    while in_main_menu:
        screen.fill((255, 255, 255))  # Clear the screen
        background = pygame.image.load('Images/menubackground2.jpg').convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background, (0,0))

        # Title
        title_message = "Forest Veil: Rogue's Echo"
        title_position = ((SCREEN_WIDTH - title_font.size(title_message)[0]) // 2, 50)
        render_text_with_shadow(screen, title_font, title_message, title_position, (0, 0, 0), (255, 255, 255))

        # Intro blurb
        intro_message = "Welcome to the demo of Forest Veil: Rogue's Echo, Please select one of the emotions below and hit play to begin."
        intro_position = ((SCREEN_WIDTH - font.size(intro_message)[0]) // 2, 350)
        render_text_with_shadow(screen, font, intro_message, intro_position, (255, 255, 255))

        intro_message2 = "This game is still in beta, please feel free to give feedback to the developers!"
        intro_position2 = ((SCREEN_WIDTH - font.size(intro_message2)[0]) // 2, 400)
        render_text_with_shadow(screen, font, intro_message2, intro_position2, (255, 255, 255))

        # Emotion boxes
        for i, emotion_img in enumerate(emotion_images):
            player_box_rect = pygame.Rect(
                (SCREEN_WIDTH - (len(emotion_images) * (player_box_width + player_box_spacing))) // 2 + i * (player_box_width + player_box_spacing),
                SCREEN_HEIGHT - player_box_height - 150,
                player_box_width,
                player_box_height
            )

            pygame.draw.rect(screen, (0, 0, 0), player_box_rect, 3)  # Border
            screen.blit(pygame.transform.scale(emotion_img, (player_box_width, player_box_height)), player_box_rect.topleft)

            if i == selected_emoji_index:
                    pygame.draw.rect(screen, (0, 255, 0), player_box_rect, 3)  


            if player_box_rect.collidepoint(pygame.mouse.get_pos()):
                # Displaying emotion description with black shadow
                description_text = emotion_descriptions.get(i, "Description not available")
                description_position = (SCREEN_WIDTH - 1200 , SCREEN_HEIGHT - 100)
                render_text_with_shadow(screen, font, description_text, description_position, (255, 255, 255), (0, 0, 0))


        # Play button
        play_button_rect = pygame.Rect(SCREEN_WIDTH - play_button_width - 20, SCREEN_HEIGHT - play_button_height - 20, play_button_width, play_button_height)
        pygame.draw.rect(screen, (100, 200, 100) if selected_emoji_index != -1 else (150, 150, 150), play_button_rect)

        play_button_text = title_font.render("Play", True, (0, 0, 0))
        screen.blit(play_button_text, (play_button_rect.x + 40, play_button_rect.y + 0))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, _ in enumerate(emotion_images):
                    player_box_rect = pygame.Rect(
                        (SCREEN_WIDTH - (len(emotion_images) * (player_box_width + player_box_spacing))) // 2 + i * (player_box_width + player_box_spacing),
                        SCREEN_HEIGHT - player_box_height - 150,
                        player_box_width,
                        player_box_height
                    )
                    if player_box_rect.collidepoint(event.pos):
                        selected_emoji_index = i

                if play_button_rect.collidepoint(event.pos) and selected_emoji_index != -1:
                    in_main_menu = False  

    return selected_emoji_index