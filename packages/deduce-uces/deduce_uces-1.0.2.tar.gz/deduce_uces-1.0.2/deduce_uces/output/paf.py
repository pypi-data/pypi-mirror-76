import csv
from io import StringIO
from typing import List

from deduce_uces.types import MinimalUCE


def output_paf(uces: List[MinimalUCE], _reference_name: str) -> str:
    output_file = StringIO()

    writer = csv.DictWriter(
        output_file,
        fieldnames=[
            "query name",
            "query len",
            "query start",
            "query end",
            "direction",
            "target name",
            "target length",
            "target start",
            "target end",
            "number matches",
            "alignment length",
            "quality",
        ],
        delimiter="\t",
    )

    writer.writerows(
        [
            {
                "query name": uce.id,
                "query len": uce.end - uce.start + 1,
                "query start": uce.start,
                "query end": uce.end,
                "direction": "+",
                "target name": _reference_name,
                "target length": "-",
                "target start": "-",
                "target end": "-",
                "number matches": (uce.end - uce.start + 1)
                * (uce.percent_identity / 100),
                "alignment length": "-",
                "quality": "-",
            }
            for uce in uces
        ]
    )

    return output_file.getvalue()
