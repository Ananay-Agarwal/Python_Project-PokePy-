from pygame import *
from console import *
from os import path
import random
import pygame
import sqlite3
import sys

conn = sqlite3.connect('PokePy.db')
cursor = conn.cursor()
attack_cursor = conn.cursor()
user_hp_cursor = conn.cursor()
enemy_hp_cursor = conn.cursor()
pygame.init()

font = pygame.font.SysFont('sans', 32)


class Battle:
    def __init__(self):
        self.battle_playing = True
        self.attack_selected = False

        self.pokemon_list = ['Bulbasaur', 'Charmander', 'Squirtle', 'Pidgey', 'Pikachu', 'Onix']
        self.player_poke_name = 'Pikachu'
        self.opp_poke_name = random.choice(self.pokemon_list)
        self.opponent_health=0
        self.opp_health = cursor.execute('SELECT HP from Pokemon where Pokemon_Name=(?)', (self.opp_poke_name,)).fetchall()
        for health in self.opp_health:
            self.opponent_health = int(health[0])

        self.player_health = 274 #Needs to be changed
        self.max_player_health = self.player_health  # fetch
        self.max_opponent_health = self.opponent_health  # fetch

        self.scr = display.set_mode((1024, 768))
        self.scr.fill(LIGHTGREY)

    def AAfilledRoundedRect(self, surface, rect, color, radius=0.4):
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

    def draw_health_bar(self, health, max_health, x, y, w, h):
        if health > (0.75 * max_health):
            col = GREEN
        elif health > (0.40 * max_health):
            col = YELLOW
        else:
            col = RED
        width = int(w * health / max_health)
        health_bar = Rect(x, y, width, h)
        draw.rect(self.scr, col, health_bar)

    def print_text(self, msg, x, y, colour):
        text = font.render(msg, True, colour)
        self.scr.blit(text, [x, y])

    def load_battle(self):
        self.opp_poke_name = random.choice(self.pokemon_list)
        game_folder = path.dirname(__file__)
        poke_folder = path.join(game_folder, 'Assets\Pokemon')

        bg_img = image.load(path.join(poke_folder, 'battle_background.png'))
        bg_img2 = image.load(path.join(poke_folder, 'dialogbox_background.png'))

        user_poke = image.load(path.join(poke_folder, self.player_poke_name + '_back.png'))
        opp_poke = image.load(path.join(poke_folder, self.opp_poke_name + '_front.png'))

        self.scr.blit(bg_img, (0, 0))  # loading background
        for i in range(0, 871, 290):  # loading lower background
            self.scr.blit(bg_img2, (i, 478))

        # loading black borders on dialog boxes
        self.AAfilledRoundedRect(self.scr, (20, 20, 470, 120), BLACK, 0.5)
        self.AAfilledRoundedRect(self.scr, (530, 340, 470, 120), BLACK, 0.5)
        self.AAfilledRoundedRect(self.scr, (5, 485, 1010, 270), BLACK, 0.3)

        # loading status boxes
        self.AAfilledRoundedRect(self.scr, (30, 30, 450, 100), WHITE, 0.5)
        self.AAfilledRoundedRect(self.scr, (540, 350, 450, 100), WHITE, 0.5)

        # printing details
        self.print_text(self.player_poke_name, 570, 360, BLACK)
        self.print_text(self.opp_poke_name, 60, 40, BLACK)

        # drawing health bars
        # opponent health bar
        self.AAfilledRoundedRect(self.scr, (196, 86, 258, 18), BLACK, 0.7)
        self.AAfilledRoundedRect(self.scr, (200, 90, 250, 10), LIGHTGREY, 0.5)
        self.draw_health_bar(self.opponent_health, self.max_opponent_health, 200, 90, 250, 10)

        # player health bar
        self.AAfilledRoundedRect(self.scr, (696, 406, 258, 18), BLACK, 0.7)
        self.AAfilledRoundedRect(self.scr, (700, 410, 250, 10), LIGHTGREY, 0.5)
        self.draw_health_bar(self.player_health, self.max_player_health, 700, 410, 250, 10)

        # loading pokemon sprites
        self.scr.blit(user_poke, (150, 478 - user_poke.get_height()))
        self.scr.blit(opp_poke, (700, 270 - opp_poke.get_height()))

        # loading main dialog box
        self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
        self.print_text("A wild Pokemon has appeared!! what do you want to do?", 20, 500, WHITE)
        self.print_text("1. Attack", 20, 550, WHITE)
        self.print_text("2. Flee", 180, 550, WHITE)
        self.print_text("3. Inventory", 20, 590, WHITE)
        self.print_text("4. Shop", 200, 590, WHITE)
        display.update()
        self.battle_run()
        # while event.wait().type != QUIT and self.opponent_health != 0 and self.player_health != 0 and pygame.event != pygame.K_ESCAPE:
        #    pass

    def battle_run(self):
        # game loop - set self.playing = False to end the game
        while self.battle_playing:
            self.battle_events()
            self.battle_update()
            # self.draw()

    def quit_battle(self):
        self.battle_playing = False

    def battle_update(self):
        display.update()

    def battle_events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_battle()
            elif event.type == pygame.KEYDOWN:
                if self.opponent_health >= 1 and self.player_health >= 1:
                    x = attack_cursor.execute('''SELECT Move1 , Move2 , Move3 , Move4 from 
                                            Pokemon where Pokemon_Name=(?)''',
                                          (self.player_poke_name,)).fetchall()

                    if not self.attack_selected:
                        if event.key == pygame.K_1:
                            self.display_attacks(x)
                        if event.key == pygame.K_2:
                            self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
                            self.print_text("Items opened", 500, 520, WHITE)
                    else:
                        if event.key == pygame.K_1:
                            self.player_attack(x,0)
                            time.delay(1000)
                            # self.check_health()
                            # time.delay(1000)
                            self.opponent_attack()
                            # time.delay(1000)
                            # self.check_health()
                            time.delay(1000)
                            self.display_attacks(x)
                        elif event.key == pygame.K_2:
                                self.player_attack(x, 1)
                                time.delay(1000)
                                # self.check_health()
                                # time.delay(1000)
                                self.opponent_attack()
                                # time.delay(1000)
                                # self.check_health()
                                time.delay(1000)
                                self.display_attacks(x)
                        elif event.key == pygame.K_3:
                                self.player_attack(x, 2)
                                time.delay(1000)
                                # self.check_health()
                                # time.delay(1000)
                                self.opponent_attack()
                                # time.delay(1000)
                                # self.check_health()
                                time.delay(1000)
                                self.display_attacks(x)
                        elif event.key == pygame.K_4:
                                self.player_attack(x, 3)
                                time.delay(1000)
                                #self.check_health()
                                #time.delay(1000)
                                self.opponent_attack()
                                #time.delay(1000)
                                #self.check_health()
                                time.delay(1000)
                                self.display_attacks(x)

    def display_attacks(self,x):
        self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
        self.print_text("1." + x[0][0], 630, 520, WHITE)
        self.print_text("2." + x[0][1], 850, 520, WHITE)
        self.print_text("3." + x[0][2], 630, 620, WHITE)
        self.print_text("4." + x[0][3], 830, 620, WHITE)
        self.attack_selected = True


    def player_attack(self,x,i):
        self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
        self.print_text("Pikachu used " + x[0][i], 20, 520, WHITE)
        self.hp_enemy = user_hp_cursor.execute('SELECT Move_damage from Moves where Move_Name=(?)',
                                               (x[0][i],)).fetchall()
        for hp in self.hp_enemy:
            self.hp_to_reduce = int(hp[0])
        self.opponent_health -= self.hp_to_reduce
        print(self.opponent_health)
        self.attack_selected = False
        # player health bar
        self.AAfilledRoundedRect(self.scr, (696, 406, 258, 18), BLACK, 0.7)
        self.AAfilledRoundedRect(self.scr, (700, 410, 250, 10), LIGHTGREY, 0.5)
        self.draw_health_bar(self.player_health, self.max_player_health, 700, 410, 250, 10)

        # opponent health bar
        self.AAfilledRoundedRect(self.scr, (196, 86, 258, 18), BLACK, 0.7)
        self.AAfilledRoundedRect(self.scr, (200, 90, 250, 10), LIGHTGREY, 0.5)
        if self.opponent_health>=1:
            self.draw_health_bar(self.opponent_health, self.max_opponent_health, 200, 90, 250, 10)
            display.update()
        else:
            self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
            self.print_text("You Won!!", 20, 520, WHITE)
            self.draw_health_bar(0, self.max_opponent_health, 200, 90, 250, 10)
            display.update()
            time.delay(500)
            pygame.quit()

    def opponent_attack(self):
        y = attack_cursor.execute('''SELECT Move1 , Move2 , Move3 , Move4 from 
                                                    Pokemon where Pokemon_Name=(?)''',
                                  (self.opp_poke_name,)).fetchall()
        self.opponent_attacks_list = [y[0][0], y[0][1], y[0][2], y[0][3]]
        self.opp_poke_attack = random.choice(self.opponent_attacks_list)

        self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
        self.print_text(self.opp_poke_name+" used " + self.opp_poke_attack, 20, 520, WHITE)
        print(self.opp_poke_attack)
        self.hp_user = enemy_hp_cursor.execute('SELECT Move_damage from Moves where Move_Name=(?)',
                                         (self.opp_poke_attack,)).fetchall()
        for hp in self.hp_user:
            self.hp_to_reduce_player = int(hp[0])

        self.player_health -= self.hp_to_reduce_player
        self.attack_selected = False
        # opponent health bar
        self.AAfilledRoundedRect(self.scr, (196, 86, 258, 18), BLACK, 0.7)
        self.AAfilledRoundedRect(self.scr, (200, 90, 250, 10), LIGHTGREY, 0.5)
        self.draw_health_bar(self.opponent_health, self.max_opponent_health, 200, 90, 250, 10)

        # player health bar
        self.AAfilledRoundedRect(self.scr, (696, 406, 258, 18), BLACK, 0.7)
        self.AAfilledRoundedRect(self.scr, (700, 410, 250, 10), LIGHTGREY, 0.5)
        if self.player_health>=1:
            self.draw_health_bar(self.player_health, self.max_player_health, 700, 410, 250, 10)
            display.update()
        else:
            self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
            self.print_text("You Lost!!", 20, 520, WHITE)
            self.draw_health_bar(0, self.max_player_health, 700, 410, 250, 10)
            display.update()
            time.delay(500)
            pygame.quit()
    def start_battle(self):
        self.battle_playing = True
        self.load_battle()



