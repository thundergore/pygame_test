import json
import os
import pygame
from settings import LEADERBOARD_FILE, WIDTH, HEIGHT, WHITE, BLACK

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE) and os.path.getsize(LEADERBOARD_FILE) > 0:
        try:
            with open(LEADERBOARD_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, 'w') as file:
        json.dump(leaderboard, file)

def update_leaderboard(name, new_score):
    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "score": new_score})
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    if len(leaderboard) > 20:
        leaderboard.pop()
    save_leaderboard(leaderboard)

def display_leaderboard(screen, font, leaderboard):
    screen.fill(BLACK)
    title_surface = font.render("Leaderboard", True, WHITE)
    screen.blit(
        title_surface,
        (WIDTH // 2 - title_surface.get_width() // 2, 50),
    )
    for i, entry in enumerate(leaderboard[:20]):
        score_surface = font.render(f"{i+1}. {entry['name']} - {entry['score']}", True, WHITE)
        screen.blit(
            score_surface,
            (WIDTH // 2 - score_surface.get_width() // 2, 100 + i * 30),
        )
    pygame.display.flip()

def get_player_name(screen, font):
    name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        screen.fill(BLACK)
        name_surface = font.render(f"Enter your name: {name}", True, WHITE)
        screen.blit(name_surface, (WIDTH // 2 - name_surface.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
    return name
