import os
from typing import Dict, List, Tuple, Set, Union

from tqdm import tqdm

from deduce_uces.extenders.extender import Extender
from deduce_uces.types import MinimalUCE

import mappy as mp

from deduce_uces.utils import make_id


class MinimapExtender(Extender):
    def __init__(
        self,
        uce_sequences: Dict[str, str],
        uces_by_genome: Dict[str, List[MinimalUCE]],
        fasta_files: Dict[str, str],
        min_similarity: int,
        min_length: int,
    ):
        super().__init__(uce_sequences, uces_by_genome, min_similarity, min_length)

        self.all_genomes = set(uces_by_genome.keys())

        self.aligners = {}

        for genome in uces_by_genome.keys():
            if not os.path.exists(fasta_files[genome]):
                raise FileNotFoundError(fasta_files[genome])

            self.aligners[genome] = mp.Aligner(fasta_files[genome], preset="map-ont")

    def extend(self) -> Dict[str, List[MinimalUCE]]:
        # If uce was not found in a Genome using kmer search search genome
        # to see if there is a match with min-similarity
        uces_by_id = {}

        for genome, uce_list in self.uces_by_genome.items():
            for uce in uce_list:
                if uce.id in uces_by_id:
                    uces_by_id[uce.id].append((genome, uce))
                else:
                    uces_by_id[uce.id] = [(genome, uce)]

        all_ids = set(uces_by_id.keys())
        gen_id = make_id(len(all_ids), start_from=int(max(all_ids).replace("uce", "")))

        for uce_id in tqdm(all_ids):

            if len(uces_by_id[uce_id]) < len(self.uces_by_genome):
                # Find genomes where UCE wasn't found
                unchecked_genomes = self.get_missing_genomes(uce_id, uces_by_id)

                # search
                for unchecked_genome in unchecked_genomes:
                    instance = self.check_for_occurrence(
                        uce_id, self.aligners[unchecked_genome], gen_id
                    )

                    if instance is not None:
                        self.uces_by_genome[unchecked_genome].append(instance)

        return self.uces_by_genome

    def get_missing_genomes(
        self, uce_id: str, uces_by_id: Dict[str, List[Tuple[str, MinimalUCE]]]
    ) -> Set[str]:
        genomes_present = set(u[0] for u in uces_by_id[uce_id])
        return self.all_genomes.difference(genomes_present)

    def check_for_occurrence(
        self, uce_id: str, aligner: mp.Aligner, gen_id
    ) -> Union[MinimalUCE, None]:
        for alignment in aligner.map(self.uce_sequences[uce_id]):
            uce_length = int(alignment.blen)
            mis_matches = float(alignment.NM)
            matches = float(uce_length - mis_matches)

            percent_identity = (matches / uce_length) * 100.0

            if (
                percent_identity < self.min_similarity or uce_length < self.min_length
            ):  # if UCE definition parameters aren't met
                return None

            return MinimalUCE(
                gen_id(),
                alignment.r_st,
                alignment.r_st + uce_length - 1,
                percent_identity=percent_identity,
            )

        return None
