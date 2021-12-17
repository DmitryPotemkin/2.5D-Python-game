from settings import *
import map_generator
from ray_casting import mapping
import math
import pygame
from numba import njit
import sys


njit(fastmath = True, cache = True)
def ray_casting_npc_player(npc_x, npc_y, blocked_doors, world_map, player_pos):
    ox, oy = player_pos
    xm, ym, = mapping(ox, oy)
    cur_angle = player_angle - half_FOV
    delta_x, delta_y = ox - npc_x, oy - npc_y
    cur_angle = math.atan2(delta_y, delta_x)
    cur_angle += math.pi

    sin_a = math.sin(cur_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = math.cos(cur_angle)
    cos_a = cos_a if cos_a else 0.000001

    # verticals
    if cos_a >= 0:
        x = xm + tile
        dx = 1
    else:
        x = xm
        dx = -1
    for i in range(0, int(abs(delta_x)) // tile):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = mapping(x + dx, yv)
        if tile_v in world_map or tile_v in blocked_doors:
            return False
        x += dx * tile

    # horisontals
    if sin_a >= 0:
        y = ym + tile
        dy = 1
    else:
        y = ym
        dy = -1
    for i in range(0, int(abs(delta_y)) // tile):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        if tile_h in world_map or tile_h in blocked_doors:
            return False
        y += dy * tile
    return True


class Interaction:
    def __init__(self, player, sprites, drawing):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing
        self.pain_sound = pygame.mixer.Sound('sound/MonsterPain.mp3')
        self.lives = 1
        self.score = 0
        self.add_score = 0
        self.factor = 0
        self.counter = 0
        self.last = pygame.time.get_ticks()
        self.cooldown = 3000
        self.lvl = 1


    def interaction_objects(self):
        if self.player.shot and self.drawing.shot_animation_trigger:
            for obj in sorted(self.sprites.list_of_objects, key=lambda obj: obj.distance_to_sprite):
                if obj.is_on_fire[1]:
                    if obj.is_dead != 'immortal' and not obj.is_dead:
                        if ray_casting_npc_player(obj.x, obj.y,
                                                  self.sprites.blocked_doors,
                                                  map_generator.world_map, self.player.pos):
                            if obj.flag == 'npc':
                                self.pain_sound.play()
                            obj.is_dead = True
                            obj.blocked = None

                            self.add_score += 100
                            self.factor += 1

                            self.drawing.shot_animation_trigger = False
                    if obj.flag in {'door_h', 'door_v'} and obj.distance_to_sprite < tile:
                        obj.door_open_trigger = True
                        obj.blocked = None
                    break

    def npc_action(self, pl_x, pl_y):
        for obj in self.sprites.list_of_objects:
            if obj.flag == 'npc' and not obj.is_dead:
                if ray_casting_npc_player(obj.x, obj.y, self.sprites.blocked_doors, map_generator.world_map, self.player.pos):
                    obj.npc_action_trigger = True
                    self.npc_move(obj, pl_x, pl_y)
                else:
                    obj.npc_action_trigger = False

    def npc_move(self, obj, pl_x, pl_y):
        if obj.distance_to_sprite > tile:
            dx = obj.x - self.player.pos[0]
            dy = obj.y - self.player.pos[1]
            if dx < -1:
                obj.x = obj.x + 1
            elif dx > 1:
                obj.x = obj.x - 1
            if dy < -1:
                obj.y = obj.y + 1
            elif dy > 1:
                obj.y = obj.y - 1
        if abs(pl_x - obj.x) < tile and abs(pl_y - obj.y) < tile:
            self.lives = 0

    def clear_world(self):
        deleted_objects = self.sprites.list_of_objects[:]
        [self.sprites.list_of_objects.remove(obj) for obj in deleted_objects if obj.delete]


    def play_music(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load('sound/1.mp3')
        pygame.mixer.music.play(10)

    def check_win(self):
        if not len([obj for obj in self.sprites.list_of_objects if obj.flag == 'npc' and not obj.is_dead]):
            self.score += self.add_score * self.factor
            pygame.time.delay(500)
            pygame.mixer.music.stop()
            pygame.mixer.music.load('sound/Victory.mp3')
            pygame.mixer.music.play()
            pygame.mouse.set_visible(True)
            while not len([obj for obj in self.sprites.list_of_objects if obj.flag == 'npc' and not obj.is_dead]):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                self.drawing.win(self.score, self.lvl)
            self.lvl += 1
            self.score = 0
            self.factor = 0
            self.add_score = 0


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


