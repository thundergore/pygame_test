# game/leaderboard.py

import os
import json

LEADERBOARD_FILE = "leaderboard.json"

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

def display_leaderboard(screen, font):
    leaderboard = load_leaderboard()
    screen.fill((0, 0, 0))
    title_surface = font.render("Leaderboard", True, (255, 255, 255))
    screen.blit(
        title_surface,
        (screen.get_width() // 2 - title_surface.get_width() // 2, 50),
    )
    for i, entry in enumerate(leaderboard[:20]):
        score_surface = font.render(f"{i+1}. {entry['name']} - {entry['score']}", True, (255, 255, 255))
        screen.blit(
            score_surface,
            (screen.get_width() // 2 - score_surface.get_width() // 2, 100 + i * 30),
        )
    pygame.display.flip()
