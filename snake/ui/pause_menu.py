import pygame
from snake.configs import colors, game as game_configs
from snake import actions # Added

# Local Action identifiers removed

class PauseMenuScreen:
    def __init__(self, display_surface, font):
        self.display = display_surface
        self.font = font # Expecting a pygame.font.Font object
        self.title_text = "Paused"

        self.button_width = 280
        self.button_height = 50
        self.button_spacing = 20
        screen_center_x = self.display.get_width() // 2

        self.buttons = []
        self._setup_buttons(screen_center_x)

    def _setup_buttons(self, screen_center_x):
        """Helper method to define button properties."""
        self.buttons = [] # Clear any previous buttons

        num_buttons = 4
        total_button_height = (num_buttons * self.button_height) + ((num_buttons - 1) * self.button_spacing)
        start_y = (self.display.get_height() - total_button_height) // 2

        button_definitions = [
            {"text": "Resume", "action": actions.ACTION_RESUME_GAME, "border_color": colors.GREEN},
            {"text": "Restart Game", "action": actions.ACTION_RESTART_GAME, "border_color": colors.GREEN},
            {"text": "Main Menu", "action": actions.ACTION_MAIN_MENU, "border_color": colors.GREEN},
            {"text": "Quit Game", "action": actions.ACTION_QUIT_GAME, "border_color": colors.RED},
        ]

        current_y = start_y
        for item in button_definitions:
            self.buttons.append({
                "rect": pygame.Rect(
                    screen_center_x - self.button_width // 2,
                    current_y,
                    self.button_width,
                    self.button_height
                ),
                "text": item["text"],
                "action": item["action"],
                "base_color": colors.BLACK,
                "text_color": colors.WHITE,
                "border_color": item["border_color"]
            })
            current_y += self.button_height + self.button_spacing

    def draw(self):
        """Draws the pause menu screen on the display surface."""
        self.display.fill(colors.BLACK) # Screen background

        # Draw Title "Paused"
        title_y_pos = self.display.get_height() // 4
        title_surface = self.font.render(self.title_text, True, colors.WHITE)
        title_rect = title_surface.get_rect(center=(self.display.get_width() // 2, title_y_pos))
        self.display.blit(title_surface, title_rect)

        # Draw Buttons
        border_thickness = 3
        for button in self.buttons:
            pygame.draw.rect(self.display, button["base_color"], button["rect"]) # Button face
            pygame.draw.rect(self.display, button["border_color"], button["rect"], border_thickness) # Border

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
#     pygame.display.set_caption("Pause Menu Test")
#     main_font = pygame.font.SysFont("arial", 40)
#
#     pause_menu = PauseMenuScreen(screen, main_font)
#
#     running = True
#     while running:
#         events = pygame.event.get()
#         for event in events:
#             if event.type == pygame.QUIT:
#                 running = False
#
#             action = pause_menu.handle_event(event)
#             if action:
#                 print(f"Action from Pause Menu: {action}")
#                 if action == ACTION_QUIT_GAME: # Example of handling one action
#                     running = False
#                 # Handle other actions based on what AppController would do
#
#         pause_menu.draw()
#         pygame.time.Clock().tick(30)
#
#     pygame.quit()
#     import sys
#     sys.exit()
