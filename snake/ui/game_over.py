import pygame
from snake.configs import colors, game as game_configs

# Action identifiers
ACTION_PLAY_AGAIN = "ACTION_PLAY_AGAIN"
ACTION_MAIN_MENU = "ACTION_MAIN_MENU"

class GameOverScreen:
    def __init__(self, display_surface, font, final_score):
        self.display = display_surface
        self.font = font # Expecting a pygame.font.Font object
        self.final_score = final_score

        self.title_text = "Game Over!"
        self.score_display_text = f"Your Score: {self.final_score}"

        self.button_width = 250
        self.button_height = 50
        self.button_spacing = 30
        screen_center_x = self.display.get_width() // 2

        self.buttons = []
        self._setup_buttons(screen_center_x)

    def _setup_buttons(self, screen_center_x):
        """Helper method to define button properties."""
        # Position buttons below the score display
        current_y = self.display.get_height() // 2 # Start buttons around vertical center

        # Play Again Button
        self.buttons.append({
            "rect": pygame.Rect(
                screen_center_x - self.button_width // 2,
                current_y,
                self.button_width,
                self.button_height
            ),
            "text": "Play Again",
            "action": ACTION_PLAY_AGAIN,
            "color": colors.GREEN,
            "text_color": colors.BLACK
        })
        current_y += self.button_height + self.button_spacing

        # Main Menu Button
        self.buttons.append({
            "rect": pygame.Rect(
                screen_center_x - self.button_width // 2,
                current_y,
                self.button_width,
                self.button_height
            ),
            "text": "Main Menu",
            "action": ACTION_MAIN_MENU,
            "color": colors.BLUE,
            "text_color": colors.WHITE
        })

    def draw(self):
        """Draws the game over screen on the display surface."""
        self.display.fill(colors.BLACK) # Background color

        # Draw Title "Game Over!"
        title_y_pos = self.display.get_height() // 4 # Position title in the upper part
        title_surface = self.font.render(self.title_text, True, colors.RED)
        title_rect = title_surface.get_rect(center=(self.display.get_width() // 2, title_y_pos))
        self.display.blit(title_surface, title_rect)

        # Draw Score Display
        score_y_pos = title_y_pos + title_rect.height + 40 # Position score below title
        score_surface = self.font.render(self.score_display_text, True, colors.WHITE)
        score_rect = score_surface.get_rect(center=(self.display.get_width() // 2, score_y_pos))
        self.display.blit(score_surface, score_rect)

        # Draw Buttons (buttons are already positioned relative to screen center/height in _setup_buttons)
        for button in self.buttons:
            pygame.draw.rect(self.display, button["color"], button["rect"])

            text_surface = self.font.render(button["text"], True, button["text_color"])
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.display.blit(text_surface, text_rect)

        pygame.display.flip()

    def handle_event(self, event):
        """
        Handles a single Pygame event.
        Returns an action string if a button is clicked, otherwise None.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for button in self.buttons:
                    if button["rect"].collidepoint(event.pos):
                        return button["action"]
        return None

# Example usage (conceptual)
# if __name__ == '__main__':
#     pygame.init()
#     screen_width = game_configs.WIDTH
#     screen_height = game_configs.HEIGHT
#     screen = pygame.display.set_mode((screen_width, screen_height))
#     pygame.display.set_caption("Game Over Test")
#     main_font = pygame.font.SysFont("arial", 40) # Example font
#
#     # Example: Trigger game over screen
#     score_to_display = 125
#     game_over_screen = GameOverScreen(screen, main_font, score_to_display)
#
#     running = True
#     while running:
#         events = pygame.event.get()
#         for event in events:
#             if event.type == pygame.QUIT:
#                 running = False
#
#             action = game_over_screen.handle_event(event)
#             if action:
#                 print(f"Action from Game Over: {action}")
#                 if action == ACTION_PLAY_AGAIN:
#                     print("Restarting game...")
#                 elif action == ACTION_MAIN_MENU:
#                     print("Returning to main menu...")
#                 running = False # Exit test loop
#
#         game_over_screen.draw()
#         pygame.time.Clock().tick(30)
#
#     pygame.quit()
#     import sys
#     sys.exit()
