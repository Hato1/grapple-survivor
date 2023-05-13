from ursina import Entity


class Chunk:
    state = 0
    @staticmethod
    def gen_chunk(i, size, **kwargs) -> dict[str, Entity]:
        raise NotImplementedError


class EmptyCorridor(Chunk):
    @staticmethod
    def gen_chunk(i, size, **kwargs):
        return {
            "ground": Entity(z=i * size, **kwargs),
            "left": Entity(x=-size / 2, y=size / 2, z=i * size, rotation_z=90, **kwargs),
            "ceil": Entity(y=size, z=i * size, rotation_z=180, **kwargs),
            "right": Entity(x=size / 2, y=size / 2, z=i * size, rotation_z=270, **kwargs),
        }


class SinglePillar(EmptyCorridor):
    """standard corridor with a sphere on the right wall at the end"""
    @classmethod
    def gen_chunk(cls, i, size, **kwargs):
        parent = super().gen_chunk(i, size, **kwargs)
        parent["pillar"] = Entity(model='sphere', x=size / 2, y=size / 2, z=i * size + size / 2)
        return parent
