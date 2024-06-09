from .textures import create_paddle_texture, create_ball_texture, create_powerup_texture, create_net_texture
from settings import PADDLE_WIDTH, PADDLE_HEIGHT, BALL_RADIUS, POWERUP_SIZE, NET_SIZE

def load_assets():
    global paddle_texture, ball_texture, powerup_texture, net_texture
    paddle_texture = create_paddle_texture(PADDLE_WIDTH, PADDLE_HEIGHT)
    ball_texture = create_ball_texture(BALL_RADIUS)
    powerup_texture = create_powerup_texture(POWERUP_SIZE)
    net_texture = create_net_texture(NET_SIZE)
