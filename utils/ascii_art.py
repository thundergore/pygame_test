import pygame
from settings import WHITE

ascii_kian = """
K I A N ' S  P O W E R F U L ,   D E A D L Y   P O N G! ! !
"""

def render_ascii_art(font, screen):
    y_offset = 20
    for line in ascii_kian.splitlines():
        text_surface = font.render(line, True, WHITE)
        screen.blit(text_surface, (20, y_offset))
        y_offset += 36
    return y_offset
