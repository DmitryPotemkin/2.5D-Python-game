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

        self.sprite_parameters = {
            'sprite_fire':{
                'sprite': pygame.image.load('sprites/fire/main/0.png') .convert_alpha(),
                'viewing_angles': False,
                'shift': -2.7,
                'scale': (0.5, 0.5),
                'side': 30,
                'animation': deque([pygame.image.load(f'sprites/fire/anim/{i}.png').convert_alpha() for i in range(24, 1, -1)]),
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 1.8,
                'animation_dist': 800,
                'animation_speed': 3,
                'blocked': False,
                'flag': 'decor',
                'obj_action': []
            },

                'sprite_column':{
                'sprite': [pygame.image.load(f'sprites/Column/main/{i}.png') .convert_alpha() for i in range(36)],
                'viewing_angles': True,
                'shift': 0.1,
                'scale': (1.2, 1.2),
                'side': 50,
                'animation': pygame.image.load('sprites/column/main/0.png') .convert_alpha(),
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 1.8,
                'animation_dist': 1,
                'animation_speed': 10,
                'blocked': True,
                'flag': 'decor',
                'obj_action': []
            },

            'sprite_sphere':{
                'sprite': pygame.image.load('sprites/Sphere/main/0.png').convert_alpha(),
                'viewing_angles': False,
                'shift': 0.15,
                'scale': (1, 1),
                'side': 50,
                'animation': pygame.image.load('sprites/Sphere/main/0.png').convert_alpha(),
                'death_animation': deque([pygame.image.load(f'sprites/Sphere/destroy/{i}.png').convert_alpha() for i in range(6)]),
                'is_dead': None,
                'dead_shift': 0.35,
                'animation_dist': 1,
                'animation_speed': 2,
                'blocked': True,
                'flag': 'decor',
                'obj_action': []
            },

            'sprite_enemy':{
                'sprite': [pygame.image.load(f'sprites/Enemy/main/{i}.png') .convert_alpha() for i in range(36)],
                'viewing_angles': True,
                'shift': 0.2,
                'scale': (1.2, 1.2),
                'side': 50,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/Enemy/Die/{i}.png').convert_alpha() for i in range(9)]),
                'is_dead': None,
                'dead_shift': 0.2,
                'animation_dist': None,
                'animation_speed': 2,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque([pygame.image.load(f'sprites/enemy/EnemyAtack/{i}.png').convert_alpha() for i in range(8)]),
            },

            'sprite_door_v':{
                'sprite': [pygame.image.load(f'sprites/Door_v/{i}.png') .convert_alpha() for i in range(36)],
                'viewing_angles': True,
                'shift': 0.3,
                'scale': (1.9, 1.3),
                'side': 100,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 0,
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': True,
                'flag': 'door_h',
                'obj_action': []
            },

            'sprite_door_h':{
                'sprite': [pygame.image.load(f'sprites/Door_h/{i}.png') .convert_alpha() for i in range(36)],
                'viewing_angles': True,
                'shift': 0.31,
                'scale': (1.9, 1.3),
                'side': 100,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 0,
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': True,
                'flag': 'door_v',
                'obj_action': []
            },
        }
        self.list_of_objects = self.map_fill(1)
    def map_fill(self, lvl):
        if lvl == 1:
            list_of_objects = [SpriteObject(self.sprite_parameters['sprite_sphere'], (5.5, 2.5)),
                SpriteObject(self.sprite_parameters['sprite_enemy'], (10.5, 2.5)),
                SpriteObject(self.sprite_parameters['sprite_enemy'], (1.5, 6.5)),]
        elif lvl == 2:
            list_of_objects = [SpriteObject(self.sprite_parameters['sprite_sphere'], (6, 6)),
                SpriteObject(self.sprite_parameters['sprite_enemy'], (7, 4)),
                SpriteObject(self.sprite_parameters['sprite_enemy'], (14, 4)),
                SpriteObject(self.sprite_parameters['sprite_enemy'], (16, 7)),
                SpriteObject(self.sprite_parameters['sprite_enemy'], (4, 12)),
                SpriteObject(self.sprite_parameters['sprite_column'], (4, 4)),
                SpriteObject(self.sprite_parameters['sprite_door_v'], (11.5, 12.5)),
                SpriteObject(self.sprite_parameters['sprite_door_h'], (1.5, 8.5))]
        elif lvl == 3:
            list_of_objects = [SpriteObject(self.sprite_parameters['sprite_fire'], (10.5, 8.5)),
                SpriteObject(self.sprite_parameters['sprite_column'], (10.5, 8.5)),
                SpriteObject(self.sprite_parameters['sprite_fire'], (10.5, 6.5)),
                SpriteObject(self.sprite_parameters['sprite_column'], (10.5, 6.5)),
                SpriteObject(self.sprite_parameters['sprite_fire'], (10.5, 4.5)),
                SpriteObject(self.sprite_parameters['sprite_column'], (10.5, 4.5)),
                SpriteObject(self.sprite_parameters['sprite_fire'], (13.5, 8.5)),
                SpriteObject(self.sprite_parameters['sprite_column'], (13.5, 8.5)),
                SpriteObject(self.sprite_parameters['sprite_fire'], (13.5, 6.5)),
                SpriteObject(self.sprite_parameters['sprite_column'], (13.5, 6.5)),
                SpriteObject(self.sprite_parameters['sprite_fire'], (13.5, 4.5)),
                SpriteObject(self.sprite_parameters['sprite_column'], (13.5, 4.5)),
                SpriteObject(self.sprite_parameters['sprite_enemy'], (12.5, 4.5)),
                SpriteObject(self.sprite_parameters['sprite_enemy'], (21, 4.5)),
                SpriteObject(self.sprite_parameters['sprite_enemy'], (19.5, 8.5)),
                SpriteObject(self.sprite_parameters['sprite_enemy'], (22.5, 14)),
                SpriteObject(self.sprite_parameters['sprite_enemy'], (3.5, 4.5)),
                SpriteObject(self.sprite_parameters['sprite_enemy'], (4.5, 14.5)),
                SpriteObject(self.sprite_parameters['sprite_sphere'], (4.5, 7.5)),
                SpriteObject(self.sprite_parameters['sprite_sphere'], (8.5, 12.5)),
                SpriteObject(self.sprite_parameters['sprite_door_h'], (20.5, 10.5))]
        else:
            list_of_objects = []
            while len(list_of_objects) <= 1:
                for i in range(len(map_generator.matrix_map)):
                    for j in range(len(map_generator.matrix_map[i])):
                        if i > 5 and j > 5 and map_generator.matrix_map[i][j] == False and random.randint(0, 10) > 9:
                            list_of_objects.append(SpriteObject(self.sprite_parameters['sprite_enemy'], (j + 0.5, i + 0.5)))
        return list_of_objects

        

    @property
    def sprite_shot(self):
        return min([obj.is_on_fire for obj in self.list_of_objects], default=(float('inf'), 0))

    @property
    def blocked_doors(self):
        blocked_doors = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
        for obj in self.list_of_objects:
            if obj.flag in {'door_h', 'door_v'} and obj.blocked:
                i, j = mapping(obj.x, obj.y)
                blocked_doors[(i, j)] = 0
        return blocked_doors

