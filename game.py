from ursina import Entity, Ursina, color, random

from custom_first_person_controller import create_player
from enemy import Enemy

app = Ursina()

ground = Entity(model="plane", collider="box", scale=128, texture="grass", texture_scale=(4, 4))
create_player()
Enemy.new_enemy()
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
    pass


app.run()
