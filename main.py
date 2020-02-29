import pygame as pg
import sys
from console import *
from sprites import *
from os import path
from tilemap import *
from battle import *


class Game:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        icon = pg.image.load('Assets\Pokeball.png')
        pg.display.set_icon(icon)
        self.clock = pg.time.Clock()
        self.load_data()
        self.battle = Battle()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'Assets')
        map_folder = path.join(img_folder, 'Maps')
        self.map = TiledMap(path.join(map_folder, 'Hometown.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.grass_img = pg.image.load(path.join(img_folder, GRASS_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.type == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.battle_encounter = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
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
            self.battle.load_battle()
            self.new()
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
            if 585 <= self.player.pos.x <= 600 and self.player.pos.y == 989:
                if event.key == pg.K_e:
                    self.battle_encounter = not self.battle_encounter

    def show_start_screen(self):
        pass


gameobj = Game()
gameobj.show_start_screen()

while True:
    gameobj.new()
    gameobj.run()
