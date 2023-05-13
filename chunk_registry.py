from ursina import Entity
from random import choices

from chunk import EmptyCorridor, SinglePillar


class ChunkRegistry:
    """
    Get chunks for corridor using a markov chain.

    The markov chain restricts what chunks can be connected to other chunks.
    It also allows weighting the frequency of chunks (RNG).

    TODO: move these to above class

    """

    # TODO: change some of these to getter notimplementederror
    size = 16
    kwargs = {"model": "plane", "collider": "box", "texture_scale": (4, 4), "scale": size, "texture": "brick"}

    def __init__(self):
        # Make a verbose, human readablish list of lists for the random elements, then normalize so sum=1
        # TODO: Use a numpy array here instead
        # Todo: move into stage
        self.markov_chain: list[list] = [[1]]
        # Normalise it for random.choices
        self.markov_chain = [[prob/sum(probs) for prob in probs] for probs in self.markov_chain]
        self.num_chunks: int = len(self.markov_chain[0])
        self.potential_chunks = [
            EmptyCorridor.gen_chunk,
        ]

    def roll_chunk_id(self, chunk_id) -> int:
        """takes the previous chunk id, returns a valid connecting chunk id

        valid states are determined with weights in self.markov_chain (will be stage.markov_chain)
        The chance of each valid state being picked is determined by the markov chain.
        """
        return choices(range(self.num_chunks), self.markov_chain[chunk_id])[0]

    def make_chunk(self, i, chunk_id) -> list[Entity]:
        # i is the chunks z position
        chunk_generator = self.potential_chunks[chunk_id]
        return chunk_generator(i, self.size, **self.kwargs)


class ChunkRegistryPillars(ChunkRegistry):
    """This level can place the pillar chunk"""
    def __init__(self):
        super().__init__()
        # Make a verbose, human readablish list of lists for the random elements, then normalize so sum=1
        self.potential_chunks = [
            EmptyCorridor.gen_chunk,
            SinglePillar.gen_chunk,
        ]
        self.markov_chain = [   # Use a numpy array here instead?
            [1,  7],
            [1, 0.4],
            ]
        # Normalise it for random.choices
        self.markov_chain = [[prob/sum(probs) for prob in probs] for probs in self.markov_chain]
        self.num_chunks = len(self.potential_chunks)
