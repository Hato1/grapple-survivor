from ursina import Entity, Ursina, color, random

import enemy
from custom_first_person_controller import create_player

app = Ursina()

ground = Entity(model="plane", collider="box", scale=128, texture="brick", texture_scale=(4, 4))
roof = Entity(model="plane", collider="box", scale=128, texture="brick", texture_scale=(4, 4), y=128)
wall = Entity(model="plane", collider="box", scale=128, texture="brick", texture_scale=(4, 4), x=64, y=64)
wall2 = Entity(model="plane", collider="box", scale=128, texture="brick", texture_scale=(4, 4), y=64, z=64)
wall3 = Entity(model="plane", collider="box", scale=128, texture="brick", texture_scale=(4, 4), y=64, z=-64)
wall4 = Entity(model="plane", collider="box", scale=128, texture="brick", texture_scale=(4, 4), x=-64, y=64)

wall.rotation_z = 270
wall2.rotation_x = 270
wall3.rotation_x = 90
wall4.rotation_z = 90

roof.rotation_x = 180
create_player()
# Creates the blocks around the map
for _i in range(16):
    Entity(
        model="cube",
        origin_y=-0.5,
        scale=2,
        texture="brick",
        texture_scale=(1, 4),
        x=random.uniform(-26, 26),
        z=random.uniform(-26, 26) + 8,
        collider="box",
        scale_x=random.uniform(2, 10),
        scale_y=random.uniform(2, 90),
        scale_z=random.uniform(2, 10),
        color=color.hsv(0, 0, random.uniform(0.9, 1)),
    )

for _i in range(8):
    Entity(
        model="cube",
        origin_y=-0.5,
        scale=8,
        texture="brick",
        texture_scale=(1, 4),
        x=random.choice((-64, 64)),
        y=random.uniform(10, 128),
        z=random.choice((-64, 64)) + 8,
        collider="box",
        scale_x=random.uniform(50, 128),
        scale_z=random.uniform(50, 128),
        color=color.hsv(0, 0, random.uniform(0.9, 1)),
    )


def update():
    if len(enemy.enemies) < 10:
        if not enemy.enemies or enemy.enemies[-1].lifetime > 5:
            enemy.FollowingFelicia.new_enemy()


def input(key):
    if key == "q":
        quit()


app.run()
