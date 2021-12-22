import pygame
from settings import *
from collections import deque
from ray_casting import mapping
from numba.core import types
from numba.typed import Dict
from numba import int32
import map_generator
import random


class Sprites:
    def __init__(self):

        self.sprites_properties = {
            'fire':{
                'sprite': pygame.image.load('sprites/fire/main/0.png').convert_alpha(),
                'viewing_angles': False,
                'shift': -2.7,
                'size': (0.5, 0.5),
                'collision_side': 30,
                'animation': deque([pygame.image.load(f'sprites/fire/anim/{i}.png').convert_alpha() for i in range(24, 1, -1)]),
                'death_animation': [],
                'dead': 'immortal',
                'dead_shift': 1.8,
                'animation_distance': 800,
                'animation_speed': 3,
                'walkable': False,
                'type': 'decor',
                'obj_action': []
            },

                'column':{
                'sprite': [pygame.image.load(f'sprites/Column/main/{i}.png') .convert_alpha() for i in range(36)],
                'viewing_angles': True,
                'shift': 0.1,
                'size': (1.2, 1.2),
                'collision_side': 50,
                'animation': pygame.image.load('sprites/column/main/0.png') .convert_alpha(),
                'death_animation': [],
                'dead': 'immortal',
                'dead_shift': 1.8,
                'animation_distance': 1,
                'animation_speed': 10,
                'walkable': True,
                'type': 'decor',
                'obj_action': []
            },

            'sphere':{
                'sprite': pygame.image.load('sprites/Sphere/main/0.png').convert_alpha(),
                'viewing_angles': False,
                'shift': 0.15,
                'size': (1, 1),
                'collision_side': 50,
                'animation': pygame.image.load('sprites/Sphere/main/0.png').convert_alpha(),
                'death_animation': deque([pygame.image.load(f'sprites/Sphere/destroy/{i}.png').convert_alpha() for i in range(6)]),
                'dead': False,
                'dead_shift': 0.35,
                'animation_distance': 1,
                'animation_speed': 2,
                'walkable': True,
                'type': 'decor',
                'obj_action': []
            },

            'enemy':{
                'sprite': [pygame.image.load(f'sprites/Enemy/main/{i}.png') .convert_alpha() for i in range(36)],
                'viewing_angles': True,
                'shift': 0.2,
                'size': (1.2, 1.2),
                'collision_side': 50,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/Enemy/Die/{i}.png').convert_alpha() for i in range(9)]),
                'dead': False,
                'dead_shift': 0.2,
                'animation_distance': None,
                'animation_speed': 2,
                'walkable': True,
                'type': 'enemy',
                'obj_action': deque([pygame.image.load(f'sprites/enemy/EnemyAtack/{i}.png').convert_alpha() for i in range(8)]),
            },

            'door_vertical':{
                'sprite': [pygame.image.load(f'sprites/Door_v/{i}.png') .convert_alpha() for i in range(36)],
                'viewing_angles': True,
                'shift': 0.3,
                'size': (1.9, 1.3),
                'collision_side': 100,
                'animation': [],
                'death_animation': [],
                'dead': 'immortal',
                'dead_shift': 0,
                'animation_distance': 0,
                'animation_speed': 0,
                'walkable': True,
                'type': 'door_h',
                'obj_action': []
            },

            'door_horisontal':{
                'sprite': [pygame.image.load(f'sprites/Door_h/{i}.png') .convert_alpha() for i in range(36)],
                'viewing_angles': True,
                'shift': 0.31,
                'size': (1.9, 1.3),
                'collision_side': 100,
                'animation': [],
                'death_animation': [],
                'dead': 'immortal',
                'dead_shift': 0,
                'animation_distance': 0,
                'animation_speed': 0,
                'walkable': True,
                'type': 'door_v',
                'obj_action': []
            },
        }
        self.list_of_objects = self.map_fill(1)

    # Заполнение карты спрайтами
    def map_fill(self, lvl):
        if lvl == 1:
            list_of_objects = [SpriteObject(self.sprites_properties['sphere'], (5.5, 2.5)),
                SpriteObject(self.sprites_properties['enemy'], (10.5, 2.5)),
                SpriteObject(self.sprites_properties['enemy'], (1.5, 6.5)),]
        elif lvl == 2:
            list_of_objects = [SpriteObject(self.sprites_properties['sphere'], (6, 6)),
                SpriteObject(self.sprites_properties['enemy'], (7, 4)),
                SpriteObject(self.sprites_properties['enemy'], (14, 4)),
                SpriteObject(self.sprites_properties['enemy'], (16, 7)),
                SpriteObject(self.sprites_properties['enemy'], (4, 12)),
                SpriteObject(self.sprites_properties['column'], (4, 4)),
                SpriteObject(self.sprites_properties['door_vertical'], (11.5, 12.5)),
                SpriteObject(self.sprites_properties['door_horisontal'], (1.5, 8.5))]
        elif lvl == 3:
            list_of_objects = [SpriteObject(self.sprites_properties['fire'], (10.5, 8.5)),
                SpriteObject(self.sprites_properties['column'], (10.5, 8.5)),
                SpriteObject(self.sprites_properties['fire'], (10.5, 6.5)),
                SpriteObject(self.sprites_properties['column'], (10.5, 6.5)),
                SpriteObject(self.sprites_properties['fire'], (10.5, 4.5)),
                SpriteObject(self.sprites_properties['column'], (10.5, 4.5)),
                SpriteObject(self.sprites_properties['fire'], (13.5, 8.5)),
                SpriteObject(self.sprites_properties['column'], (13.5, 8.5)),
                SpriteObject(self.sprites_properties['fire'], (13.5, 6.5)),
                SpriteObject(self.sprites_properties['column'], (13.5, 6.5)),
                SpriteObject(self.sprites_properties['fire'], (13.5, 4.5)),
                SpriteObject(self.sprites_properties['column'], (13.5, 4.5)),
                SpriteObject(self.sprites_properties['enemy'], (12.5, 4.5)),
                SpriteObject(self.sprites_properties['enemy'], (21, 4.5)),
                SpriteObject(self.sprites_properties['enemy'], (19.5, 8.5)),
                SpriteObject(self.sprites_properties['enemy'], (22.5, 14)),
                SpriteObject(self.sprites_properties['enemy'], (3.5, 4.5)),
                SpriteObject(self.sprites_properties['enemy'], (4.5, 14.5)),
                SpriteObject(self.sprites_properties['sphere'], (4.5, 7.5)),
                SpriteObject(self.sprites_properties['sphere'], (8.5, 12.5)),
                SpriteObject(self.sprites_properties['door_horisontal'], (20.5, 10.5))]
        else:
            list_of_objects = []
            while len(list_of_objects) <= 1:
                for i in range(len(map_generator.map_list)):
                    for j in range(len(map_generator.map_list[i])):
                        if i > 5 and j > 5 and map_generator.map_list[i][j] == False and random.randint(0, 10) > 9:
                            list_of_objects.append(SpriteObject(self.sprites_properties['enemy'], (j + 0.5, i + 0.5)))
        return list_of_objects

        

    @property
    def sprite_shoot(self):
        return min([obj.is_on_fire for obj in self.list_of_objects], default=(float('inf'), 0))

    @property
    def blocked_doors(self):
        blocked_doors = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
        for obj in self.list_of_objects:
            if obj.type in {'door_h', 'door_v'} and obj.walkable:
                i, j = mapping(obj.x_pos, obj.y_pos)
                blocked_doors[(i, j)] = 0
        return blocked_doors

