import csv
from io import StringIO
from typing import List

from deduce_uces.types import MinimalUCE


def output_tsv(uces: List[MinimalUCE], _reference_name: str) -> str:
    output_file = StringIO()

    writer = csv.DictWriter(
        output_file, fieldnames=["start", "end", "% identity"], delimiter="\t"
    )

    writer.writeheader()

    writer.writerows(
        [
            {"start": uce.start, "end": uce.end, "% identity": uce.percent_identity}
            for uce in uces
        ]
    )

    return output_file.getvalue()
