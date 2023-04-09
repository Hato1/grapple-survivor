from ursina import Entity, Ursina, color, random

import enemy
from custom_first_person_controller import create_player

app = Ursina()

ground = Entity(model="plane", collider="box", scale=128, texture="grass", texture_scale=(4, 4))
create_player()
# Creates the blocks around the map
for _i in range(16):
    Entity(
        model="cube",
        origin_y=-0.5,
        scale=2,
        texture="brick",
        texture_scale=(1, 4),
        x=random.uniform(-16, 16),
        z=random.uniform(-16, 16) + 8,
        collider="box",
        scale_y=random.uniform(2, 90),
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
