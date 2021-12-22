from settings import *
import pygame
import math
import map_generator
from sprite_objects import SpriteObject

class Player:
    def __init__(self, sprites):
        self.pos_x, self.pos_y = player_pos
        self.sprites = sprites
        self.player_view_angle = player_view_angle
        # Параметры коллизий
        self.collision_side = 50
        self.collision_rectangle = pygame.Rect(self.pos_x, self.pos_y, self.collision_side, self.collision_side)
        # Оружие
        self.shoot = False

    @property
    def position(self):
        return (self.pos_x, self.pos_y)

    @property
    def collision_list(self):
        return map_generator.collision_walls + [pygame.Rect(*obj.pos, obj.collision_side, obj.collision_side) for obj in
                                  self.sprites.list_of_objects if obj.walkable]

        # Обнаружение коллизий
    def collision_detect(self, step_x, step_y):
        # step_x, step_y - перемещение игрока на один "шаг" по соответствующим осям
        future_rect = self.collision_rectangle.copy()
        # Положение персонажа, после совершения "шага"
        future_rect.move_ip(step_x, step_y)
        # индекс стены, с которой столкнётся игрок, если совершит "шаг"
        coll_indexes = future_rect.collidelistall(self.collision_list)
        if len(coll_indexes):
            delta_x, delta_y = 0, 0
            for coll_index in coll_indexes:
                coll_rect = self.collision_list[coll_index]
                if step_x > 0:
                    delta_x += future_rect.right - coll_rect.left
                else:
                    delta_x += coll_rect.right - future_rect.left
                if step_y > 0:
                    delta_y += future_rect.bottom - coll_rect.top
                else:
                    delta_y += coll_rect.bottom - future_rect.top
            # игрок упёрся в угол
            if abs(delta_x - delta_y) < 10:
                step_x, step_y = 0, 0
            # игрок столкнулся с вертикальной стеной
            elif delta_x > delta_y:
                step_y = 0
            #игрок столкнулся с горизонтальной стеной
            elif delta_y > delta_x:
                step_x = 0
        self.pos_x += step_x
        self.pos_y += step_y

        # Перемещение персонажа
    def movement(self):
        sin_a = math.sin(self.player_view_angle)
        cos_a = math.cos(self.player_view_angle)

        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            speed = 5
        else:
            speed = 3
        if pygame.key.get_pressed()[pygame.K_w]:
            step_x = speed * cos_a
            step_y = speed * sin_a
            self.collision_detect(step_x, step_y)
        if pygame.key.get_pressed()[pygame.K_s]:
            step_x = -speed * cos_a
            step_y = -speed * sin_a
            self.collision_detect(step_x, step_y)
        if pygame.key.get_pressed()[pygame.K_a]:
            step_x = speed / 1.5 * sin_a
            step_y = -speed / 1.5 * cos_a
            self.collision_detect(step_x, step_y)
        if pygame.key.get_pressed()[pygame.K_d]:
            step_x = -speed / 1.5 * sin_a
            step_y = speed / 1.5 * cos_a
            self.collision_detect(step_x, step_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.shoot:
                    self.shoot = True

        self.player_view_angle += pygame.mouse.get_rel()[0] / 400
        self.collision_rectangle.center = self.pos_x, self.pos_y
        self.player_view_angle %= 2 * math.pi

