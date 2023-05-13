"""Module for managing hostile creatures."""
from ursina import Entity, Sprite, destroy, distance, time

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
        self.creation_time = time.time()
        if "model" not in kwargs:
            kwargs["model"] = "sphere"
        if "texture" not in kwargs:
            kwargs["texture"] = "rainbow"
        if "x" not in kwargs:
            kwargs["x"] = 0
        if "y" not in kwargs:
            kwargs["y"] = 3
        if "z" not in kwargs:
            kwargs["z"] = 1
        super().__init__(**kwargs)

    @classmethod
    def new_enemy(cls):
        enemies.append(cls())
        return enemies[-1]

    @property
    def lifetime(self):
        """Get how long this entity has existed in seconds."""
        return time.time() - self.creation_time


class FollowingFelicia(Enemy):
    def __init__(self):
        super().__init__()
        self.speed = 1.0

    def update(self):
        """Move toward player and accelerate"""
        self.look_at(custom_first_person_controller.player)
        move_amount = self.forward * time.dt * self.speed
        self.position += move_amount
        self.speed = min(self.speed + 0.01, 5)

        if distance(self, custom_first_person_controller.player) < 5:
            custom_first_person_controller.player.health_bar.value -= 1
            destroy(self)


class Walleye(Sprite):
    """The Wall spans the entire corridor and moves through it."""

    def __init__(self, **kwargs):
        # Todo: set y to half height of the chunk. Hardcoding it here for now :(
        super().__init__(
            model="scardinius.obj",
            texture="fish.png",
            y=16 / 2,
            z=-10,
            rotation_y=180,
            **kwargs,
        )
        self.speed = 0.01

    def update(self):

        self.z += self.speed
