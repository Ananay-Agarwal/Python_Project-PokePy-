from os import path
import pygame as pg
from console import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.direction = 0
        self.counter = 0

    def get_keys(self):
        self.vel = vec(0, 0)
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'Assets')
        keys = pg.key.get_pressed()
        # initializing
        image_left = ['pokechar_left_1.png', 'pokechar_left_2.png', 'pokechar_left_3.png', 'pokechar_left_4.png']
        image_right = ['pokechar_right_1.png', 'pokechar_right_2.png', 'pokechar_right_3.png', 'pokechar_right_4.png']
        image_up = ['pokechar_up_1.png', 'pokechar_up_2.png', 'pokechar_up_3.png', 'pokechar_up_4.png']
        image_down = ['pokechar_down_1.png', 'pokechar_down_2.png', 'pokechar_down_3.png', 'pokechar_down_4.png']
        self.counter += 1
        self.counter %= 32
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
            self.image = pg.image.load(path.join(img_folder, image_left[int(self.counter/8)])).convert_alpha()
            self.direction = 1
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
            self.image = pg.image.load(path.join(img_folder, image_right[int(self.counter/8)])).convert_alpha()
            self.direction = 2
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
            self.image = pg.image.load(path.join(img_folder, image_up[int(self.counter/8)])).convert_alpha()
            self.direction = 3
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
            self.image = pg.image.load(path.join(img_folder, image_down[int(self.counter/8)])).convert_alpha()
            self.direction = 4
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
        # print(self.counter)

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def update(self):
        self.get_keys()
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'Assets')
        # check if player is idle
        if self.vel.x == 0 and self.vel.y == 0:
            if self.direction == 1:
                self.image = pg.image.load(path.join(img_folder, 'pokechar_left_1.png')).convert_alpha()
            if self.direction == 2:
                self.image = pg.image.load(path.join(img_folder, 'pokechar_right_1.png')).convert_alpha()
            if self.direction == 3:
                self.image = pg.image.load(path.join(img_folder, 'pokechar_up_1.png')).convert_alpha()
            if self.direction == 4:
                self.image = pg.image.load(path.join(img_folder, 'pokechar_down_1.png')).convert_alpha()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Grass(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.grass
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.grass_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
