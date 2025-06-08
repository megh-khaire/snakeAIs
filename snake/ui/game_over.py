import pygame
from snake.configs import colors, game as game_configs
from snake import actions # Added

# Local Action identifiers removed

class GameOverScreen:
    def __init__(self, display_surface, font, final_score):
        self.display = display_surface
        self.font = font # Expecting a pygame.font.Font object
        self.final_score = final_score

        self.title_text = "Game Over!"
        self.score_display_text = f"Your Score: {self.final_score}"

        # Button dimensions will be set in _setup_buttons
        self.button_height = 50
        self.button_spacing = 30
        # screen_center_x will be derived from self.display in _setup_buttons

        self.buttons = []
        self._setup_buttons() # screen_center_x no longer needed

    def _setup_buttons(self): # screen_center_x removed
        """Helper method to define button properties."""
        screen_width = self.display.get_width()
        screen_center_x = screen_width // 2
        self.button_width = min(screen_width * 0.5, 300) # Responsive width, capped

        self.buttons = [] # Clear buttons before repopulating

        # Position buttons below the score display, centered vertically as a group
        num_buttons = 2
        total_button_block_height = (num_buttons * self.button_height) + ((num_buttons - 1) * self.button_spacing)

        # Calculate y for score text (already responsive in draw)
        title_y_pos = self.display.get_height() // 4
        # Assuming font size for title_rect.height is roughly 40-50 for estimation
        estimated_title_height = 50 # Estimate, or use font.size(text)[1] if font available here
        score_y_pos = title_y_pos + estimated_title_height + 40

        # Start buttons below the score text area
        current_y = score_y_pos + 50 # Add some space after score text

        # If buttons go too low, adjust start or use a more dynamic centering for the block
        if current_y + total_button_block_height > self.display.get_height() - self.button_spacing:
             current_y = self.display.get_height() - total_button_block_height - self.button_spacing # Place from bottom up

        # Play Again Button
        self.buttons.append({
            "rect": pygame.Rect(
                screen_center_x - self.button_width // 2,
                current_y,
                self.button_width,
                self.button_height
            ),
            "text": "Play Again",
            "action": actions.ACTION_PLAY_AGAIN,
            "base_color": colors.BLACK,
            "text_color": colors.WHITE,
            "border_color": colors.GREEN
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
            "action": actions.ACTION_MAIN_MENU,
            "base_color": colors.BLACK,
            "text_color": colors.WHITE,
            "border_color": colors.GREEN
        })

    def on_resize(self, new_display_surface):
        """Handles window resize events to adapt the layout."""
        self.display = new_display_surface
        # Score text needs to be updated if final_score can change, but it's fixed per instance.
        # Re-setup buttons for new screen dimensions.
        self._setup_buttons()

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
            pygame.draw.rect(self.display, button["base_color"], button["rect"])
            pygame.draw.rect(self.display, button["border_color"], button["rect"], 3) # Border

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
