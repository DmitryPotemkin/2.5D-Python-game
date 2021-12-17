from settings import *
import pygame
import math
import map_generator
from sprite_objects import SpriteObject

class Player:
    def __init__(self, sprites):
        self.x, self.y = player_pos
        self.sprites = sprites
        self.angle = player_angle
        # Параметры коллизий
        self.side = 50
        self.rect = pygame.Rect(*player_pos, self.side, self.side)
        # Оружие
        self.shot = False

    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def collision_list(self):
        return map_generator.collision_walls + [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  self.sprites.list_of_objects if obj.blocked]

        # Обнаружение коллизий
    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collision_list)
        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = self.collision_list[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top

            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy

        # Перемещение персонажа
    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            player_speed = 5
        else:
            player_speed = 3
        if keys[pygame.K_w]:
            dx = player_speed * cos_a
            dy = player_speed * sin_a
            self.detect_collision(dx, dy)
            lvl = 2
        if keys[pygame.K_s]:
            dx = -player_speed * cos_a
            dy = -player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = player_speed / 1.5 * sin_a
            dy = -player_speed / 1.5 * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_d]:
            dx = -player_speed / 1.5 * sin_a
            dy = player_speed / 1.5 * cos_a
            self.detect_collision(dx, dy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.shot:
                    self.shot = True

        self.angle += pygame.mouse.get_rel()[0] / 400
        self.rect.center = self.x, self.y
        self.angle %= double_pi

