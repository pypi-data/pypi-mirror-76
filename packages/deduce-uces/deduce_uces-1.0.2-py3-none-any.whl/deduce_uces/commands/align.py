import os
from pathlib import Path

from mappy import fastx_read
from tqdm import tqdm

from deduce_uces.Logger import LOG_LEVEL_INFO, LOG_LEVEL_WARNING
from deduce_uces.matchers.bowtie_matcher import BowtieMatcher
from deduce_uces.matchers.minimap_matcher import MinimapMatcher
from deduce_uces.matchers.naive_matcher import NaiveMatcher
from deduce_uces.output.output import OUTPUT_FORMATS
from deduce_uces.types import MinimalUCE


def command_align(args, logger):
    uces = []
    for seq in fastx_read(os.path.abspath(args.uces), read_comment=False):
        uces.append((seq[0], seq[1]))

    if len(args.genomes) != len(set(args.genomes)):
        logger.log(
            f"One or more genomes have been supplied more than once, all duplicates have been removed",
            LOG_LEVEL_WARNING,
        )
        args.genomes = set(args.genomes)

    logger.log(f"Read {len(uces)} UCEs", LOG_LEVEL_INFO)

    logger.log(
        f"Aligning UCEs with genomes using method {args.method}...", LOG_LEVEL_INFO
    )

    for i, genome_filename in enumerate(tqdm(args.genomes)):
        genome_name = Path(genome_filename).stem

        if args.method == "bowtie":
            matcher = BowtieMatcher(
                genome_path=os.path.abspath(genome_filename),
                index_path=os.path.abspath(args.indices[i])
                if len(args.indices or []) >= i + 1
                else None,
                threads=args.threads,
            )
        elif args.method == "minimap":
            matcher = MinimapMatcher(
                genome_path=os.path.abspath(genome_filename), threads=args.threads,
            )

        else:
            matcher = NaiveMatcher(genome_path=os.path.abspath(genome_filename))

        matcher.match(os.path.abspath(args.uces), threads=args.threads)

        aligned_uces = []

        for uce in uces:
            for match in matcher[uce[1]]:
                aligned_uces.append(
                    MinimalUCE(uce[0], start=match, end=match + len(uce[1]) - 1,)
                )

        with open(genome_name + "." + args.output_format, "w") as output_f:
            output_f.write(
                OUTPUT_FORMATS[args.output_format](aligned_uces, genome_name)
            )

        matcher.cleanup()
