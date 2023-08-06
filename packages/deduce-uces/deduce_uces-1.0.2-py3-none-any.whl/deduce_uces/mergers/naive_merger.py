from itertools import permutations
from typing import Dict, List

from deduce_uces.mergers.merger import Merger
from deduce_uces.types import MinimalUCE

from deduce_uces.utils import find, make_id

# Returns true if two UCEs overlap in all genomes
def can_merge(
    uces_by_genome: Dict[str, List[MinimalUCE]], first_uce: str, second_uce: str
) -> bool:
    for genome, uces in uces_by_genome.items():
        instance_of_first = find(uces, lambda x: x.id == first_uce)
        instance_of_second = find(uces, lambda x: x.id == second_uce)

        if not (
            instance_of_first
            and instance_of_second
            and instance_of_first.start
            < instance_of_second.start
            < instance_of_first.end
        ):
            return False

    return True


def merge(
    uces_by_genome: Dict[str, List[MinimalUCE]],
    first_uce: str,
    second_uce: str,
    new_id: str,
) -> Dict[str, List[MinimalUCE]]:
    for genome, uces in uces_by_genome.items():
        from_in_genome = find(uces_by_genome[genome], lambda u: u.id == first_uce)
        to_in_genome = find(uces_by_genome[genome], lambda u: u.id == second_uce)

        merged_uce = MinimalUCE(
            new_id,
            min(to_in_genome.start, from_in_genome.start),
            max(from_in_genome.end, to_in_genome.end),
        )

        uces_by_genome[genome] = [
            uce
            for uce in uces_by_genome[genome]
            if uce.id not in [from_in_genome.id, to_in_genome.id]
        ]

        uces_by_genome[genome].append(merged_uce)

    return uces_by_genome


class NaiveMerger(Merger):
    def merge(
        self, uces_by_genome: Dict[str, List[MinimalUCE]], min_genomes: int
    ) -> Dict[str, List[MinimalUCE]]:
        # Start generating new UCE ids from the maximum already used
        all_ids = set(u.id for genome in uces_by_genome.values() for u in genome)
        gen_id = make_id(len(all_ids), start_from=int(max(all_ids).replace("uce", "")))

        # Repeatedly picks overlapping UCEs and merges them
        # Once no more UCEs overlap, return
        found_merge = True
        while found_merge:
            found_merge = False
            all_ids = set(u.id for genome in uces_by_genome.values() for u in genome)

            for p in permutations(all_ids, 2):
                if can_merge(uces_by_genome, p[0], p[1]):
                    uces_by_genome = merge(uces_by_genome, p[0], p[1], gen_id())
                    found_merge = True
                    break

        return uces_by_genome
