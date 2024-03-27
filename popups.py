import pygame

class Popups:
    def __init__(self, screen, message):
        self.screen = screen
        self.message = message
        self.font = pygame.font.Font(None, 40)
        self.popup_surf = self.font.render(message, True, (255, 255, 255))
        self.popup_rect = self.popup_surf.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        self.button_font = pygame.font.Font(None, 30)
        self.button_text = self.button_font.render('Close', True, (255, 255, 255))
        self.button_rect = pygame.Rect(0, 0, 100, 50)
        self.button_rect.center = (self.popup_rect.centerx, self.popup_rect.bottom + 30)

    def show(self):
        background_surf = pygame.Surface(self.screen.get_size())
        background_surf.set_alpha(128)  
        background_surf.fill((0, 0, 0)) 
        self.screen.blit(background_surf, (0, 0))

        pygame.draw.rect(self.screen, (0, 0, 255), self.popup_rect.inflate(20, 20))  
        self.screen.blit(self.popup_surf, self.popup_rect)  

        pygame.draw.rect(self.screen, (100, 100, 100), self.button_rect)  
        self.screen.blit(self.button_text, (self.button_rect.x + 10, self.button_rect.y + 10))

        pygame.display.flip()  

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                        waiting_for_input = False
                elif event.type == pygame.QUIT:
                    waiting_for_input = False
                    pygame.quit()