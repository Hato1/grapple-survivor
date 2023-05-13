from __future__ import annotations

from chunk import Chunk

from ursina import Entity, Ursina
from chunk_registry import ChunkRegistryPillars
import custom_first_person_controller
import enemy
from custom_first_person_controller import create_player

app = Ursina()


class ChunkManager:
    """A section of the main tunnel.

    The tunnel has no splitting paths, so each chunk connects to at most two others, like a line.

     chunks: A list of all the chunks in order. Adjacent chunks in the list connect.

     Todo: Add left/right turns. Add up/down turns.
     Todo: Delete old chunks that the player can't return to.
     Note: It would be great if we could replace cls.chunks with a linked-list system. But then how do we tell where
     the player is to know when to generate more chunks?
    """
    chunk_registry = ChunkRegistryPillars()
    chunks: list[Chunk] = []

    def __init__(self):
        """Chunks only expand in the z direction"""
        # TODO: Have a chunk store its end position (rotation?) for next chunk to know where to put itself
        i = len(self.chunks)
        # NOW IN STAGES kwargs = {"model": "plane", "collider": "box", "texture_scale": (4, 4), "scale": self.size, "texture": "brick"}
        # State is used to track the kind of chunk to ensure valid connections
        last_state = self.chunks[-1].state
        self.state = self.chunk_registry.roll_chunk_id(last_state) if self.chunks else 0
        # TODO: make this not rely on i, and instead rely on pos: (x, y, z, xrot, yrot..)
        # Entities are the things to be rendered
        self.entities: list[Entity] = self.chunk_registry.make_chunk(i, self.state)
        self.chunks.append(self)

    @classmethod
    def get_chunk_index(cls, entity: Entity) -> int:
        """Get the index into cls.chunks where the entity stands."""
        return int((entity.z + cls.chunk_registry.size / 2) // cls.chunk_registry.size)

    @classmethod
    def new_chunk(cls):
        cls()


# Todo: This DOESN'T BELONG HERE
ChunkManager()
create_player()
enemy.Walleye()


def update():
    player_chunk = ChunkManager.get_chunk_index(custom_first_person_controller.player)
    if len(ChunkManager.chunks) - player_chunk < 3:
        ChunkManager.new_chunk()
    if len(enemy.enemies) < 10:
        if not enemy.enemies or enemy.enemies[-1].lifetime > 5:
            enemy.FollowingFelicia.new_enemy()


def input(key):
    if key == "q":
        quit()


app.run()
