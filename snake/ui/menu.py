import pygame
from snake.configs import colors, game as game_configs

# Action identifiers (can be replaced by an enum or GameState later)
ACTION_SELECT_MODE = "SELECT_MODE"
ACTION_QUIT_GAME = "QUIT_GAME"
ACTION_SHOW_HIGH_SCORES = "SHOW_HIGH_SCORES" # Example for future use
ACTION_OPTIONS = "OPTIONS"                 # Example for future use

class MainMenu:
    def __init__(self, display_surface, font):
        self.display = display_surface
        self.font = font
        self.title_text = "Snake AI Game"

        self.button_width = 300
        self.button_height = 50
        self.button_spacing = 30  # Vertical spacing between buttons
        screen_center_x = self.display.get_width() // 2

        self.buttons = []
        self._setup_buttons(screen_center_x)

    def _setup_buttons(self, screen_center_x):
        """Helper method to define button properties."""
        start_y = 200  # Starting y-position for the first button

        # Select Game Mode Button
        self.buttons.append({
            "rect": pygame.Rect(
                screen_center_x - self.button_width // 2,
                start_y,
                self.button_width,
                self.button_height
            ),
            "text": "Select Game Mode",
            "action": ACTION_SELECT_MODE,
            "color": colors.GREEN,
            "text_color": colors.BLACK
        })

        # High Scores Button (example)
        # start_y += self.button_height + self.button_spacing
        # self.buttons.append({
        #     "rect": pygame.Rect(
        #         screen_center_x - self.button_width // 2,
        #         start_y,
        #         self.button_width,
        #         self.button_height
        #     ),
        #     "text": "High Scores",
        #     "action": ACTION_SHOW_HIGH_SCORES,
        #     "color": colors.BLUE, # Different color for example
        #     "text_color": colors.WHITE
        # })

        # Quit Game Button
        start_y += self.button_height + self.button_spacing # Adjust y for next button
        self.buttons.append({
            "rect": pygame.Rect(
                screen_center_x - self.button_width // 2,
                start_y,
                self.button_width,
                self.button_height
            ),
            "text": "Quit Game",
            "action": ACTION_QUIT_GAME,
            "color": colors.RED,
            "text_color": colors.WHITE
        })

    def draw(self):
        """Draws the main menu on the display surface."""
        self.display.fill(colors.BLACK)

        # Draw Title
        # Assuming self.font is a pygame.font.Font object
        title_surface = self.font.render(self.title_text, True, colors.WHITE)
        title_rect = title_surface.get_rect(center=(self.display.get_width() // 2, 100))
        self.display.blit(title_surface, title_rect)

        # Draw Buttons
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

# Example usage (conceptual, for testing this file directly if needed)
# if __name__ == '__main__':
#     pygame.init()
#     screen_width = game_configs.WIDTH
#     screen_height = game_configs.HEIGHT
#     screen = pygame.display.set_mode((screen_width, screen_height))
#     pygame.display.set_caption("Main Menu Test")
#     main_font = pygame.font.SysFont("arial", 40) # Example font
#
#     menu = MainMenu(screen, main_font)
#
#     running = True
#     while running:
#         events = pygame.event.get()
#         for event in events:
#             if event.type == pygame.QUIT:
#                 running = False
#
#             action = menu.handle_event(event)
#             if action:
#                 print(f"Action: {action}")
#                 if action == ACTION_QUIT_GAME:
#                     running = False
#                 # Handle other actions (e.g., switch to game mode selection screen)
#
#         menu.draw()
#         pygame.time.Clock().tick(30) # Limit FPS
#
#     pygame.quit()
#     import sys
#     sys.exit()
