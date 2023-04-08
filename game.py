from ursina import BoxCollider, Entity, Ursina, Vec3, color, held_keys, invoke, random

from Bullet import Bullet
from custom_first_person_controller import CustomFirstPersonController

app = Ursina()
player = CustomFirstPersonController(model="cube", z=-10, color=color.orange, origin_y=-0.5, speed=16)
player.collider = BoxCollider(player, Vec3(0, 1, 0), Vec3(1, 2, 1))
ground = Entity(model="plane", collider="box", scale=128, texture="grass", texture_scale=(4, 4))
bullet = Bullet(model="cube", collider="box", scale=1, texture="brick", texture_scale=(4, 4))

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


def grapple():
    """Activates the grapple mode on the player"""
    if not player.grapple:
        player.grapple = True
        from ursina.prefabs.ursfx import ursfx

        ursfx(
            [(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)],
            volume=0.5,
            wave="noise",
            pitch=random.uniform(-13, -12),
            pitch_change=-12,
            speed=1.0,
        )
        player.jumping = False
        player.speed = 40
        player.air_time = 0
        player.grapple_direction = Vec3(player.camera_pivot.forward)
        invoke(disable_grapple, player, delay=1)


def disable_grapple(playerobj: CustomFirstPersonController):
    """Disables the grapple mode on the player"""
    playerobj.grapple = False
    playerobj.grapple_direction = None
    playerobj.speed = 12


def shoot():
    bullet.shoot(player.camera_pivot.forward)


def update():
    if held_keys["left mouse"]:
        grapple()
    if held_keys["right mouse"]:
        shoot()


app.run()
