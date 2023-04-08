from ursina import BoxCollider, Entity, Ursina, Vec3, color, held_keys, invoke, random
from ursina.prefabs.ursfx import ursfx

from custom_first_person_controller import CustomFirstPersonController

app = Ursina()
player = CustomFirstPersonController(model="cube", z=-10, color=color.orange, origin_y=-0.5, speed=16)
player.collider = BoxCollider(player, Vec3(0, 1, 0), Vec3(1, 2, 1))
ground = Entity(model="plane", collider="box", scale=128, texture="grass", texture_scale=(4, 4))


def grapple():
    if not player.grapple:
        player.grapple = True

        ursfx(
            [(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)],
            volume=0.5,
            wave="noise",
            pitch=random.uniform(-13, -12),
            pitch_change=-12,
            speed=1.0,
        )

        player.grapple_direction = Vec3(player.camera_pivot.forward)
        invoke(disable_grapple, player, delay=1)


def disable_grapple(player_obj: CustomFirstPersonController):
    player_obj.grapple = False
    player_obj.grapple_direction = None


def update():
    if held_keys["left mouse"]:
        grapple()


app.run()
