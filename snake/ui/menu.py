import pygame

from snake.configs import (
    actions,
    colors,
)


class MainMenu:
    def __init__(self, display_surface, font):
        self.display = display_surface
        self.font = font
        self.title_text = "Snake AI Game"

        self.button_width = 250  # Adjusted width
        self.button_height = 50
        self.button_spacing = 20  # Adjusted vertical spacing
        screen_center_x = self.display.get_width() // 2

        self.buttons = []
        self._setup_buttons(screen_center_x)

    def _setup_buttons(self, screen_center_x):
        """Helper method to define button properties."""
        self.buttons = []  # Clear any previous buttons

        start_y = (
            self.display.get_height() // 2
            - (self.button_height * 3 + self.button_spacing * 2) // 2
        )

        button_texts_actions_borders = [
            ("Play Game", actions.ACTION_PLAY_MANUAL, colors.BLUE),
            ("Select Algorithm", actions.ACTION_SELECT_ALGORITHM, colors.GREEN),
            ("Quit", actions.ACTION_QUIT_GAME, colors.RED),
        ]

        current_y = start_y
        for text, action, border_color_val in button_texts_actions_borders:
            self.buttons.append(
                {
                    "rect": pygame.Rect(
                        screen_center_x - self.button_width // 2,
                        current_y,
                        self.button_width,
                        self.button_height,
                    ),
                    "text": text,
                    "action": action,
                    "base_color": colors.BLACK,  # Button face color
                    "text_color": colors.WHITE,
                    "border_color": border_color_val,  # Specific border color for this button
                }
            )
            current_y += self.button_height + self.button_spacing

    def draw(self):
        """Draws the main menu on the display surface."""
        self.display.fill(colors.BLACK)

        # Draw Title
        # Assuming self.font is a pygame.font.Font object
        title_surface = self.font.render(self.title_text, True, colors.WHITE)
        title_rect = title_surface.get_rect(
            center=(self.display.get_width() // 2, 100)
        )  # Y pos for title
        self.display.blit(title_surface, title_rect)

        # Draw Buttons
        for button in self.buttons:
            # Draw the black background of the button
            pygame.draw.rect(self.display, button["base_color"], button["rect"])
            # Draw the colored border around it
            pygame.draw.rect(
                self.display, button["border_color"], button["rect"], 3
            )  # border_thickness = 3

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
