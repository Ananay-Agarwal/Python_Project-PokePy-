# defining colours (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (75, 75, 225)
LIGHTBLUE = (150, 150, 225)

# game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "PokePy"
BGCOLOR = LIGHTGREY

TILESIZE = 16
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Sound Settings
EFFECTS_SOUNDS = {'HIT_SFX_01': 'firered_000D.wav',
                  'Victory': 'Victory! (Wild Pokémon).wav.',
                  'Lose': 'Too bad.wav'}
BG_MUSIC = {'Map_Music': 'Road to Viridian City.wav',
            'Battle_Music': 'Battle! (Wild Pokémon).wav',
            'Ascension': 'Ascension.wav',
            'Final Battle': 'Final Battle.wav'}

# Player settings
PLAYER_SPEED = 300
GRASS_IMG = 'grass.png'
WALL_IMG = 'wall.png'
PLAYER_IMG = 'pokechar_down_1.png'
