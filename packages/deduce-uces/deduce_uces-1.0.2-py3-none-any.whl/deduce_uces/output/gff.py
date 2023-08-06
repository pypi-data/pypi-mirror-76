from operator import attrgetter
from typing import List

from deduce_uces.types import MinimalUCE


def output_gff(uces: List[MinimalUCE], reference_name: str) -> str:
    rows = []

    for i, uce in enumerate(sorted(uces, key=attrgetter("start"))):
        start = uce.start + 1  # GFF is 1-indexed
        end = uce.end

        tags = {"ID": uce.id}

        # conserved_region seems to be the closest definition in the SOFA sequence ontology
        # http://www.sequenceontology.org/so_wiki/index.php/Category:SO:0000330_!_conserved_region
        rows.append(
            f"{reference_name}\t.\tconserved_region\t{start}\t{end}\t{uce.percent_identity}\t+\t.\t{format_tags(tags)}"
        )

    return "##gff-version 3\n" + "\n".join(rows) + "\n"


def format_tags(tags):
    return ";".join(f"{k}={v}" for k, v in tags.items())
