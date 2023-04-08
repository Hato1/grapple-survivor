"""Module for managing hostile creatures."""
from ursina import Entity, time

import custom_first_person_controller

enemies = []

# Todo: Make these Enums?
model_types = [
    "quad",
    "wireframe_cube",
    "plane",
    "circle",
    "diamond",
    "wireframe_quad",
    "sphere",
    "cube",
    "icosphere",
    "cube_uv_top",
    "arrow",
    "sky_dome",
]
texture_types = [
    "noise",
    "grass",
    "vignette",
    "arrow_right",
    "test_tileset",
    "tilemap_test_level",
    "shore",
    "file_icon",
    "sky_sunset",
    "radial_gradient",
    "circle",
    "perlin_noise",
    "brick",
    "grass_tintable",
    "circle_outlined",
    "ursina_logo",
    "arrow_down",
    "cog",
    "vertical_gradient",
    "white_cube",
    "horizontal_gradient",
    "folder",
    "rainbow",
    "heightmap_1",
    "sky_default",
]


class Enemy(Entity):
    def __init__(self, **kwargs):
        if "model" not in kwargs:
            kwargs["model"] = "sphere"
        if "texture" not in kwargs:
            kwargs["texture"] = "rainbow"
        if "x" not in kwargs:
            kwargs["x"] = 0
        if "y" not in kwargs:
            kwargs["y"] = 2
        if "z" not in kwargs:
            kwargs["z"] = 1
        super().__init__(**kwargs)

    @classmethod
    def new_enemy(cls):
        enemies.append(cls())
        return enemies[-1]


class FollowingFelicia(Enemy):
    def __init__(self):
        super().__init__()

    def update(self):
        self.look_at(custom_first_person_controller.player)
        move_amount = self.direction * time.dt * self.speed
        self.position += move_amount
