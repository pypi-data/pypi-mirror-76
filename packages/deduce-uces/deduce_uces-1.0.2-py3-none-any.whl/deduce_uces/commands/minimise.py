import os
from pathlib import Path
from tqdm import tqdm
from deduce_uces.io import read_gff3
from deduce_uces.mergers.graph_merger import GraphMerger
from deduce_uces.output.output import OUTPUT_FORMATS

from deduce_uces.Logger import LOG_LEVEL_INFO, LOG_LEVEL_WARNING, LOG_LEVEL_ERROR


def command_minimise(args, logger):
    min_genomes = args.min_genomes or len(args.alignments)

    if min_genomes < len(args.alignments):
        logger.log(
            f"Minimise currently supports min_genomes = n_genomes. Other values of min_genomes will be supported soon!",
            LOG_LEVEL_ERROR,
        )

    logger.log(f"Reading aligned UCEs...", LOG_LEVEL_INFO)

    uces_by_genome = {}

    if len(args.alignments) != len(set(args.alignments)):
        logger.log(
            f"One or more alignment files were supplied more than once, all duplicates have been removed.",
            LOG_LEVEL_WARNING,
        )
        args.alignments = set(args.alignments)

    for alignment_filename in tqdm(args.alignments):
        uces_by_genome[alignment_filename] = read_gff3(alignment_filename)

    merged_uces_by_genome = GraphMerger().merge(uces_by_genome, min_genomes)

    logger.log(f"Saving minimised UCEs...", LOG_LEVEL_INFO)

    for alignment_filename in tqdm(args.alignments):
        with open(os.path.abspath(alignment_filename) + ".min", "w") as output_f:
            output_f.write(
                OUTPUT_FORMATS[args.output_format](
                    merged_uces_by_genome[alignment_filename],
                    Path(alignment_filename).stem,
                )
            )
