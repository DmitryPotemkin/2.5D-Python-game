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
        self.font = pygame.font.Font('fonts/BarcadeBrawlRegular.ttf', 20)
        self.font_for_game = pygame.font.Font('fonts/OutlinePixel7.ttf', 144)
        self.textures = {1: pygame.image.load('textures/Wall.png').convert(),
                        2: pygame.image.load('textures/Wall1.png').convert(),
                        'S': pygame.image.load('textures/Skybox.png').convert(),
                        'F': pygame.image.load('textures/Floor.png').convert()}

        # Меню
        self.menu_trigger = True
        self.menu_picture = pygame.image.load('textures/Menu.png').convert()

        # Параметры оружия
        self.weapon_base_sprite = pygame.image.load('sprites/Arm/main/0.png').convert_alpha()
        self.weapon_shot_animation = deque([pygame.image.load(f'sprites/Arm/Shoot/{i}.png').convert_alpha()
                                            for i in range(36)])
        self.weapon_rect = self.weapon_base_sprite.get_rect()
        self.weapon_pos = (width - self.weapon_rect.width, height - self.weapon_rect.height)
        self.shot_length = len(self.weapon_shot_animation)
        self.shot_length_count = 0
        self.shot_animation_speed = 2
        self.shot_animation_count = 0
        self.shot_animation_trigger = True
        self.shot_sound = pygame.mixer.Sound('sound/Shoot.mp3')

        # Параметры вспышки от выстрела
        self.sfx = deque([pygame.image.load(f'sprites/Sfx/{i}.png').convert_alpha() for i in range(6)])
        self.sfx_length_count = 0
        self.sfx_length = len(self.sfx)

        # Отрисовка заднего фона
    def background(self, angle):
        sky_offset = -20 * math.degrees(angle) % width
        self.screen.blit(self.textures['S'], (sky_offset, 0))
        self.screen.blit(self.textures['S'], (sky_offset - width, 0))
        self.screen.blit(self.textures['S'], (sky_offset + width, 0))
        self.screen.blit(self.textures['F'], (0, half_height))

        # Отрисовка мира
    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.screen.blit(object, object_pos)

        # Отрисовка мини карты
    def mini_map(self, player):
        self.screen_map.fill(black)
        map_x, map_y = player.x // map_scale, player.y // map_scale
        pygame.draw.line(self.screen_map, green, (map_x, map_y), (map_x + 12 * math.cos(player.angle),
                                                 map_y + 12 * math.sin(player.angle)), 2)
        pygame.draw.circle(self.screen_map, green, (int(map_x), int(map_y)), 5)
        for x, y in map_generator.mini_map:
            pygame.draw.rect(self.screen_map, white, (x, y, map_tile, map_tile))
        self.screen.blit(self.screen_map, map_pos)

        # Отрисовка руки с оружием
    def player_weapon(self, shots):
        if self.player.shot:
            if not self.shot_length_count:
                self.shot_sound.play()
            self.shot_projection = min(shots)[1] // 2
            self.bullet_sfx()
            shot_sprite = self.weapon_shot_animation[0]
            self.screen.blit(shot_sprite, self.weapon_pos)
            self.shot_animation_count += 1
            if self.shot_animation_count == self.shot_animation_speed:
                self.weapon_shot_animation.rotate(-1)
                self.shot_animation_count = 0
                self.shot_length_count += 1
                self.shot_animation_trigger = False
            if self.shot_length_count == self.shot_length:
                self.player.shot = False
                self.shot_length_count = 0
                self.sfx_length_count = 0
                self.shot_animation_trigger = True
        else:
            self.screen.blit(self.weapon_base_sprite, self.weapon_pos)

        # Отрисовка вспышки от выстрела
    def bullet_sfx(self):
        if self.sfx_length_count < self.sfx_length:
            sfx = pygame.transform.scale(self.sfx[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx.get_rect()
            self.screen.blit(sfx, (half_width - sfx_rect.w // 2, half_height - sfx_rect.h // 2))
            self.sfx_length_count += 1
            self.sfx.rotate(-1)

        # Отрисовка очков
    def draw_ui(self, score, add_score, factor):
        display_score = "Очки: " + str(int(score))
        render = self.font.render(display_score, 0, white)
        self.screen.blit(render, (5, 5))
        if factor != 0:
            display_score_add = str(int(add_score)) + " * " + str(int(factor))
            render = self.font.render(display_score_add, 0, white)
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
        rect.center = half_width, half_height
        pygame.draw.rect(self.screen, gray, rect, border_radius=50)
        self.screen.blit(render, (rect.centerx - 450, rect.centery - 180))
        self.screen.blit(score_text, (rect.centerx - 450, rect.centery - 70))
        # Кнопка продолжения на победном экране
        next = button_font.render('CONTINUE', 1, pygame.Color('lightgray'))
        button_next = pygame.Rect(0, 0, 450, 150)
        button_next.center = half_width - 250, half_height + 100

        pygame.draw.rect(self.screen, black, button_next, border_radius=25, width=10)
        self.screen.blit(next, (button_next.centerx - 210, button_next.centery - 40))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if button_next.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, black, button_next, border_radius=25)
            self.screen.blit(next, (button_next.centerx - 210, button_next.centery - 40))
            if mouse_click[0]:
                with open('ScoreSave/High_Scores.txt', 'r+') as HS_file:
                    lines = HS_file.readlines()
                    if int(lines[lvl - 1]) < score:
                        lines[lvl - 1] = (str(int(score)) + '\n')
                    HS_file.seek(0)
                    for line in lines:
                        HS_file.write(line)
                (map_generator.matrix_map, map_generator.world_width, map_generator.world_height, 
                map_generator.world_map, map_generator.mini_map, map_generator.collision_walls) = map_generator.mapCreate(lvl + 1)
                self.sprites.list_of_objects = self.sprites.map_fill(lvl + 1)
                self.player.x = 150
                self.player.y = 150
                self.player.angle = 0
                pygame.mixer.music.stop()
                if lvl < 3:
                    pygame.mixer.music.load('sound/%d.mp3' % (lvl + 1))
                else:
                    pygame.mixer.music.load('sound/1.mp3')
                pygame.mixer.music.play()
                pygame.mouse.set_visible(False)
        # Кнопка выхода на победном экране
        exit = button_font.render('EXIT', 1, pygame.Color('lightgray'))
        button_exit = pygame.Rect(0, 0, 450, 150)
        button_exit.center = half_width + 250, half_height + 100

        pygame.draw.rect(self.screen, black, button_exit, border_radius=25, width=10)
        self.screen.blit(exit, (button_exit.centerx - 100, button_exit.centery - 40))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if button_exit.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, black, button_exit, border_radius=25)
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
        rect.center = half_width, half_height
        pygame.draw.rect(self.screen, red, rect, border_radius=50)
        self.screen.blit(render, (rect.centerx - 270, rect.centery - 140))
        # Кнопка рестарта экрана поражения
        restart = button_font.render('RESTART', 1, pygame.Color('lightgray'))
        button_restart = pygame.Rect(0, 0, 450, 150)
        button_restart.center = half_width - 250, half_height + 100

        pygame.draw.rect(self.screen, black, button_restart, border_radius=25, width=10)
        self.screen.blit(restart, (button_restart.centerx - 180, button_restart.centery - 40))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if button_restart.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, black, button_restart, border_radius=25)
            self.screen.blit(restart, (button_restart.centerx - 180, button_restart.centery - 40))
            if mouse_click[0]:
                (map_generator.matrix_map, map_generator.world_width, map_generator.world_height, 
                map_generator.world_map, map_generator.mini_map, map_generator.collision_walls) = map_generator.mapCreate(1)
                self.sprites.list_of_objects = self.sprites.map_fill(1)
                self.player.x = 150
                self.player.y = 150
                self.player.angle = 0
                pygame.mixer.music.stop()
                pygame.mixer.music.load('sound/1.mp3')
                pygame.mixer.music.play()
                pygame.mouse.set_visible(False)
                self.dead = False
        # Кнопка выхода экрана поражения
        exit = button_font.render('EXIT', 1, pygame.Color('lightgray'))
        button_exit = pygame.Rect(0, 0, 450, 150)
        button_exit.center = half_width + 250, half_height + 100

        pygame.draw.rect(self.screen, black, button_exit, border_radius=25, width=10)
        self.screen.blit(exit, (button_exit.centerx - 100, button_exit.centery - 40))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if button_exit.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, black, button_exit, border_radius=25)
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
        start = button_font.render('START', 1, yellow)
        button_start = pygame.Rect(0, 0, 400, 150)
        button_start.center = half_width, half_height
        # Кнопка выхода
        exit = button_font.render('EXIT', 1, yellow)
        button_exit = pygame.Rect(0, 0, 400, 150)
        button_exit.center = half_width, half_height + 200

        while self.menu_trigger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.menu_picture, (0, 0), (x % width, height * 0.8, width, height))
            x += 1

            pygame.draw.rect(self.screen, black, button_start, border_radius=25, width=10)
            self.screen.blit(start, (button_start.centerx - 130, button_start.centery - 40))

            pygame.draw.rect(self.screen, black, button_exit, border_radius=25, width=10)
            self.screen.blit(exit, (button_exit.centerx - 100, button_exit.centery - 40))

            label = button_font.render('project', 1, (0, 0, 0))
            self.screen.blit(label, (400, 90))
            label = label_font.render('M.I.G.P.R.G.', 1, (0, 0, 0))
            self.screen.blit(label, (150, 150))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if button_start.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, black, button_start, border_radius=25)
                self.screen.blit(start, (button_start.centerx - 130, button_start.centery - 40))
                if mouse_click[0]:
                    self.menu_trigger = False
            elif button_exit.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, black, button_exit, border_radius=25)
                self.screen.blit(exit, (button_exit.centerx - 100, button_exit.centery - 40))
                if mouse_click[0]:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(20)