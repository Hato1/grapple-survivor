from __future__ import annotations

from ursina import Entity, Ursina

import custom_first_person_controller
import enemy
from custom_first_person_controller import create_player

app = Ursina()


class Chunk:
    """A section of the main tunnel.

    The tunnel has no splitting paths, so each chunk connects to at most two others, like a line.

     chunks: A list of all the chunks in order. Adjacent chunks in the list connect.
     size: how large the chunks are. Currently, each chunk is cube shaped, so width=height=length.

     Todo: Add left/right turns. Add up/down turns.
     Todo: Delete old chunks that the player can't return to.
     Note: It would be great if we could replace cls.chunks with a linked-list system. But then how do we tell where
     the player is to know when to generate more chunks?
    """

    chunks: list[Chunk] = []
    size = 16

    def __init__(self):
        """Chunks only expand in the z direction"""
        i = len(self.chunks)
        kwargs = {"model": "plane", "collider": "box", "texture_scale": (4, 4), "scale": self.size, "texture": "brick"}
        self.ground = Entity(**kwargs, z=i * self.size)
        self.left = Entity(**kwargs, x=-self.size / 2, y=self.size / 2, z=i * self.size, rotation_z=90)
        self.ceil = Entity(**kwargs, y=self.size, z=i * self.size, rotation_z=180)
        self.right = Entity(**kwargs, x=self.size / 2, y=self.size / 2, z=i * self.size, rotation_z=270)
        self.chunks.append(self)

    @classmethod
    def get_chunk_index(cls, entity: Entity) -> int:
        """Get the index into cls.chunks where the entity stands."""
        return int((entity.z + cls.size / 2) // cls.size)


Chunk()
create_player()
enemy.Walleye()


def update():
    player_chunk = Chunk.get_chunk_index(custom_first_person_controller.player)
    if len(Chunk.chunks) - player_chunk < 3:
        Chunk()
    if len(enemy.enemies) < 10:
        if not enemy.enemies or enemy.enemies[-1].lifetime > 5:
            enemy.FollowingFelicia.new_enemy()


def input(key):
    if key == "q":
        quit()


app.run()