# Местоположение спрайта и его начальные характеристики
class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite'].copy()
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.size = parameters['size']
        self.animation = parameters['animation']

        self.death_animation = parameters['death_animation'].copy()
        self.dead = parameters['dead']
        self.dead_shift = parameters['dead_shift']

        self.animation_distance = parameters['animation_distance']
        self.animation_speed = parameters['animation_speed']
        self.walkable = parameters['walkable']
        self.type = parameters['type']
        self.obj_action = parameters['obj_action'].copy()
        self.collision_side = parameters['collision_side']
        self.dead_animation_count = 0
        self.animation_count = 0
        self.x_pos, self.y_pos = pos[0] * tile, pos[1] * tile
        self.enemy_action_trigger = False
        self.door_open_trigger = False
        self.door_prev_pos = self.y_pos if self.type == 'door_h' else self.x_pos
        self.delete = False


        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 10)) for i in range(0, 360, 10)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    @property
    def is_on_fire(self):
        if center_ray - self.collision_side // 2 < self.current_ray < center_ray + self.collision_side // 2 and self.walkable:
            return self.distance_to_sprite, self.proj_height
        return float('inf'), None

    @property
    def pos(self):
        return self.x_pos - self.collision_side // 2, self.y_pos - self.collision_side // 2

    def object_locate(self, player):
        

        dx, dy = self.x_pos - player.pos_x, self.y_pos - player.pos_y
        self.distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.player_view_angle
        if dx > 0 and 180 <= math.degrees(player.player_view_angle) <= 360 or dx < 0 and dy < 0:
            gamma += 2 * math.pi

        delta_rays = int(gamma / delta_angle)
        self.current_ray = center_ray + delta_rays
        if self.type not in {'door_h', 'door_v'}:
            self.distance_to_sprite *= math.cos(field_of_view / 2 - self.current_ray * delta_angle)

        fake_ray = self.current_ray + fake_rays
        if 0 <= fake_ray <= fake_rays_range and self.distance_to_sprite > 30:
            self.proj_height = min(int(proj_coeff / self.distance_to_sprite), 2 * screen_height if self.type not in {'door_h', 'door_v'} else screen_height)
            sprite_width = int(self.proj_height * self.size[0])
            sprite_height = int(self.proj_height * self.size[1])
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_height // 2
            shift = half_sprite_width * self.shift

            # Логика для объектов
            if self.type in {'door_h', 'door_v'}:
                if self.door_open_trigger:
                    self.open_door()
                self.object = self.visible_sprite()
                sprite_object = self.sprite_animation()
            else:
                if self.dead and self.dead != 'immortal':
                    sprite_object = self.dead_animation()
                    shift = half_sprite_height * self.dead_shift
                elif self.enemy_action_trigger:
                    sprite_object = self.enemy_in_action()
                else:
                    self.object = self.visible_sprite()
                    sprite_object = self.sprite_animation()
            

            # Размер и позиция спрайта
            sprite_pos = (self.current_ray * scale - half_sprite_width, screen_height / 2 - half_sprite_width + shift)
            sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_height))
            return (self.distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)

    # Анимация спрайтов
    def sprite_animation(self):
        if self.animation and self.distance_to_sprite < self.animation_distance:
            sprite_object = self.animation[0]
            if self.animation_count < self.animation_speed:
                self.animation_count +=1
            else:
                self.animation.rotate()
                self.animation_count = 0
            return sprite_object
        return self.object

    def visible_sprite(self):
        if self.viewing_angles:
            if self.theta < 0:
                self.theta += 2 * math.pi
            self.theta = 360 - int(math.degrees(self.theta))

            for angles in self.sprite_angles:
                if self.theta in angles:
                    return self.sprite_positions[angles]
        return self.object

    # Анимация смерти
    def dead_animation(self):
        if len(self.death_animation):
            if self.dead_animation_count < self.animation_speed:
                self.dead_sprite = self.death_animation[0]
                self.dead_animation_count += 1
            else:
                self.dead_sprite = self.death_animation.popleft()
                self.dead_animation_count = 0
        return self.dead_sprite

    # Анимация атаки
    def enemy_in_action(self):
        sprite_object = self.obj_action[0]
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.obj_action.rotate()
            self.animation_count = 0
        return sprite_object

    # Анимация открытия двери
    def open_door(self):
        if self.type == 'door_h':
            self.y_pos -= 3
            if abs(self.y_pos - self.door_prev_pos) > tile:
                self.delete = True
        elif self.type == 'door_v':
            self.x_pos -= 3
            if abs(self.x_pos - self.door_prev_pos) > tile:
                self.delete = True
