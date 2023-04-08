from ursina import BoxCollider, Entity, Ursina, Vec3, color, held_keys, random

import Helpers
from Bullet import Bullet
from custom_first_person_controller import CustomFirstPersonController

app = Ursina()
player = CustomFirstPersonController(model="cube", z=-10, color=color.orange, origin_y=-0.5, speed=16)
player.collider = BoxCollider(player, Vec3(0, 1, 0), Vec3(1, 2, 1))
ground = Entity(model="plane", collider="box", scale=128, texture="grass", texture_scale=(4, 4))
bullet = Bullet(model="cube", collider="box", scale=1, texture="brick", texture_scale=(4, 4))
bullet.enabled = False
player.bullet = bullet
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
    if held_keys["left mouse"]:
        player.activate_grapple()
    if (held_keys["right mouse"] and bullet.state == Helpers.State.LOADED) or bullet.state == Helpers.State.FLYING:
        player.shoot()
    if held_keys["r"] and bullet.state == Helpers.State.ANCHORED:
        bullet.reload()


app.run()
