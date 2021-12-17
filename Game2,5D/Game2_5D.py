import pygame
import math
from settings import *
from player import Player
from ray_casting import ray_casting_walls
from drawing import Drawing
from sprite_objects import *
from interaction import Interaction

# Инициализация pygame
pygame.init()
# Окно программы
screen = pygame.display.set_mode((width, height))
# Мини карта
screen_map = pygame.Surface(minimap_res)

clock = pygame.time.Clock()
sprites = Sprites()
player = Player(sprites)
drawing = Drawing(screen, screen_map, player, clock, sprites)
interaction = Interaction(player, sprites, drawing)

drawing.menu()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
interaction.play_music()

GameRunning = True
while GameRunning:
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        GameRunning = False

    pygame.display.set_caption(str(int(clock.get_fps())))

    player.movement()

    drawing.background(player.angle)
    walls, wall_shot = ray_casting_walls(player, drawing.textures)
    drawing.world(walls + [obj.object_locate(player)
                           for obj in sprites.list_of_objects])
    drawing.mini_map(player)
    drawing.player_weapon([wall_shot, sprites.sprite_shot])

    interaction.interaction_objects()
    interaction.npc_action(player.x, player.y)
    interaction.clear_world()
    interaction.check_win()
    interaction.check_status()

    # обновление содержимого окна на каждой итерации
    pygame.display.flip()
    clock.tick(FPS)
