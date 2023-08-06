from typing import Dict, List

from deduce_uces.types import MinimalUCE


class Extender:
    def __init__(
        self,
        uce_sequences: Dict[str, str],
        uces_by_genome: Dict[str, List[MinimalUCE]],
        min_similarity: int,
        min_length: int,
    ):
        self.uce_sequences = uce_sequences
        self.uces_by_genome = uces_by_genome
        self.min_similarity = min_similarity
        self.min_length = min_length

    def extend(self) -> Dict[str, List[MinimalUCE]]:
        pass
