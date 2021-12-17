import math

# Настройки игры
width = 1200
height = 800
half_width = width / 2
half_height = height / 2
penta_height = 5 * height
double_height = 2 * height
FPS = 60
tile = 100


# Настройки Ray casting
FOV = math.pi / 3
half_FOV = FOV / 2
num_rays = 600
delta_angle = FOV / num_rays
dist = num_rays / (2 * math.tan(half_FOV))
proj_coeff = 1.5 * dist * tile
scale = width // num_rays

# Настройки спрайтов
double_pi = 2 * math.pi
center_ray = num_rays // 2 - 1
fake_rays = 100
fake_rays_range = num_rays - 1 + 2 * fake_rays

# Настройки текстур
texture_width = 1000
texture_height = 1000
half_texture_height = texture_height // 2
texture_scale = texture_width // tile

# Настройки игрока
player_pos = (150, 150)
player_angle = 0
# player_speed = 2

# Настройки мини карты
minimap_scale = 5
minimap_res = (width // minimap_scale, height // minimap_scale)
map_scale = 2 * minimap_scale
map_tile = tile / map_scale
map_pos = (width - width // minimap_scale, 0)

# Цвета
white = (255,255,255)
gray = (100,100,100)
black = (0,0,0)
red = (220,0,0)
green = (0,220,0)
blue = (0,0,220)
darkgray = (90,90,90)
purple = (120,0,120)
yellow = (230,200,0)