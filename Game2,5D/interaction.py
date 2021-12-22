from settings import *
import map_generator
from ray_casting import mapping
import math
import pygame
from numba import njit
import sys


# Находится ли персонаж в прямой видимости с врагом
njit(fastmath = True, cache = True)
def ray_casting_enemy_player(npc_x, npc_y, blocked_doors, world_map, player_pos):
    # Начальные координаты луча
    pos_x, pos_y = player_pos
    x_tile, y_tile, = mapping(pos_x, pos_y)
    # Текущий угол направления игрока
    current_angle = player_view_angle - field_of_view / 2
    # Синусы и косинусы каправлений лучей
    delta_x, delta_y = pos_x - npc_x, pos_y - npc_y
    current_angle = math.atan2(delta_y, delta_x)
    current_angle += math.pi

    ray_sin = math.sin(current_angle)
    ray_sin = ray_sin if ray_sin else 0.000001
    ray_cos = math.cos(current_angle)
    ray_cos = ray_cos if ray_cos else 0.000001

    # Вертикали
    if ray_cos >= 0:
        # Текущаа вертикаль
        x = x_tile + tile
        # Вспомогательная переменная для вычисления очередной вертикали
        next_x = 1
    else:
        x = x_tile
        next_x = -1
    for i in range(0, int(abs(delta_x)) // tile):
        # Расстояние до вертикали
        vertical_depth = (x - pos_x) / ray_cos
        # Координата y вертикали
        yv = pos_y + vertical_depth * ray_sin
        vertical_tile = mapping(x + next_x, yv)
        if vertical_tile in world_map or vertical_tile in blocked_doors:
            return False
        x += next_x * tile

    # Горизонтали
    if ray_sin >= 0:
        y = y_tile + tile
        next_y = 1
    else:
        y = y_tile
        next_y = -1
    for i in range(0, int(abs(delta_y)) // tile):
        horisontal_depth = (y - pos_y) / ray_sin
        xh = pos_x + horisontal_depth * ray_cos
        horisontal_tile = mapping(xh, y + next_y)
        if horisontal_tile in world_map or horisontal_tile in blocked_doors:
            return False
        y += next_y * tile
    return True


class Interaction:
    def __init__(self, player, sprites, drawing):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing
        self.death_sound = pygame.mixer.Sound('sound/MonsterPain.mp3')
        self.lives = 1
        self.score = 0
        self.add_score = 0
        self.factor = 0
        self.counter = 0
        self.last = pygame.time.get_ticks()
        self.cooldown = 3000
        self.lvl = 1

    # Действия при выстреле по объекту
    def interaction_objects(self):
        if self.player.shoot and self.drawing.shoot_animation_trigger:
            for obj in sorted(self.sprites.list_of_objects, key=lambda obj: obj.distance_to_sprite):
                if obj.is_on_fire[1]:
                    if obj.dead != 'immortal' and not obj.dead:
                        if ray_casting_enemy_player(obj.x_pos, obj.y_pos,
                                                  self.sprites.blocked_doors,
                                                  map_generator.world_map, self.player.position):
                            if obj.type == 'enemy':
                                self.death_sound.play()
                            obj.dead = True
                            obj.walkable = False

                            self.add_score += 100
                            self.factor += 1

                            self.drawing.shoot_animation_trigger = False
                    if obj.type in {'door_h', 'door_v'} and obj.distance_to_sprite < tile:
                        obj.door_open_trigger = True
                        obj.walkable = False
                    break

    # Анимация атаки врага
    def enemy_action(self, player_x, player_y):
        for obj in self.sprites.list_of_objects:
            if obj.type == 'enemy' and not obj.dead:
                if ray_casting_enemy_player(obj.x_pos, obj.y_pos, self.sprites.blocked_doors, map_generator.world_map, self.player.position):
                    obj.enemy_action_trigger = True
                    self.enemy_move(obj, player_x, player_y)
                else:
                    obj.enemy_action_trigger = False

    # Перемещение врага
    def enemy_move(self, obj, player_x, player_y):
        if obj.distance_to_sprite > tile:
            x_distance = obj.x_pos - self.player.position[0]
            y_distance = obj.y_pos - self.player.position[1]

            if x_distance < -2:
                obj.x_pos = obj.x_pos + 2
            elif x_distance < -1:
                obj.x_pos = obj.x_pos + 1
            elif x_distance < -0.5:
                obj.x_pos = obj.x_pos + 0.5
            elif x_distance > 2:
                obj.x_pos = obj.x_pos - 2
            elif x_distance > 1:
                obj.x_pos = obj.x_pos - 1
            elif x_distance > 0.5:
                obj.x_pos = obj.x_pos - 0.5

            if y_distance < -2:
                obj.y_pos = obj.y_pos + 2
            elif y_distance < -1:
                obj.y_pos = obj.y_pos + 1
            elif y_distance < -0.5:
                obj.y_pos = obj.y_pos + 0.5
            elif y_distance > 2:
                obj.y_pos = obj.y_pos -2
            elif y_distance > 1:
                obj.y_pos = obj.y_pos - 1
            elif y_distance > 0.5:
                obj.y_pos = obj.y_pos - 0.5

        if abs(player_x - obj.x_pos) < tile and abs(player_y - obj.y_pos) < tile:
            self.lives = 0

    # Очищение объектов
    def clear_objects(self):
        deleted_objects = self.sprites.list_of_objects[:]
        [self.sprites.list_of_objects.remove(obj) for obj in deleted_objects if obj.delete]

    # Воспроизведение музыки
    def play_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load('sound/1.mp3')
        pygame.mixer.music.play(10)
    
    # Выигрыш
    def win(self):
        if not len([obj for obj in self.sprites.list_of_objects if obj.type == 'enemy' and not obj.dead]):
            self.score += self.add_score * self.factor
            pygame.time.delay(500)
            pygame.mixer.music.stop()
            pygame.mixer.music.load('sound/Victory.mp3')
            pygame.mixer.music.play()
            pygame.mouse.set_visible(True)
            while not len([obj for obj in self.sprites.list_of_objects if obj.type == 'enemy' and not obj.dead]):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                self.drawing.win(self.score, self.lvl)
            self.lvl += 1
            self.score = 0
            self.factor = 0
            self.add_score = 0

    # Проигрыш
    def check_status(self):
        self.drawing.draw_ui(self.score, self.add_score, self.factor)

        now = pygame.time.get_ticks()
        if now - self.last >= self.cooldown and self.factor == self.counter and self.factor != 0:
            self.last = now
            self.score += self.add_score * self.factor
            self.counter = 0
            self.factor = 0
            self.add_score = 0
        elif now - self.last >= self.cooldown and self.factor > self.counter:
            self.last = now
            self.counter = self.factor

        if self.lives < 1:
            self.drawing.dead = True
            pygame.time.delay(500)
            pygame.mixer.music.stop()
            pygame.mixer.music.load('sound/Lose.mp3')
            pygame.mixer.music.play()
            pygame.mouse.set_visible(True)
            while self.drawing.dead:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                self.drawing.lose()
            self.lives = 1
            self.lvl = 1
            self.score = 0
            self.factor = 0
            self.add_score = 0


