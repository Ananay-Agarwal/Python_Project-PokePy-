from pygame import *
import pygame
from console import *
from os import path
import sqlite3
import sys

conn = sqlite3.connect('PokePy.db')
cursor = conn.cursor()


class PC:
    def __init__(self):
        self.scr = display.set_mode((1024, 768))
        self.scr.fill(LIGHTGREY)

        self.pokemon_onhand = []
        for i in range(1, 6):
            newpoke = cursor.execute('''SELECT Pokemon_Name, Level, XP, Current_HP FROM User_Pokemon
                                                WHERE On_Hand=(?)''', (i,)).fetchall()
            self.pokemon_onhand.append(newpoke[0])
        self.pokemon_not_onhand = []
        self.pokemon_not_onhand = cursor.execute('''SELECT Pokemon_Name, Level, XP, Current_HP FROM User_Pokemon
                                                    WHERE On_Hand=0''').fetchall()
        print(self.pokemon_onhand)
        print(self.pokemon_not_onhand)

    def load_screen(self):
        game_folder = path.dirname(__file__)
        poke_folder = path.join(game_folder, 'Assets\Pokemon')

        bg_img = image.load(path.join(poke_folder, 'battle_background.png'))
        bg_img2 = image.load(path.join(poke_folder, 'dialogbox_background.png'))
        self.scr.blit(bg_img, (0, 0))  # loading background
        for i in range(0, 871, 290):  # loading lower background
            self.scr.blit(bg_img2, (i, 478))
        display.update()

    def pc_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.pc_on = False

    def run_pc(self):
        self.pc_on = True
        while self.pc_on:
            self.pc_events()

    def start_pc(self):
        self.load_screen()
        self.run_pc()


# obj = PC()
# obj.start_pc()
