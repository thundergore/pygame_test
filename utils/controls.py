import pygame
from settings import WIDTH, HEIGHT, WHITE

def control_selection_screen(screen, font):
    screen.fill(BLACK)
    option_1 = "1. Scroll Wheel Control"
    option_2 = "2. Mouse Control"
    option_1_surface = font.render(option_1, True, WHITE)
    option_2_surface = font.render(option_2, True, WHITE)
    screen.blit(option_1_surface, (WIDTH // 2 - option_1_surface.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(option_2_surface, (WIDTH // 2 - option_2_surface.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

def select_control_method():
    control_selected = False
    while not control_selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "scroll"
                elif event.key == pygame.K_2:
                    return "mouse"

def move_paddle_scroll(scroll_amount, paddle):
    paddle.y += scroll_amount * paddle_speed
    paddle.clamp_ip(screen.get_rect())

def move_paddle_mouse(paddle):
    mouse_y = pygame.mouse.get_pos()[1]
    paddle.y = mouse_y - PADDLE_HEIGHT // 2
    paddle.clamp_ip(screen.get_rect())
