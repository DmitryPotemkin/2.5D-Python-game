import pygame
from settings import *
import map_generator
from numba import njit

# Координаты верхнего левого угла квадрата в котором находится игрок
@njit(fastmath=True, cache=True)
def mapping(a, b):
    return (a // tile) * tile, (b // tile) * tile

@njit(fastmath=True, cache=True)
def ray_casting(player_pos, player_view_angle, world_map):
    casted_walls = []
    # Начальные координаты луча
    pos_x, pos_y = player_pos
    texture_vertical, texture_horisontal = 1, 1
    x_tile, y_tile, = mapping(pos_x, pos_y)
    # Текущий угол направления игрока
    current_angle = player_view_angle - field_of_view / 2
    # Синусы и косинусы каправлений лучей
    for i in range(num_rays):
        ray_sin = math.sin(current_angle)
        ray_sin = ray_sin if ray_sin else 0.000001
        ray_cos = math.cos(current_angle)
        ray_cos = ray_cos if ray_cos else 0.000001

        # пересечение с вертикалями
        if ray_cos >= 0:
            # Текущаа вертикаль
            x = x_tile + tile
            # Вспомогательная переменная для вычисления очередной вертикали
            next_x = 1
        else:
            x = x_tile
            next_x = -1
        # Проходим по всем вертикалям 
        for i in range(0, map_generator.map_width * 2, tile):
            # Расстояние до вертикали
            vertical_depth = (x - pos_x) / ray_cos
            # Координата y вертикали
            yv = pos_y + vertical_depth * ray_sin
            vertical_tile = mapping(x + next_x, yv)
            # Если пересечения со стеной не было, переходим к следующей вертикали
            if vertical_tile in world_map:
                # Номер текстуры
                texture_vertical = world_map[vertical_tile]
                break
            x += next_x * tile

        # Пересечение с горизонталями
        if ray_sin >= 0:
            y = y_tile + tile
            next_y = 1
        else:
            y = y_tile
            next_y = -1
        for i in range(0, map_generator.map_height * 2, tile):
            horisontal_depth = (y - pos_y) / ray_sin
            xh = pos_x + horisontal_depth * ray_cos
            horisontal_tile = mapping(xh, y + next_y)
            if horisontal_tile in world_map:
                texture_horisontal = world_map[horisontal_tile]
                break
            y += next_y * tile

        # Проекция
        # Выбор, какая из точек пересечений с вертикальной 
        # или горизонтальной прямой ближе к нам
        if vertical_depth < horisontal_depth:
            depth = vertical_depth
            # Смещение текстуры (для наложения)
            offset = yv
            texture = texture_vertical
        else:
            depth = horisontal_depth
            offset = xh
            texture = texture_horisontal

        offset = int(offset) % tile
        # Устранение эфекта "рыбьего глаза"
        depth *= math.cos(player_view_angle - current_angle)
        depth = max(depth, 0.0001)
        # Проекционная высота стены
        projection_height = int(proj_coeff / depth)

        casted_walls.append((depth, offset, projection_height, texture))
        current_angle += delta_angle

    return casted_walls

def ray_casting_walls(player, textures):
    casted_walls = ray_casting(player.position, player.player_view_angle, map_generator.world_map)
    wall_shot = casted_walls[center_ray][0], casted_walls[center_ray][2]
    walls = []
    for i, casted_values in enumerate(casted_walls):
        depth, offset, projection_height, texture = casted_values
        if projection_height > screen_height:
            coeff = projection_height / screen_height
            texture_h = texture_height / coeff
            # Полоска с наложеной текстурой из картинки
            wall_piece = textures[texture].subsurface(offset * texture_scale,
                                                       texture_height // 2 - texture_h // 2,
                                                       texture_scale, texture_h)
            wall_piece = pygame.transform.scale(wall_piece, (scale, screen_height))
            wall_position = (i * scale, 0)
        else:
            wall_piece = textures[texture].subsurface(offset * texture_scale, 0, texture_scale, texture_height)
            wall_piece = pygame.transform.scale(wall_piece, (scale, projection_height))
            wall_position = (i * scale, screen_height / 2 - projection_height // 2)
        walls.append((depth, wall_piece, wall_position))
    return walls, wall_shot
