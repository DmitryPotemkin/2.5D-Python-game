import pygame
from settings import *
from ray_casting import ray_casting
import map_generator
from collections import deque
import sys
from sprite_objects import SpriteObject

class Drawing:
    def __init__(self, screen, screen_map, player, clock, sprites):
        self.sprites = sprites
        self.dead = False
        self.screen = screen
        self.screen_map = screen_map
        self.player = player
        self.clock = clock
        # Текстуры
        self.textures = {1: pygame.image.load('textures/Wall.png').convert(),
                        2: pygame.image.load('textures/Wall1.png').convert(),
                        'S': pygame.image.load('textures/Skybox.png').convert(),
                        'F': pygame.image.load('textures/Floor.png').convert()}

        # Меню
        self.menu_trigger = True
        self.Fone = pygame.image.load('textures/Menu.png').convert()

        # Параметры оружия
        self.weapon_base_sprite = pygame.image.load('sprites/Arm/main/0.png').convert_alpha()
        self.weapon_shot_animation = deque([pygame.image.load(f'sprites/Arm/Shoot/{i}.png').convert_alpha()
                                            for i in range(36)])
        self.weapon_rect = self.weapon_base_sprite.get_rect()
        self.weapon_pos = (screen_width - self.weapon_rect.width, screen_height - self.weapon_rect.height)
        self.shoot_length = len(self.weapon_shot_animation)
        self.shoot_length_count = 0
        self.shoot_animation_speed = 2
        self.shoot_animation_count = 0
        self.shoot_animation_trigger = True
        self.shoot_sound = pygame.mixer.Sound('sound/Shoot.mp3')

        # Параметры вспышки от выстрела
        self.sfx = deque([pygame.image.load(f'sprites/Sfx/{i}.png').convert_alpha() for i in range(6)])
        self.sfx_length_count = 0
        self.sfx_length = len(self.sfx)

    # Отрисовка заднего фона
    def background(self, angle):
        sky_offset = -20 * math.degrees(angle) % screen_width
        self.screen.blit(self.textures['S'], (sky_offset, 0))
        self.screen.blit(self.textures['S'], (sky_offset - screen_width, 0))
        self.screen.blit(self.textures['S'], (sky_offset + screen_width, 0))
        self.screen.blit(self.textures['F'], (0, screen_height / 2))

    # Отрисовка мира
    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.screen.blit(object, object_pos)

    # Отрисовка мини карты
    def minimap(self, player):
        self.screen_map.fill(black_color)
        map_pos_x, map_pos_y = player.pos_x // map_scale, player.pos_y // map_scale
        pygame.draw.line(self.screen_map, green_color, (map_pos_x, map_pos_y), (map_pos_x + 12 * math.cos(player.player_view_angle),
                                                 map_pos_y + 12 * math.sin(player.player_view_angle)), 2)
        pygame.draw.circle(self.screen_map, green_color, (int(map_pos_x), int(map_pos_y)), 5)
        for x, y in map_generator.minimap:
            pygame.draw.rect(self.screen_map, white_color, (x, y, map_tile, map_tile))
        self.screen.blit(self.screen_map, map_pos)

    # Отрисовка руки с оружием
    def player_weapon(self, shots):
        if self.player.shoot:
            if not self.shoot_length_count:
                self.shoot_sound.play()
            self.shot_projection = min(shots)[1] // 2
            self.bullet_sfx()
            shot_sprite = self.weapon_shot_animation[0]
            self.screen.blit(shot_sprite, self.weapon_pos)
            self.shoot_animation_count += 1
            if self.shoot_animation_count == self.shoot_animation_speed:
                self.weapon_shot_animation.rotate(-1)
                self.shoot_animation_count = 0
                self.shoot_length_count += 1
                self.shoot_animation_trigger = False
            if self.shoot_length_count == self.shoot_length:
                self.player.shoot = False
                self.shoot_length_count = 0
                self.sfx_length_count = 0
                self.shoot_animation_trigger = True
        else:
            self.screen.blit(self.weapon_base_sprite, self.weapon_pos)

    # Отрисовка вспышки от выстрела
    def bullet_sfx(self):
        if self.sfx_length_count < self.sfx_length:
            sfx = pygame.transform.scale(self.sfx[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx.get_rect()
            self.screen.blit(sfx, (screen_width / 2 - sfx_rect.w // 2, screen_height / 2 - sfx_rect.h // 2))
            self.sfx_length_count += 1
            self.sfx.rotate(-1)

    # Отрисовка очков
    def draw_ui(self, score, add_score, factor):
        fontUI = pygame.font.Font('fonts/BarcadeBrawlRegular.ttf', 20)
        display_score = "Очки: " + str(int(score))
        render = fontUI.render(display_score, 0, white_color)
        self.screen.blit(render, (5, 5))
        if factor != 0:
            display_score_add = str(int(add_score)) + " * " + str(int(factor))
            render = fontUI.render(display_score_add, 0, white_color)
            self.screen.blit(render, (5, 40))

    # Отрисовка победного экрана
    def win(self, score, lvl):
        label_font = pygame.font.Font('fonts/OutlinePixel7.ttf', 100)
        button_font = pygame.font.Font('fonts/OutlinePixel7.ttf', 80)
        render = label_font.render('level complete', 1, (255, 255, 255))

        with open('ScoreSave/High_Scores.txt', 'r') as HS_file:
            lines = HS_file.readlines()
            score_text = button_font.render('Score:' + str(int(score)) + '/' + str(int(lines[lvl - 1])), 1, (255, 255, 255))

        # Фон победного экрана
        rect = pygame.Rect(0, 0, 1000, 450)
        rect.center = screen_width / 2, screen_height / 2
        pygame.draw.rect(self.screen, gray_color, rect, border_radius=50)
        self.screen.blit(render, (rect.centerx - 450, rect.centery - 180))
        self.screen.blit(score_text, (rect.centerx - 450, rect.centery - 70))
        # Кнопка продолжения на победном экране
        next = button_font.render('CONTINUE', 1, white_color)
        button_next = pygame.Rect(0, 0, 450, 150)
        button_next.center = screen_width / 2 - 250, screen_height / 2 + 100

        pygame.draw.rect(self.screen, black_color, button_next, border_radius=25, width=10)
        self.screen.blit(next, (button_next.centerx - 210, button_next.centery - 40))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if button_next.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, black_color, button_next, border_radius=25)
            self.screen.blit(next, (button_next.centerx - 210, button_next.centery - 40))
            if mouse_click[0]:
                with open('ScoreSave/High_Scores.txt', 'r+') as HS_file:
                    lines = HS_file.readlines()
                    if int(lines[lvl - 1]) < score:
                        lines[lvl - 1] = (str(int(score)) + '\n')
                    HS_file.seek(0)
                    for line in lines:
                        HS_file.write(line)
                (map_generator.map_list, map_generator.map_width, map_generator.map_height, 
                map_generator.world_map, map_generator.minimap, map_generator.collision_walls) = map_generator.mapCreate(lvl + 1)
                self.sprites.list_of_objects = self.sprites.map_fill(lvl + 1)
                self.player.pos_x = 150
                self.player.pos_y = 150
                self.player.player_view_angle = 0
                pygame.mixer.music.stop()
                if lvl < 3:
                    pygame.mixer.music.load('sound/%d.mp3' % (lvl + 1))
                else:
                    pygame.mixer.music.load('sound/1.mp3')
                pygame.mixer.music.play()
                pygame.mouse.set_visible(False)
        # Кнопка выхода на победном экране
        exit = button_font.render('EXIT', 1, white_color)
        button_exit = pygame.Rect(0, 0, 450, 150)
        button_exit.center = screen_width / 2 + 250, screen_height / 2 + 100

        pygame.draw.rect(self.screen, black_color, button_exit, border_radius=25, width=10)
        self.screen.blit(exit, (button_exit.centerx - 100, button_exit.centery - 40))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if button_exit.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, black_color, button_exit, border_radius=25)
            self.screen.blit(exit, (button_exit.centerx - 100, button_exit.centery - 40))
            if mouse_click[0]:
                with open('ScoreSave/High_Scores.txt', 'r+') as HS_file:
                    lines = HS_file.readlines()
                    if int(lines[0]) < score:
                        lines[0] = (str(int(score)) + '\n')
                    HS_file.seek(0)
                    for line in lines:
                        HS_file.write(line)
                pygame.quit()
                sys.exit()


        pygame.display.flip()
        self.clock.tick(15)

    # Экран поражения
    def lose(self):
        label_font = pygame.font.Font('fonts/OutlinePixel7.ttf', 100)
        button_font = pygame.font.Font('fonts/OutlinePixel7.ttf', 80)
        render = label_font.render('you lose', 1, (255, 255, 255))
        # Фон экрана поражения
        rect = pygame.Rect(0, 0, 1000, 450)
        rect.center = screen_width / 2, screen_height / 2
        pygame.draw.rect(self.screen, red_color, rect, border_radius=50)
        self.screen.blit(render, (rect.centerx - 270, rect.centery - 140))
        # Кнопка рестарта экрана поражения
        restart = button_font.render('RESTART', 1, white_color)
        button_restart = pygame.Rect(0, 0, 450, 150)
        button_restart.center = screen_width / 2 - 250, screen_height / 2 + 100

        pygame.draw.rect(self.screen, black_color, button_restart, border_radius=25, width=10)
        self.screen.blit(restart, (button_restart.centerx - 180, button_restart.centery - 40))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if button_restart.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, black_color, button_restart, border_radius=25)
            self.screen.blit(restart, (button_restart.centerx - 180, button_restart.centery - 40))
            if mouse_click[0]:
                (map_generator.map_list, map_generator.map_width, map_generator.map_height, 
                map_generator.world_map, map_generator.minimap, map_generator.collision_walls) = map_generator.mapCreate(1)
                self.sprites.list_of_objects = self.sprites.map_fill(1)
                self.player.pos_x = 150
                self.player.pos_y = 150
                self.player.player_view_angle = 0
                pygame.mixer.music.stop()
                pygame.mixer.music.load('sound/1.mp3')
                pygame.mixer.music.play()
                pygame.mouse.set_visible(False)
                self.dead = False
        # Кнопка выхода экрана поражения
        exit = button_font.render('EXIT', 1, white_color)
        button_exit = pygame.Rect(0, 0, 450, 150)
        button_exit.center = screen_width / 2 + 250, screen_height / 2 + 100

        pygame.draw.rect(self.screen, black_color, button_exit, border_radius=25, width=10)
        self.screen.blit(exit, (button_exit.centerx - 100, button_exit.centery - 40))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if button_exit.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, black_color, button_exit, border_radius=25)
            self.screen.blit(exit, (button_exit.centerx - 100, button_exit.centery - 40))
            if mouse_click[0]:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        self.clock.tick(15)

    # Главное меню
    def menu(self):
        x = 0
        button_font = pygame.font.Font('fonts/OutlinePixel7.ttf', 80)
        label_font = pygame.font.Font('fonts/OutlinePixel7.ttf', 120)
        # Кнопка старта
        start = button_font.render('START', 1, yellow_color)
        button_start = pygame.Rect(0, 0, 400, 150)
        button_start.center = screen_width / 2, screen_height / 2
        # Кнопка выхода
        exit = button_font.render('EXIT', 1, yellow_color)
        button_exit = pygame.Rect(0, 0, 400, 150)
        button_exit.center = screen_width / 2, screen_height / 2 + 200

        while self.menu_trigger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.Fone, (0, 0))

            pygame.draw.rect(self.screen, black_color, button_start, border_radius=25, width=10)
            self.screen.blit(start, (button_start.centerx - 130, button_start.centery - 40))

            pygame.draw.rect(self.screen, black_color, button_exit, border_radius=25, width=10)
            self.screen.blit(exit, (button_exit.centerx - 100, button_exit.centery - 40))

            label = button_font.render('project', 1, (0, 0, 0))
            self.screen.blit(label, (400, 90))
            label = label_font.render('M.I.G.P.R.G.', 1, (0, 0, 0))
            self.screen.blit(label, (150, 150))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if button_start.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, black_color, button_start, border_radius=25)
                self.screen.blit(start, (button_start.centerx - 130, button_start.centery - 40))
                if mouse_click[0]:
                    self.menu_trigger = False
            elif button_exit.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, black_color, button_exit, border_radius=25)
                self.screen.blit(exit, (button_exit.centerx - 100, button_exit.centery - 40))
                if mouse_click[0]:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(20)