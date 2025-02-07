import pygame
import sys

pygame.init()

# --------------- CONSTANTS ---------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

# Colors
WHITE   = (255, 255, 255)
BLACK   = (0,   0,   0)
GRAY    = (200, 200, 200)
GREEN   = (0,   255, 0)
RED     = (255, 0,   0)
BLUE    = (0,   0,   255)
YELLOW  = (255, 255, 0)

SHAPE_SIZE = 80  # bounding-box size for each shape

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shape Sorting Game")
clock = pygame.time.Clock()

# Font for the "CORRECT!" message
correct_font = pygame.font.SysFont(None, 64)

# --------------- SHAPE DRAWING FUNCTION ---------------
def draw_shape(surface, shape_type, color, x, y, size, fill=True, thickness=2):
    """
    Draws a specific shape (square, triangle, heart, star) at (x,y) with bounding size 'size'.
    If fill=False, draws an outline (use 'thickness' as line width).
    """
    if shape_type == "square":
        rect = pygame.Rect(x, y, size, size)
        if fill:
            pygame.draw.rect(surface, color, rect)
        else:
            pygame.draw.rect(surface, color, rect, thickness)

    elif shape_type == "triangle":
        # An upright triangle
        points = [
            (x + size // 2, y),           # top
            (x,            y + size),     # bottom-left
            (x + size,     y + size)      # bottom-right
        ]
        if fill:
            pygame.draw.polygon(surface, color, points)
        else:
            pygame.draw.polygon(surface, color, points, thickness)

    elif shape_type == "star":
        # A simple 5-point star in a bounding box
        cx = x + size // 2
        cy = y + size // 2
        star_points = [
            (cx,               cy - size // 2),    # top
            (cx + size // 6,   cy - size // 6),
            (cx + size // 2,   cy - size // 6),
            (cx + size // 4,   cy + size // 10),
            (cx + size // 3,   cy + size // 2),
            (cx,               cy + size // 3),
            (cx - size // 3,   cy + size // 2),
            (cx - size // 4,   cy + size // 10),
            (cx - size // 2,   cy - size // 6),
            (cx - size // 6,   cy - size // 6)
        ]
        if fill:
            pygame.draw.polygon(surface, color, star_points)
        else:
            pygame.draw.polygon(surface, color, star_points, thickness)

    elif shape_type == "heart":
        """
        Better heart shape: 
        - Two circles on top
        - Polygon (triangle) for the bottom 
        """
        radius = size // 4
        # Centers for the top circles
        top_left_center  = (x + radius,       y + radius)
        top_right_center = (x + 3*radius,     y + radius)

        if fill:
            pygame.draw.circle(surface, color, top_left_center, radius)
            pygame.draw.circle(surface, color, top_right_center, radius)
            bottom_polygon = [
                (x,        y + radius),
                (x + size, y + radius),
                (x + size//2, y + size)
            ]
            pygame.draw.polygon(surface, color, bottom_polygon)
        else:
            # Outline version
            pygame.draw.circle(surface, color, top_left_center, radius, thickness)
            pygame.draw.circle(surface, color, top_right_center, radius, thickness)
            bottom_polygon = [
                (x,        y + radius),
                (x + size, y + radius),
                (x + size//2, y + size)
            ]
            pygame.draw.polygon(surface, color, bottom_polygon, thickness)


# --------------- CLASSES ---------------
class DraggableShape:
    """
    Represents a draggable shape with:
    - shape_type ('square', 'triangle', 'heart', 'star')
    - color
    - bounding rect for collision
    - correct target_index (which placeholder it belongs to)
    """
    def __init__(self, shape_type, color, x, y, target_index):
        self.shape_type = shape_type
        self.color = color
        self.x = x
        self.y = y
        self.target_index = target_index
        self.dragging = False
        # For collision, we use a bounding box
        self.rect = pygame.Rect(x, y, SHAPE_SIZE, SHAPE_SIZE)
        self.drag_offset = (0, 0)

    def draw(self, surface):
        # Update bounding box rect
        self.rect.topleft = (self.x, self.y)
        # Draw the filled shape
        draw_shape(surface, self.shape_type, self.color, self.x, self.y, SHAPE_SIZE, fill=True)


class ShapePlaceholder:
    """
    Represents the 'cutout' area where a shape should go.
    Visually the same shape, but initially drawn as an outline.
    """
    def __init__(self, shape_type, index, x, y):
        self.shape_type = shape_type
        self.index = index
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, SHAPE_SIZE, SHAPE_SIZE)
        self.correctly_filled = False
        self.fill_color = None

    def draw(self, surface):
        if not self.correctly_filled:
            # Draw outline
            draw_shape(surface, self.shape_type, GRAY, self.x, self.y, SHAPE_SIZE, fill=False, thickness=3)
        else:
            # Filled
            draw_shape(surface, self.shape_type, self.fill_color, self.x, self.y, SHAPE_SIZE, fill=True)

    def check_collision(self, shape_rect):
        """Simple bounding box collision check."""
        return self.rect.colliderect(shape_rect)


# --------------- SETUP GAME OBJECTS ---------------
def create_game_objects():
    # Draggable shapes at the bottom
    shapes = [
        DraggableShape("square",   RED,      100, SCREEN_HEIGHT - SHAPE_SIZE - 30, 0),
        DraggableShape("triangle", BLUE,     220, SCREEN_HEIGHT - SHAPE_SIZE - 30, 1),
        DraggableShape("heart",    GREEN,    340, SCREEN_HEIGHT - SHAPE_SIZE - 30, 2),
        DraggableShape("star",     YELLOW,   460, SCREEN_HEIGHT - SHAPE_SIZE - 30, 3),
    ]

    # Matching placeholders
    placeholders = [
        ShapePlaceholder("square",   0,  100,  100),
        ShapePlaceholder("triangle", 1,  250,  100),
        ShapePlaceholder("heart",    2,  400,  100),
        ShapePlaceholder("star",     3,  550,  100),
    ]

    return shapes, placeholders

shapes, placeholders = create_game_objects()

# Restart button
RESTART_BUTTON_RECT = pygame.Rect(700, 20, 80, 40)

def reset_game():
    global shapes, placeholders, correct_message_timer
    shapes, placeholders = create_game_objects()
    correct_message_timer = 0

# Instead of a "pop" effect, we'll display "CORRECT!" for a short time
correct_message_timer = 0
CORRECT_MESSAGE_DURATION = 60  # frames to display the message

def main():
    global correct_message_timer

    while True:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()

        # --------------- EVENT HANDLING ---------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check for restart button
                if RESTART_BUTTON_RECT.collidepoint(mouse_pos):
                    reset_game()

                # Check if any shape is clicked
                for shape in shapes:
                    if shape.rect.collidepoint(mouse_pos):
                        shape.dragging = True
                        mx, my = mouse_pos
                        shape.drag_offset = (shape.x - mx, shape.y - my)
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                # Stop dragging
                for shape in shapes:
                    if shape.dragging:
                        shape.dragging = False
                        # Check if placed on correct placeholder
                        for placeholder in placeholders:
                            if placeholder.check_collision(shape.rect) and placeholder.index == shape.target_index:
                                # Correct match
                                placeholder.correctly_filled = True
                                placeholder.fill_color = shape.color
                                correct_message_timer = CORRECT_MESSAGE_DURATION

                                # Snap shape exactly to placeholder
                                shape.x = placeholder.x
                                shape.y = placeholder.y
                            # else: wrong placeholder => do nothing
            elif event.type == pygame.MOUSEMOTION:
                # Update shape position while dragging
                for shape in shapes:
                    if shape.dragging:
                        mx, my = mouse_pos
                        offset_x, offset_y = shape.drag_offset
                        shape.x = mx + offset_x
                        shape.y = my + offset_y

        # --------------- DRAW ---------------
        # Draw placeholders
        for placeholder in placeholders:
            placeholder.draw(screen)

        # Draw shapes
        for shape in shapes:
            shape.draw(screen)

        # Draw the restart button
        pygame.draw.rect(screen, GRAY, RESTART_BUTTON_RECT)
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render("Restart", True, BLACK)
        text_rect = text_surface.get_rect(center=RESTART_BUTTON_RECT.center)
        screen.blit(text_surface, text_rect)

        # If there's a "CORRECT!" message to display
        if correct_message_timer > 0:
            correct_text_surface = correct_font.render("CORRECT!", True, BLACK)
            # Draw near the top center of the screen
            cx = SCREEN_WIDTH // 2
            cy = 50
            correct_text_rect = correct_text_surface.get_rect(center=(cx, cy))
            screen.blit(correct_text_surface, correct_text_rect)
            correct_message_timer -= 1

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()