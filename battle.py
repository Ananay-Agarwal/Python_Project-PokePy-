from pygame import *
from console import *
from os import path


def AAfilledRoundedRect(surface, rect, color, radius=0.4):
    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)
    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """
    rect = Rect(rect)
    color = Color(*color)
    alpha = color.a
    color.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = Surface(rect.size, SRCALPHA)
    circle = Surface([min(rect.size) * 3] * 2, SRCALPHA)
    draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
    circle = transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)
    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)
    rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
    rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))
    rectangle.fill(color, special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=BLEND_RGBA_MIN)
    return surface.blit(rectangle, pos)


def load_battle():
    game_folder = path.dirname(__file__)
    poke_folder = path.join(game_folder, 'Assets\Pokemon')
    scr = display.set_mode((1024, 768))
    BG = LIGHTGREY
    scr.fill(BG)
    bg_img = image.load(path.join(poke_folder, 'battle_background.png'))
    bg_img2 = image.load(path.join(poke_folder, 'dialogbox_background.png'))
    user_poke = image.load(path.join(poke_folder, 'bulbasaur_back.png'))
    opp_poke = image.load(path.join(poke_folder, 'bulbasaur_front.png'))

    scr.blit(bg_img, (0, 0))  # loading background
    for i in range(0, 871, 290):  # loading lower background
        scr.blit(bg_img2, (i, 478))

    # loading black borders on dialog boxes
    AAfilledRoundedRect(scr, (20, 20, 470, 120), BLACK, 0.5)
    AAfilledRoundedRect(scr, (530, 340, 470, 120), BLACK, 0.5)
    AAfilledRoundedRect(scr, (5, 485, 1010, 270), BLACK, 0.3)

    # loading status boxes
    AAfilledRoundedRect(scr, (30, 30, 450, 100), WHITE, 0.5)
    AAfilledRoundedRect(scr, (540, 350, 450, 100), WHITE, 0.5)
    # pygame.draw.rect(scr, (255,255,255), (0, 290, 500, 109))

    # loading pokemon sprites
    scr.blit(user_poke, (150, 350))
    scr.blit(opp_poke, (690, 140))

    # loading main dialog box
    AAfilledRoundedRect(scr, (10, 490, 1000, 260), BLUE, 0.3)
    display.update()
    while event.wait().type != QUIT: pass


load_battle()
