import os
from pathlib import Path

from mappy import fastx_read
from tqdm import tqdm

from deduce_uces.Logger import LOG_LEVEL_INFO, LOG_LEVEL_ERROR, LOG_LEVEL_WARNING
from deduce_uces.extenders.minimap_extender import MinimapExtender
from deduce_uces.io import read_gff3
from deduce_uces.output.output import OUTPUT_FORMATS


def command_extend(args, logger):
    uce_sequences = {}

    for seq in fastx_read(os.path.abspath(args.uces), read_comment=False):
        uce_sequences[seq[0]] = seq[1]

    logger.log(f"Read {len(uce_sequences)} UCEs", LOG_LEVEL_INFO)

    logger.log(f"Reading aligned UCEs...", LOG_LEVEL_INFO)

    if args.alignments and len(args.alignments) != len(set(args.alignments)):
        logger.log(
            f"One or more alignments was supplied more than once, all duplicates were removed",
            LOG_LEVEL_WARNING,
        )
        args.alignments = set(args.alignments)

    if args.genomes and len(args.genomes) != len(set(args.genomes)):
        logger.log(
            f"One or more genomes was supplied more than once, all duplicates were removed",
            LOG_LEVEL_WARNING,
        )
        args.genomes = set(args.genomes)

    if len(args.alignments or []) != len(args.genomes or []):
        logger.log("Number of alignments and genomes do not match", LOG_LEVEL_ERROR)

    uces_by_genome = {}
    fasta_files = {}
    for i, alignment_filename in enumerate(tqdm(args.alignments)):
        uces_by_genome[alignment_filename] = read_gff3(
            os.path.abspath(alignment_filename)
        )
        fasta_files[alignment_filename] = os.path.abspath(args.genomes[i])

    logger.log(f"Building indices for genomes...", LOG_LEVEL_INFO)

    extender = MinimapExtender(
        uce_sequences, uces_by_genome, fasta_files, args.min_similarity, args.min_length
    )

    logger.log(f"Built indices", LOG_LEVEL_INFO)

    logger.log(f"Extending...", LOG_LEVEL_INFO)

    extended_uces = extender.extend()

    logger.log(f"Saving extended UCEs...", LOG_LEVEL_INFO)

    for alignment_filename in tqdm(args.alignments):
        with open(os.path.abspath(alignment_filename) + ".extended", "w") as output_f:
            output_f.write(
                OUTPUT_FORMATS[args.output_format](
                    extended_uces[alignment_filename], Path(alignment_filename).stem,
                )
            )