class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite'].copy()
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation']

        self.death_animation = parameters['death_animation'].copy()
        self.is_dead = parameters['is_dead']
        self.dead_shift = parameters['dead_shift']

        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.flag = parameters['flag']
        self.obj_action = parameters['obj_action'].copy()
        self.side = parameters['side']
        self.dead_animation_count = 0
        self.animation_count = 0
        self.x, self.y = pos[0] * tile, pos[1] * tile
        self.npc_action_trigger = False
        self.door_open_trigger = False
        self.door_prev_pos = self.y if self.flag == 'door_h' else self.x
        self.delete = False


        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 10)) for i in range(0, 360, 10)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    @property
    def is_on_fire(self):
        if center_ray - self.side // 2 < self.current_ray < center_ray + self.side // 2 and self.blocked:
            return self.distance_to_sprite, self.proj_height
        return float('inf'), None

    @property
    def pos(self):
        return self.x - self.side // 2, self.y - self.side // 2

    def object_locate(self, player):
        

        dx, dy = self.x - player.x, self.y - player.y
        self.distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += double_pi

        delta_rays = int(gamma / delta_angle)
        self.current_ray = center_ray + delta_rays
        if self.flag not in {'door_h', 'door_v'}:
            self.distance_to_sprite *= math.cos(half_FOV - self.current_ray * delta_angle)

        fake_ray = self.current_ray + fake_rays
        if 0 <= fake_ray <= fake_rays_range and self.distance_to_sprite > 30:
            self.proj_height = min(int(proj_coeff / self.distance_to_sprite), double_height if self.flag not in {'door_h', 'door_v'} else height)
            sprite_width = int(self.proj_height * self.scale[0])
            sprite_height = int(self.proj_height * self.scale[1])
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_height // 2
            shift = half_sprite_width * self.shift

            # logic for doors, npc, decor
            if self.flag in {'door_h', 'door_v'}:
                if self.door_open_trigger:
                    self.open_door()
                self.object = self.visible_sprite()
                sprite_object = self.sprite_animation()
            else:
                if self.is_dead and self.is_dead != 'immortal':
                    sprite_object = self.dead_animation()
                    shift = half_sprite_height * self.dead_shift
                elif self.npc_action_trigger:
                    sprite_object = self.npc_in_action()
                else:
                    self.object = self.visible_sprite()
                    sprite_object = self.sprite_animation()
            

            # sprite scale and pos
            sprite_pos = (self.current_ray * scale - half_sprite_width, half_height - half_sprite_width + shift)
            sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_height))
            return (self.distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)


    def sprite_animation(self):
        if self.animation and self.distance_to_sprite < self.animation_dist:
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
                self.theta += double_pi
            self.theta = 360 - int(math.degrees(self.theta))

            for angles in self.sprite_angles:
                if self.theta in angles:
                    return self.sprite_positions[angles]
        return self.object

    def dead_animation(self):
        if len(self.death_animation):
            if self.dead_animation_count < self.animation_speed:
                self.dead_sprite = self.death_animation[0]
                self.dead_animation_count += 1
            else:
                self.dead_sprite = self.death_animation.popleft()
                self.dead_animation_count = 0
        return self.dead_sprite


    def npc_in_action(self):
        sprite_object = self.obj_action[0]
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.obj_action.rotate()
            self.animation_count = 0
        return sprite_object

    def open_door(self):
        if self.flag == 'door_h':
            self.y -= 3
            if abs(self.y - self.door_prev_pos) > tile:
                self.delete = True
        elif self.flag == 'door_v':
            self.x -= 3
            if abs(self.x - self.door_prev_pos) > tile:
                self.delete = True