#obj = Battle()
#obj.start_battle()
 #     def check_health(self):

    #
    #     if self.opponent_health <= 0:
    #
    #         self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
    #
    #         self.AAfilledRoundedRect(self.scr, (196, 86, 258, 18), BLACK, 0.7)
    #         self.AAfilledRoundedRect(self.scr, (200, 90, 250, 10), LIGHTGREY, 0.5)
    #         self.draw_health_bar(0, self.max_opponent_health, 200, 90, 250, 10)
    #
    #         self.AAfilledRoundedRect(self.scr, (696, 406, 258, 18), BLACK, 0.7)
    #         self.AAfilledRoundedRect(self.scr, (700, 410, 250, 10), LIGHTGREY, 0.5)
    #         self.draw_health_bar(self.player_health, self.max_player_health, 700, 410, 250, 10)
    #
    #         self.print_text("You Won!!", 20, 520, WHITE)
    #         display.update()
    #         time.delay(1000)
    #         # pygame.quit()
    #         sys.exit()
    #         #Dont uncomment it now the though the window wont close but if you uncomment it , it will end the whole game and give a error
    #     elif self.player_health <= 0:
    #
    #         self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
    #
    #         self.AAfilledRoundedRect(self.scr, (696, 406, 258, 18), BLACK, 0.7)
    #         self.AAfilledRoundedRect(self.scr, (700, 410, 250, 10), LIGHTGREY, 0.5)
    #         self.draw_health_bar(1, self.max_player_health, 700, 410, 250, 10)
    #
    #         self.AAfilledRoundedRect(self.scr, (196, 86, 258, 18), BLACK, 0.7)
    #         self.AAfilledRoundedRect(self.scr, (200, 90, 250, 10), LIGHTGREY, 0.5)
    #         self.draw_health_bar(self.opponent_health, self.max_opponent_health, 200, 90, 250, 10)
    #
    #         self.print_text("Stupid!! You Lost", 20, 520, WHITE)
    #         display.update()
    #         time.delay(1000)
    #         #pygame.quit()
    #         # Dont uncomment it now the though the window wont close but if you uncomment it , it will end the whole game and give a error

