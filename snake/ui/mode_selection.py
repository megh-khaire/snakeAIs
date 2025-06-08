import pygame
from snake.configs import colors, game as game_configs
from snake import actions # Added

# Local Action/Mode identifiers removed, will use actions.<...>


class ModeSelectionScreen:
    def __init__(self, display_surface, font):
        self.display = display_surface
        self.font = font
        self.title_text = "Select Game Mode"

        # self.button_width will be set in _setup_buttons based on current display width
        self.button_height = 40
        self.button_spacing = 15  # Vertical spacing between buttons
        # screen_center_x will be derived from self.display in _setup_buttons

        self.mode_buttons = []
        self.back_button = {}
        self._setup_buttons() # screen_center_x no longer needed as param

    def _setup_buttons(self): # screen_center_x removed as param
        """Helper method to define button properties."""
        screen_width = self.display.get_width()
        screen_center_x = screen_width // 2
        self.button_width = screen_width // 2 # Responsive button width

        # Clear existing buttons before recalculating
        self.mode_buttons = []
        self.back_button = {} # Also clear back_button if it's redefined here

        start_y = 80  # Starting y-position for the first button, below title
        current_y = start_y

        game_modes_data = [
            # ("Manual", actions.MODE_MANUAL), # Removed, but if re-added, use actions.MODE_MANUAL
            ("A* Search", actions.MODE_ASTAR),
            ("Best-First Search", actions.MODE_BEST_FS),
            ("Breadth-First Search (BFS)", actions.MODE_BFS),
            ("Depth-First Search (DFS)", actions.MODE_DFS),
            ("Simple Hill Climbing", actions.MODE_SIMPLE_HILL_CLIMBING),
            ("Steepest Ascent Hill Climbing", actions.MODE_STEEPEST_ASCENT_HILL_CLIMBING),
            ("Stochastic Hill Climbing", actions.MODE_STOCHASTIC_HILL_CLIMBING),
            ("Random Search", actions.MODE_RANDOM) # Changed from MODE_RANDOM_SEARCH
        ]

        for text, action in game_modes_data:
            self.mode_buttons.append({
                "rect": pygame.Rect(
                    screen_center_x - self.button_width // 2,
                    current_y,
                    self.button_width,
                    self.button_height
                ),
                "text": text,
                "action": action,
                "base_color": colors.BLACK,
                "text_color": colors.WHITE,
                "border_color": colors.GREEN # Standard green border for all mode buttons
            })
            current_y += self.button_height + self.button_spacing

        # Back Button
        current_y += self.button_spacing # Extra space before back button
        self.back_button = {
            "rect": pygame.Rect(
                screen_center_x - self.button_width // 2,
                current_y,
                self.button_width,
                self.button_height
            ),
            "text": "Back to Main Menu",
            "action": actions.ACTION_BACK_TO_MENU,
            "base_color": colors.BLACK,
            "text_color": colors.WHITE,
            "border_color": colors.RED # Distinct red border for Back button
        }

    def on_resize(self, new_display_surface):
        """Handles window resize events to adapt the layout."""
        self.display = new_display_surface
        self._setup_buttons() # Recalculate layout

    def draw(self):
        """Draws the mode selection screen on the display surface."""
        self.display.fill(colors.BLACK) # Screen background

        # Draw Title
        title_surface = self.font.render(self.title_text, True, colors.WHITE)
        title_rect = title_surface.get_rect(center=(self.display.get_width() // 2, 40)) # Title higher up
        self.display.blit(title_surface, title_rect)

        # Draw Mode Buttons
        for button in self.mode_buttons:
            pygame.draw.rect(self.display, button["base_color"], button["rect"])
            pygame.draw.rect(self.display, button["border_color"], button["rect"], 3) # Border
            text_surface = self.font.render(button["text"], True, button["text_color"])
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.display.blit(text_surface, text_rect)

        # Draw Back Button
        pygame.draw.rect(self.display, self.back_button["base_color"], self.back_button["rect"])
        pygame.draw.rect(self.display, self.back_button["border_color"], self.back_button["rect"], 3) # Border
        back_text_surface = self.font.render(self.back_button["text"], True, self.back_button["text_color"])
        back_text_rect = back_text_surface.get_rect(center=self.back_button["rect"].center)
        self.display.blit(back_text_surface, back_text_rect)

        pygame.display.flip()

    def handle_event(self, event):
        """
        Handles a single Pygame event.
        Returns an action string (game mode identifier or navigation action) if a button is clicked, otherwise None.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for button in self.mode_buttons:
                    if button["rect"].collidepoint(event.pos):
                        return button["action"] # Return the game mode identifier

                if self.back_button["rect"].collidepoint(event.pos):
                    return self.back_button["action"] # Return "BACK_TO_MENU"
        return None

# Example usage (conceptual)
# if __name__ == '__main__':
#     pygame.init()
#     screen_width = game_configs.WIDTH
#     screen_height = game_configs.HEIGHT
#     # Adjust screen height if too many buttons for default
#     # For testing, might need a taller screen if all buttons are listed vertically
#     # screen_height = 800 # Example for testing
#     screen = pygame.display.set_mode((screen_width, screen_height))
#     pygame.display.set_caption("Mode Selection Test")
#     main_font = pygame.font.SysFont("arial", 30) # Example font
#
#     mode_screen = ModeSelectionScreen(screen, main_font)
#
#     running = True
#     while running:
#         events = pygame.event.get()
#         for event in events:
#             if event.type == pygame.QUIT:
#                 running = False
#
#             action = mode_screen.handle_event(event)
#             if action:
#                 print(f"Action: {action}")
#                 if action == ACTION_BACK_TO_MENU:
#                     print("Going back to main menu...")
#                     running = False
#                 elif action.startswith("MODE_"):
#                     print(f"Selected game mode: {action}")
#                     # Here, you would typically signal the main controller to start this game mode
#                     running = False # Or switch state
#
#         mode_screen.draw()
#         pygame.time.Clock().tick(30)
#
#     pygame.quit()
#     import sys
#     sys.exit()
