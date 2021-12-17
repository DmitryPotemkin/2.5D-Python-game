import pygame
from settings import *
import map_generator
from numba import njit

@njit(fastmath=True, cache=True)
def mapping(a, b):
    return (a // tile) * tile, (b // tile) * tile

@njit(fastmath=True, cache=True)
def ray_casting(player_pos, player_angle, world_map):
    casted_walls = []
    ox, oy = player_pos
    texture_v, texture_h = 1, 1
    xm, ym, = mapping(ox, oy)
    cur_angle = player_angle - half_FOV
    for ray in range(num_rays):
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
        for i in range(0, map_generator.world_width * 2, tile):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * tile

        # horisontals
        if sin_a >= 0:
            y = ym + tile
            dy = 1
        else:
            y = ym
            dy = -1
        for i in range(0, map_generator.world_height * 2, tile):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * tile

        # projection
        if depth_v < depth_h:
            depth = depth_v
            offset = yv
            texture = texture_v
        else:
            depth = depth_h
            offset = xh
            texture = texture_h
        offset = int(offset) % tile
        depth *= math.cos(player_angle - cur_angle)
        depth = max(depth, 0.00001)
        proj_height = int(proj_coeff / depth)

        casted_walls.append((depth, offset, proj_height, texture))
        cur_angle += delta_angle
    return casted_walls

def ray_casting_walls(player, textures):
    casted_walls = ray_casting(player.pos, player.angle, map_generator.world_map)
    wall_shot = casted_walls[center_ray][0], casted_walls[center_ray][2]
    walls = []
    for ray, casted_values in enumerate(casted_walls):
        depth, offset, proj_height, texture = casted_values
        if proj_height > height:
            coeff = proj_height / height
            texture_h = texture_height / coeff
            wall_column = textures[texture].subsurface(offset * texture_scale,
                                                       half_texture_height - texture_h // 2,
                                                       texture_scale, texture_h)
            wall_column = pygame.transform.scale(wall_column, (scale, height))
            wall_pos = (ray * scale, 0)
        else:
            wall_column = textures[texture].subsurface(offset * texture_scale, 0, texture_scale, texture_height)
            wall_column = pygame.transform.scale(wall_column, (scale, proj_height))
            wall_pos = (ray * scale, half_height - proj_height // 2)
        walls.append((depth, wall_column, wall_pos))
    return walls, wall_shot
