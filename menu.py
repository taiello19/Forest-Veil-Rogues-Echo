import pygame
import sys

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
        background = pygame.image.load('Images/menubackground.jpg').convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background, (0,0))

        # Title
        title_text = title_font.render("Forest Veil: Rogue's Echo", True, (255, 255, 255))
        screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, 50))

        # Intro blurb
        welcome_text = font.render("Welcome to the demo of Forest Veil: Rogue's Echo, Please select one of the emotions below and hit play to begin.", True, (255, 255, 255))
        screen.blit(welcome_text, ((SCREEN_WIDTH - welcome_text.get_width()) // 2, 350))

        welcome_text2 = font.render("Please note some emotions might not be available as the game is still in development, thank you for your patience!", True, (255, 255, 255))
        screen.blit(welcome_text2, ((SCREEN_WIDTH - welcome_text.get_width()) // 2, 400))

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
                description_text = font.render(emotion_descriptions.get(i, "Description not available"), True, (255, 255, 255))
                screen.blit(description_text, ((SCREEN_WIDTH - description_text.get_width()) // 2, SCREEN_HEIGHT - 100))


        # Play button
        play_button_rect = pygame.Rect(SCREEN_WIDTH - play_button_width - 20, SCREEN_HEIGHT - play_button_height - 20, play_button_width, play_button_height)
        pygame.draw.rect(screen, (100, 200, 100) if selected_emoji_index != -1 else (150, 150, 150), play_button_rect)

        play_button_text = title_font.render("Play", True, (0, 0, 0))
        screen.blit(play_button_text, (play_button_rect.x + 20, play_button_rect.y + 20))

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