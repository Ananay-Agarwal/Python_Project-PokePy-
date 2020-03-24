from sprites import *
from tilemap import *
import sqlite3

conn = sqlite3.connect('PokePy.db')
cursor = conn.cursor()


class Game:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        icon = pg.image.load('Assets\Pokeball.png')
        pg.display.set_icon(icon)
        self.clock = pg.time.Clock()
        self.current_map = 'Hometown.tmx'
        self.load_data()
        self.battle = Battle()
        self.draw_debug = False
        self.battle_encounter = False
        # Loading Sounds
        game_folder = path.dirname(__file__)
        sound_folder = path.join(game_folder, 'Sound Files')
        self.bg_music = {}
        for sound_type in BG_MUSIC:
            self.bg_music[sound_type] = pg.mixer.Sound(path.join(sound_folder, BG_MUSIC[sound_type]))
            self.bg_music[sound_type].set_volume(0.5)
        self.sound_effects = {}
        for sound_type in EFFECTS_SOUNDS:
            self.sound_effects[sound_type] = pg.mixer.Sound(path.join(sound_folder, EFFECTS_SOUNDS[sound_type]))

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'Assets')
        map_folder = path.join(img_folder, 'Maps')
        self.map = TiledMap(path.join(map_folder, self.current_map))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.type == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'player' and not self.battle_encounter:  # on game start
                self.player = Player(self, tile_object.x, tile_object.y)
            elif tile_object.name == 'player' and self.battle_encounter:  # after battle encounter
                self.player = Player(self, self.player.pos.x, self.player.pos.y)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        self.bg_music['Map_Music'].play(-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(wall.rect), 1)
            pg.draw.rect(self.screen, RED, self.camera.apply_rect(self.player.rect), 1)
        if self.battle_encounter:
            self.bg_music['Map_Music'].stop()
            self.battle.start_battle()
            self.bg_music['Map_Music'].play(-1)
            self.new()
            self.battle_encounter = False

        pg.display.flip()

    def quit(self):
        pg.quit()
        sys.exit()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                # Interact check
                if event.key == pg.K_e:
                    if self.current_map == "Hometown.tmx":
                        if 580 <= self.player.pos.x <= 600 and 980 <= self.player.pos.y <= 995:
                            self.current_map = "House.tmx"
                            self.load_data()
                            self.new()
                    elif self.current_map == "House.tmx":
                        if 512 <= self.player.pos.x <= 576 and self.player.pos.y == 690:
                            self.current_map = "Hometown.tmx"
                            self.load_data()
                            self.new()
                        if 530 <= self.player.pos.x <= 560 and self.player.pos.y == 159:
                            print("Pokemon healed")
                            cursor.execute('''UPDATE User_Pokemon SET Current_HP=
                            (SELECT HP FROM Pokemon WHERE Pokemon.Pokemon_Name = User_Pokemon.Pokemon_Name)''')
                            conn.commit()
                        if 340 <= self.player.pos.x <= 360 and self.player.pos.y == 127:
                            print("pc opened")
            # Battle check
            if 1400 <= self.player.pos.x <= 1800 and 1200 <= self.player.pos.y <= 1550 \
                    and self.current_map == "Hometown.tmx":
                if self.player.encounter_chance > 8 and (self.player.vel.x != 0 or self.player.vel.y != 0):
                    self.battle_encounter = True

    def show_start_screen(self):
        pass


gameobj = Game()
gameobj.show_start_screen()

while True:
    gameobj.new()
    gameobj.run()
