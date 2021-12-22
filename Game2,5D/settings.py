import math

# Настройки игры
screen_height = 800
screen_width = 1200
tile = 100
FPS = 60


# Настройки RayCasting
field_of_view = math.pi / 3
num_rays = 600
delta_angle = field_of_view / num_rays
dist = num_rays / (2 * math.tan(field_of_view / 2))
proj_coeff = 1.5 * dist * tile
scale = screen_width // num_rays

# Настройки спрайтов
center_ray = num_rays // 2 - 1
fake_rays = 100
fake_rays_range = num_rays - 1 + 2 * fake_rays

# Настройки текстур
texture_height = 1000
texture_width = 1000
texture_scale = texture_width // tile

# Настройки игрока
player_view_angle = 0
player_pos = (150, 150)

# Настройки мини карты
minimap_scale = 5
minimap_res = (screen_width // minimap_scale, screen_height // minimap_scale)
map_scale = 2 * minimap_scale
map_tile = tile / map_scale
map_pos = (screen_width - screen_width // minimap_scale, 0)

# Цвета
white_color = (255,255,255)
gray_color = (110,110,110)
black_color = (0,0,0)
red_color = (210,0,0)
green_color = (0,210,0)
yellow_color = (230,200,0)