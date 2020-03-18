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


class Battle:
    def __init__(self):
        self.battle_playing = True
        self.attack_selected = False
        self.bag_selected = False
        self.pokemon_selected = False
        self.player_win = False

        self.pokemon_list = ['Bulbasaur', 'Charmander', 'Squirtle', 'Pidgey', 'Pikachu', 'Onix']

        self.scr = display.set_mode((1024, 768))
        self.scr.fill(LIGHTGREY)

        game_folder = path.dirname(__file__)
        sound_folder = path.join(game_folder, 'Sound Files')

        self.sound_effects = {}
        for sound_type in EFFECTS_SOUNDS:
            self.sound_effects[sound_type] = pygame.mixer.Sound(path.join(sound_folder, EFFECTS_SOUNDS[sound_type]))
            self.sound_effects[sound_type].set_volume(1)
        self.bg_music = {}
        for sound_type in BG_MUSIC:
            self.bg_music[sound_type] = pygame.mixer.Sound(path.join(sound_folder, BG_MUSIC[sound_type]))
            self.bg_music[sound_type].set_volume(0.5)

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
        if health >= 0:
            width = int(w * health / max_health)
        else:
            width = 0
        health_bar = Rect(x, y, width, h)
        draw.rect(self.scr, col, health_bar)

    def draw_xp_bar(self, xp, max_xp, x, y, w, h):
        col = LIGHTBLUE
        width = int(w * xp / max_xp)
        xp_bar = Rect(x, y, width, h)
        draw.rect(self.scr, col, xp_bar)

    def print_text(self, msg, x, y, colour, text_size):
        text_font = pygame.font.SysFont('sans', text_size)
        text = text_font.render(msg, True, colour)
        self.scr.blit(text, [x, y])

    def display_dialog_box(self):
        self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
        self.AAfilledRoundedRect(self.scr, (550, 500, 450, 240), BLACK, 0.3)
        self.AAfilledRoundedRect(self.scr, (560, 510, 430, 220), LIGHTBLUE, 0.3)
        self.print_text("Choose your action", 30, 500, WHITE, 40)
        self.print_text("1. FIGHT", 600, 550, WHITE, 32)
        self.print_text("2. BAG", 850, 550, WHITE, 32)
        self.print_text("3. POKEMON", 600, 650, WHITE, 32)
        self.print_text("4. RUN", 850, 650, WHITE, 32)
        display.update()

    def display_attacks(self, attacks):
        self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
        self.AAfilledRoundedRect(self.scr, (480, 500, 520, 240), BLACK, 0.3)
        self.AAfilledRoundedRect(self.scr, (490, 510, 500, 220), LIGHTBLUE, 0.3)
        self.print_text("Choose your attack", 30, 500, WHITE, 40)
        self.print_text("1." + attacks[0], 500, 550, WHITE, 32)
        self.print_text("2." + attacks[1], 750, 550, WHITE, 32)
        self.print_text("3." + attacks[2], 500, 650, WHITE, 32)
        self.print_text("4." + attacks[3], 750, 650, WHITE, 32)

    def display_bag(self):
        self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
        self.print_text("1. Potion", 50, 500, WHITE, 25)
        self.print_text("2. Super Potion", 50, 550, WHITE, 25)
        self.print_text("3. Hyper Potion", 50, 600, WHITE, 25)
        self.print_text("4. Full Heal", 50, 650, WHITE, 25)
        self.print_text("5. Pokeball", 50, 700, WHITE, 25)
        self.print_text("6. Greatball", 500, 500, WHITE, 25)
        self.print_text("7. Ultraball", 500, 550, WHITE, 25)
        for y in range(500, 710, 50):
            self.print_text("x", 300, y, WHITE, 25)
        self.print_text("x", 700, 500, WHITE, 25)
        self.print_text("x", 700, 550, WHITE, 25)
        display.update()

    def display_pokemon(self):
        game_folder = path.dirname(__file__)
        poke_folder = path.join(game_folder, 'Assets\Pokemon')
        user_poke_icon = []
        user_poke_name = []
        for name in self.player_pokemons:
            user_poke_name.append(name[0])
            user_poke_icon.append(image.load(path.join(poke_folder, name[0] + '_icon.png')))

        self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)

        # Draw small rectangles, small picture and pokemon name
        self.AAfilledRoundedRect(self.scr, (40, 540, 200, 40), LIGHTBLUE, 1)
        self.scr.blit(user_poke_icon[0], (55, 570 - user_poke_icon[0].get_height()))  # pokemon 1
        self.print_text("1. " + user_poke_name[0], 100, 550, BLACK, 20)

        if len(user_poke_name) >= 2:
            self.AAfilledRoundedRect(self.scr, (420, 540, 200, 40), LIGHTBLUE, 1)
            self.scr.blit(user_poke_icon[1], (435, 570 - user_poke_icon[1].get_height()))  # pokemon 2
            self.print_text("2. " + user_poke_name[1], 480, 550, BLACK, 20)

        if len(user_poke_name) >= 3:
            self.AAfilledRoundedRect(self.scr, (790, 540, 200, 40), LIGHTBLUE, 1)
            self.scr.blit(user_poke_icon[2], (805, 570 - user_poke_icon[2].get_height()))  # pokemon 3
            self.print_text("3. " + user_poke_name[2], 850, 550, BLACK, 20)

        if len(user_poke_name) >= 4:
            self.AAfilledRoundedRect(self.scr, (40, 640, 200, 40), LIGHTBLUE, 1)
            self.scr.blit(user_poke_icon[3], (55, 670 - user_poke_icon[3].get_height()))  # pokemon 4
            self.print_text("4. " + user_poke_name[3], 100, 650, BLACK, 20)

        if len(user_poke_name) >= 5:
            self.AAfilledRoundedRect(self.scr, (420, 640, 200, 40), LIGHTBLUE, 1)
            self.scr.blit(user_poke_icon[4], (435, 670 - user_poke_icon[4].get_height()))  # pokemon 5
            self.print_text("5. " + user_poke_name[4], 480, 650, BLACK, 20)

        if len(user_poke_name) >= 6:
            self.AAfilledRoundedRect(self.scr, (790, 640, 200, 40), LIGHTBLUE, 1)
            self.scr.blit(user_poke_icon[5], (805, 670 - user_poke_icon[5].get_height()))  # pokemon 6
            self.print_text("6. " + user_poke_name[5], 850, 650, BLACK, 20)

    def change_pokemon(self, poke_no):
        self.player_poke_name = cursor.execute('''SELECT Pokemon_Name FROM User_Pokemon WHERE On_Hand=(?)''',
                                               (poke_no,)).fetchall()
        self.player_poke_name = self.player_poke_name[0][0]
        self.max_player_health = cursor.execute('''SELECT HP FROM Pokemon WHERE Pokemon_Name=(?)''',
                                                (self.player_poke_name,)).fetchall()
        self.max_player_health = self.max_player_health[0][0]
        self.player_health = cursor.execute('''SELECT Current_HP FROM User_Pokemon WHERE On_Hand=(?)''',
                                            (poke_no,)).fetchall()
        self.player_health = self.player_health[0][0]
        self.player_poke_level = cursor.execute('''SELECT Level FROM User_Pokemon WHERE On_Hand=(?)''',
                                                (poke_no,)).fetchall()
        self.player_poke_level = self.player_poke_level[0][0]
        self.player_poke_xp = cursor.execute('''SELECT XP FROM User_Pokemon WHERE On_Hand=(?)''',
                                             (poke_no,)).fetchall()
        self.player_poke_xp = self.player_poke_xp[0][0]
        self.player_poke_max_xp = cursor.execute('''SELECT XP FROM Level_Chart WHERE Level=(?)''',
                                                 (self.player_poke_level,)).fetchall()
        self.player_poke_max_xp = self.player_poke_max_xp[0][0]
        self.load_battle_screen()
        self.display_dialog_box()
        display.update()

    def catch_pokemon(self, ball):
        ball_name = {1: 'Pokeball', 1.5: 'Greatball', 2: 'Ultraball'}
        chance = (((3 * self.max_opponent_health - 2 * self.opponent_health) * ball) / (
                6 * self.max_opponent_health)) * 100
        int(chance)
        print(chance)
        self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
        self.print_text("You throw the " + ball_name[ball] + " at the pokemon!", 30, 510, WHITE, 30)
        display.update()
        time.delay(3000)
        if random.randint(0, 100) <= chance:
            print('Caught ' + self.opp_poke_name)
            self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
            self.print_text("You successfully caught the " + self.opp_poke_name, 30, 510, WHITE, 30)
            display.update()
            next_id = cursor.execute('''SELECT max(Pokemon_id) FROM User_Pokemon''').fetchall()
            next_id = next_id[0][0] + 1
            on_hand = cursor.execute('''SELECT max(On_Hand) FROM User_Pokemon''').fetchall()
            on_hand = on_hand[0][0]
            if on_hand == 6:
                on_hand = 0
            else:
                on_hand += 1
            print(self.opponent_attacks_list)
            cursor.execute('''INSERT INTO User_Pokemon VALUES((?), (?), (?), (?), 0, (?), (?), (?), (?), (?))''',
                           (on_hand, next_id, self.opp_poke_name, self.opp_poke_level, self.max_opponent_health,
                            self.opponent_attacks_list[0], self.opponent_attacks_list[1],
                            self.opponent_attacks_list[2], self.opponent_attacks_list[3]))
            conn.commit()
            time.delay(2000)
            self.bag_selected = False
            self.battle_playing = False
            return True
        else:
            self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
            self.print_text(self.opp_poke_name + " escaped from the " + ball_name[ball], 30, 510, WHITE, 30)
            display.update()
            print('Not Caught')
            time.delay(2000)
            return False

    def load_battle_screen(self):
        game_folder = path.dirname(__file__)
        poke_folder = path.join(game_folder, 'Assets\Pokemon')

        bg_img = image.load(path.join(poke_folder, 'battle_background.png'))
        bg_img2 = image.load(path.join(poke_folder, 'dialogbox_background.png'))

        user_poke_img = image.load(path.join(poke_folder, self.player_poke_name + '_back.png'))
        opp_poke_img = image.load(path.join(poke_folder, self.opp_poke_name + '_front.png'))

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
        self.print_text(self.player_poke_name, 570, 360, BLACK, 32)
        self.print_text("Lv. " + str(self.player_poke_level), 570, 400, BLACK, 26)
        self.print_text(self.opp_poke_name, 60, 40, BLACK, 32)
        self.print_text("Lv. " + str(self.opp_poke_level), 60, 80, BLACK, 26)

        # drawing health bars
        # opponent health bar
        self.print_text("HP", 165, 85, BLACK, 15)
        self.AAfilledRoundedRect(self.scr, (196, 86, 258, 18), BLACK, 0.7)
        self.AAfilledRoundedRect(self.scr, (200, 90, 250, 10), LIGHTGREY, 0.5)
        self.draw_health_bar(self.opponent_health, self.max_opponent_health, 200, 90, 250, 10)

        # player health bar
        self.print_text("HP", 665, 405, BLACK, 15)
        self.AAfilledRoundedRect(self.scr, (696, 406, 258, 18), BLACK, 0.7)
        self.AAfilledRoundedRect(self.scr, (700, 410, 250, 10), LIGHTGREY, 0.5)
        self.draw_health_bar(self.player_health, self.max_player_health, 700, 410, 250, 10)

        # drawing xp bar for player
        self.print_text("XP", 665, 425, BLACK, 15)
        self.AAfilledRoundedRect(self.scr, (696, 426, 158, 18), BLACK, 0.7)
        self.AAfilledRoundedRect(self.scr, (700, 430, 150, 10), LIGHTGREY, 0.5)
        self.draw_xp_bar(self.player_poke_xp, self.player_poke_max_xp, 700, 430, 150, 10)

        # loading pokemon sprites
        self.scr.blit(user_poke_img, (150, 478 - user_poke_img.get_height()))
        self.scr.blit(opp_poke_img, (700, 270 - opp_poke_img.get_height()))

        # loading main dialog box
        self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)

    def load_battle(self):
        self.player_pokemons = cursor.execute(
            '''SELECT Pokemon_Name, Level, XP FROM User_Pokemon WHERE On_Hand>0''').fetchall()
        print("Your Pokemon(Name, Level, XP) : " + str(self.player_pokemons))

        self.poke_in_battle = 1
        self.player_poke_name = cursor.execute('''SELECT Pokemon_Name FROM User_Pokemon WHERE On_Hand=1''').fetchall()
        self.player_poke_name = self.player_poke_name[0][0]
        self.max_player_health = cursor.execute('''SELECT HP FROM Pokemon WHERE Pokemon_Name=(?)''',
                                                (self.player_poke_name,)).fetchall()
        self.max_player_health = self.max_player_health[0][0]
        self.player_health = cursor.execute('''SELECT Current_HP FROM User_Pokemon WHERE On_Hand=1''').fetchall()
        self.player_health = self.player_health[0][0]
        self.player_poke_level = cursor.execute('''SELECT Level FROM User_Pokemon WHERE On_Hand=1''').fetchall()
        self.player_poke_level = self.player_poke_level[0][0]
        self.player_poke_xp = cursor.execute('''SELECT XP FROM User_Pokemon WHERE On_Hand=1''').fetchall()
        self.player_poke_xp = self.player_poke_xp[0][0]
        self.player_poke_max_xp = cursor.execute('''SELECT XP FROM Level_Chart WHERE Level=(?)''',
                                                 (self.player_poke_level,)).fetchall()
        self.player_poke_max_xp = self.player_poke_max_xp[0][0]

        # fetch hp and moves of opponent pokemon
        self.opp_poke_level = random.randint(self.player_poke_level - 3, self.player_poke_level + 3)
        if self.opp_poke_level <= 0:
            self.opp_poke_level = 1
        self.opp_poke_name = random.choice(self.pokemon_list)
        self.max_opponent_health = cursor.execute('SELECT HP from Pokemon where Pokemon_Name=(?)',
                                                  (self.opp_poke_name,)).fetchall()
        self.max_opponent_health = int(self.max_opponent_health[0][0])
        self.opponent_health = self.max_opponent_health
        atk_list = attack_cursor.execute('''SELECT Move1 , Move2 , Move3 , Move4 from 
                                                                    Pokemon where Pokemon_Name=(?)''',
                                         (self.opp_poke_name,)).fetchall()
        self.opponent_attacks_list = list(atk_list[0])

        self.load_battle_screen()  # Loading the display of screen

        self.print_text("A wild Pokemon has appeared!", 30, 520, WHITE, 32)
        display.update()
        time.delay(2000)
        self.display_dialog_box()
        self.battle_run()

    def battle_run(self):
        # game loop - set self.playing = False to end the game
        while self.battle_playing:
            self.battle_events()
            self.battle_update()
            # self.draw()

    def quit_battle(self):
        pygame.quit()
        sys.exit()

    def battle_update(self):
        display.update()

    def battle_events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_battle()
            elif event.type == pygame.KEYDOWN:
                if self.opponent_health >= 1 and self.player_health >= 1:
                    attacks = attack_cursor.execute('''SELECT Move1 , Move2 , Move3 , Move4 from 
                                            Pokemon where Pokemon_Name=(?)''',
                                                    (self.player_poke_name,)).fetchall()
                    attacks = list(attacks[0])
                    # dialog box events
                    if not self.attack_selected and not self.bag_selected and not self.pokemon_selected:
                        if event.key == pygame.K_1:
                            self.display_attacks(attacks)
                            self.attack_selected = True
                        elif event.key == pygame.K_2:
                            self.display_bag()
                            self.bag_selected = True
                        elif event.key == pygame.K_3:
                            self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
                            self.print_text("Pokemon List", 30, 520, WHITE, 32)
                            self.display_pokemon()
                            self.pokemon_selected = True
                        elif event.key == pygame.K_4:
                            self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
                            self.flee_counter = random.randrange(1, 9)
                            if self.flee_counter <= 5:
                                self.print_text("You successfully run away!", 50, 520, WHITE, 32)
                                display.update()
                                time.delay(2000)
                                self.battle_playing = False
                            else:
                                self.print_text("You couldn't escape!", 50, 520, WHITE, 32)
                                display.update()
                                time.delay(2000)
                                self.opponent_attack()
                                time.delay(1000)
                                self.display_dialog_box()
                    # attack events
                    elif self.attack_selected:
                        if event.key == pygame.K_ESCAPE:
                            self.attack_selected = False
                            self.display_dialog_box()
                            break
                        if event.key == pygame.K_1:
                            self.player_attack(attacks, 0)
                            time.delay(1000)
                            if not self.player_win:
                                self.opponent_attack()
                                time.delay(1000)
                                self.display_dialog_box()
                        elif event.key == pygame.K_2:
                            self.player_attack(attacks, 1)
                            time.delay(1000)
                            if not self.player_win:
                                self.opponent_attack()
                                time.delay(1000)
                                self.display_dialog_box()
                        elif event.key == pygame.K_3:
                            self.player_attack(attacks, 2)
                            time.delay(1000)
                            if not self.player_win:
                                self.opponent_attack()
                                time.delay(1000)
                                self.display_dialog_box()
                        elif event.key == pygame.K_4:
                            self.player_attack(attacks, 3)
                            time.delay(1000)
                            if not self.player_win:
                                self.opponent_attack()
                                time.delay(1000)
                                self.display_dialog_box()
                        self.attack_selected = False
                    # bag events
                    elif self.bag_selected:
                        if event.key == pygame.K_ESCAPE:
                            self.bag_selected = False
                            self.display_dialog_box()
                            break
                        if event.key == pygame.K_1:
                            self.player_health += 50
                            if self.player_health > self.max_player_health:
                                self.player_health = self.max_player_health
                            self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
                            self.print_text("You healed your pokemon by 50 HP", 30, 510, WHITE, 30)
                            self.draw_health_bar(self.player_health, self.max_player_health, 700, 410, 250, 10)
                            display.update()
                            time.delay(2000)
                        elif event.key == pygame.K_2:
                            self.player_health += 100
                            if self.player_health > self.max_player_health:
                                self.player_health = self.max_player_health
                            self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
                            self.print_text("You healed your pokemon by 100 HP", 30, 510, WHITE, 30)
                            self.draw_health_bar(self.player_health, self.max_player_health, 700, 410, 250, 10)
                            display.update()
                            time.delay(2000)
                        elif event.key == pygame.K_3:
                            self.player_health += 200
                            if self.player_health > self.max_player_health:
                                self.player_health = self.max_player_health
                            self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
                            self.print_text("You healed your pokemon by 200 HP", 30, 510, WHITE, 30)
                            self.draw_health_bar(self.player_health, self.max_player_health, 700, 410, 250, 10)
                            display.update()
                            time.delay(2000)
                        elif event.key == pygame.K_4:
                            self.player_health = self.max_player_health
                            self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
                            self.print_text("You healed your pokemon to full HP", 30, 510, WHITE, 30)
                            self.draw_health_bar(self.player_health, self.max_player_health, 700, 410, 250, 10)
                            display.update()
                            time.delay(2000)
                        elif event.key == pygame.K_5:
                            if self.catch_pokemon(1):
                                break
                        elif event.key == pygame.K_6:
                            if self.catch_pokemon(1.5):
                                break
                        elif event.key == pygame.K_7:
                            if self.catch_pokemon(2):
                                break
                        self.bag_selected = False
                        self.opponent_attack()
                        time.delay(2000)
                        self.display_dialog_box()
                    # pokemon events
                    elif self.pokemon_selected:
                        if event.key == pygame.K_ESCAPE:
                            self.pokemon_selected = False
                            self.display_dialog_box()
                            break
                        if event.key == pygame.K_1:  # change to pokemon 1
                            self.change_pokemon(1)
                            self.poke_in_battle = 1
                        elif event.key == pygame.K_2:  # change to pokemon 2
                            self.change_pokemon(2)
                            self.poke_in_battle = 2
                        elif event.key == pygame.K_3:  # change to pokemon 3
                            self.change_pokemon(3)
                            self.poke_in_battle = 3
                        elif event.key == pygame.K_4:  # change to pokemon 4
                            self.change_pokemon(4)
                            self.poke_in_battle = 4
                        elif event.key == pygame.K_5:  # change to pokemon 5
                            self.change_pokemon(5)
                            self.poke_in_battle = 5
                        elif event.key == pygame.K_6:  # change to pokemon 6
                            self.change_pokemon(6)
                            self.poke_in_battle = 6
                        self.pokemon_selected = False
                else:
                    self.battle_playing = False

    def player_attack(self, attacks, i):
        self.sound_effects['HIT_SFX_01'].play()
        self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
        self.print_text(self.player_poke_name + " used " + attacks[i], 20, 520, WHITE, 32)
        display.update()
        self.hp_enemy = user_hp_cursor.execute('SELECT Move_damage from Moves where Move_Name=(?)',
                                               (attacks[i],)).fetchall()
        for hp in self.hp_enemy:
            self.hp_to_reduce = int(hp[0])
        self.opponent_health -= self.hp_to_reduce
        # print("Opponents health reduced to : "+str(self.opponent_health))
        self.attack_selected = False
        # player health bar
        self.AAfilledRoundedRect(self.scr, (696, 406, 258, 18), BLACK, 0.7)
        self.AAfilledRoundedRect(self.scr, (700, 410, 250, 10), LIGHTGREY, 0.5)
        self.draw_health_bar(self.player_health, self.max_player_health, 700, 410, 250, 10)

        # opponent health bar
        self.AAfilledRoundedRect(self.scr, (196, 86, 258, 18), BLACK, 0.7)
        self.AAfilledRoundedRect(self.scr, (200, 90, 250, 10), LIGHTGREY, 0.5)
        if self.opponent_health >= 1:
            self.draw_health_bar(self.opponent_health, self.max_opponent_health, 200, 90, 250, 10)
            display.update()
        else:
            level_up = False
            self.player_poke_xp += 5 * self.opp_poke_level
            if self.player_poke_xp >= self.player_poke_max_xp:
                self.player_poke_level += 1
                self.player_poke_xp -= self.player_poke_max_xp
                level_up = True
            cursor.execute('''UPDATE User_Pokemon SET Level=(?),XP=(?) WHERE On_Hand=(?)''',
                           (self.player_poke_level, self.player_poke_xp,self.poke_in_battle))
            conn.commit()
            self.draw_health_bar(-1, self.max_opponent_health, 200, 90, 250, 10)
            display.update()
            time.delay(2000)
            self.bg_music['Final Battle'].stop()
            self.sound_effects['Victory'].play()
            self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
            self.print_text("You defeated the wild " + self.opp_poke_name, 20, 520, WHITE, 32)
            display.update()
            time.delay(2000)
            self.load_battle_screen()
            self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
            self.print_text(self.player_poke_name + " gained " + str(5 * self.opp_poke_level) + " XP", 20, 520, WHITE,
                            32)
            if level_up:
                self.print_text(self.player_poke_name + "'s Level increased to " + str(self.player_poke_level),
                                20, 570, WHITE, 32)
            display.update()
            time.delay(3000)
            self.player_win = True
            self.battle_playing = False

    def opponent_attack(self):
        self.sound_effects['HIT_SFX_01'].play()
        y = attack_cursor.execute('''SELECT Move1 , Move2 , Move3 , Move4 from 
                                                    Pokemon where Pokemon_Name=(?)''',
                                  (self.opp_poke_name,)).fetchall()
        self.opponent_attacks_list = list(y[0])
        self.opp_poke_attack = random.choice(self.opponent_attacks_list)

        self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
        self.print_text(self.opp_poke_name + " used " + self.opp_poke_attack, 20, 520, WHITE, 32)
        display.update()
        # print("Opponent used "+self.opp_poke_attack)
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
        if self.player_health >= 1:
            self.draw_health_bar(self.player_health, self.max_player_health, 700, 410, 250, 10)
            display.update()
        else:
            self.draw_health_bar(0, self.max_player_health, 700, 410, 250, 10)
            display.update()
            time.delay(2000)
            self.bg_music['Final Battle'].stop()
            self.sound_effects['Lose'].play()
            self.AAfilledRoundedRect(self.scr, (10, 490, 1000, 260), BLUE, 0.3)
            self.print_text("You Lost!!", 20, 520, WHITE, 32)
            display.update()
            time.delay(3000)
            self.player_win = True
            self.battle_playing = False
            self.player_health = self.max_player_health

    def start_battle(self):
        self.bg_music['Final Battle'].play(-1)
        self.battle_playing = True
        self.player_win = False
        self.load_battle()
        if not self.player_win:
            self.bg_music['Final Battle'].stop()


# obj = Battle()
# obj.start_battle()
