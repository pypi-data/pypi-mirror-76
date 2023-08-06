import os
from typing import Generator

import mappy as mp


class MinimapMatcher:
    def __init__(self, genome_path: str, threads: int = 1):
        if not os.path.exists(genome_path):
            raise FileNotFoundError(genome_path)

        self.index = mp.Aligner(genome_path, preset="map-ont")
        self.matches = {}

    def match(self, uces_path: str, threads: int = 1):
        for seq in mp.fastx_read(os.path.abspath(uces_path), read_comment=False):
            uce_sequence = seq[1]

            self.matches[uce_sequence] = []
            for alignment in self.index.map(uce_sequence):
                alignment_len = int(alignment.blen)
                mismatches = float(alignment.NM)

                if alignment_len == len(uce_sequence) and mismatches == 0:
                    self.matches[uce_sequence].append(alignment.r_st)

    def __getitem__(self, sequence) -> Generator[int, None, None]:
        for position in self.matches.get(sequence, []):
            yield position

    def cleanup(self):
        pass
