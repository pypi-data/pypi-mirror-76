import os
import subprocess
import tempfile
from contextlib import contextmanager
from os.path import getsize
from pathlib import Path
from typing import List

from tqdm import tqdm

from deduce_uces.Logger import (
    LOG_LEVEL_INFO,
    LOG_LEVEL_DEBUG,
    LOG_LEVEL_WARNING,
    LOG_LEVEL_ERROR,
)
from deduce_uces.utils import make_id


def dump_directory(dir_path):
    @contextmanager
    def dump_directory_context():
        if not os.path.exists(dir_path):
            raise IOError("Output directory does not exist")

        try:
            yield dir_path
        finally:
            pass

    return dump_directory_context


def hash_kmers(
    genome_filename: str,
    hash_size: str,
    kmer_size: int,
    threads: int,
    canonical: bool,
    working_dir: str,
):
    output_filename = os.path.join(working_dir, Path(genome_filename).stem + ".jf")

    jellyfish_options = [
        "--output",
        output_filename,
        "--threads",
        str(threads),
        "--mer-len",
        str(kmer_size),
        "--size",
        hash_size,
        # Since we're only interested in kmers with a count of 1, we can restrict the hash counter size.
        #
        # counter_len controls the in-memory counter size. If the counter fills, it will remain at the max.
        # value - e.g. for an 8-bit counter the maximum kmer count returned is 256. We want to know whether
        # a kmer is present 0, 1, or more times, therefore we only need two bits.
        #
        # out_counter_len controls the disk counter size. We only need one byte to represent a count of 0, 1,
        # or more.
        "--counter-len",
        "2",
        "--out-counter-len",
        "1",
        # Only output to disk those kmers with a count of 1
        "--lower-count",
        "1",
        "--upper-count",
        "1",
    ]

    if canonical:
        jellyfish_options.extend(["--canonical"])

    hash_command = (
        ["jellyfish", "count"] + jellyfish_options + [os.path.abspath(genome_filename)]
    )

    subprocess.run(hash_command, cwd=working_dir, capture_output=True, check=True)


def merge_hashes(
    genome_filenames: List[str], min_genomes: int, working_dir: str
) -> str:
    output_filename = os.path.join(working_dir, "deduce-merged.jf")
    input_filenames = [
        os.path.join(working_dir, Path(genome_filename).stem + ".jf")
        for genome_filename in genome_filenames
    ]

    jellyfish_options = [
        "--output",
        output_filename,
        # Merging the hashes, which each only contain a count of 1 or 0 for each kmer, will create a hash
        # with the sum of these counts. We then restrict the output to those kmers with a count >= min_genomes
        # and <= n(genomes).
        "--lower-count",
        str(min_genomes),
        "--upper-count",
        str(len(genome_filenames)),
    ]

    merge_command = ["jellyfish", "merge"] + jellyfish_options + input_filenames

    subprocess.run(merge_command, cwd=working_dir, capture_output=True, check=True)

    return output_filename


def dump_hash(hash_filename: str, output_filename: str):
    dump_command = ["jellyfish", "dump", hash_filename]

    completed_process = subprocess.run(dump_command, capture_output=True, check=True)

    uce_fasta_lines = completed_process.stdout.decode("utf-8").split()

    gen_id = make_id(len(uce_fasta_lines) // 2)
    fasta_lines_with_ids = [
        ">" + gen_id() + "\n" if line.startswith(">") else line + "\n"
        for line in uce_fasta_lines
    ]

    with open(output_filename, "w") as f:
        f.writelines(fasta_lines_with_ids)


def command_find(args, logger):
    if len(args.genomes) != len(set(args.genomes)):
        args.genomes = set(args.genomes)
        logger.log(
            f"One or more genomes has been supplied more than once, any duplicates have been removed",
            LOG_LEVEL_WARNING,
        )

    if len(args.genomes) < 2:
        logger.log(
            f"You must provide more than one genome", LOG_LEVEL_ERROR,
        )

    min_genomes = len(args.genomes) if args.min_genomes is None else args.min_genomes

    if min_genomes > len(args.genomes):
        logger.log(
            f"Value for min_genome is greater than the number of genomes supplied. min_genomes was set to {len(args.genomes)}",
            LOG_LEVEL_WARNING,
        )
        min_genomes = len(args.genomes)

    logger.log(f"Using Jellyfish hash of size: {args.hash_size}", LOG_LEVEL_INFO)

    directory_context = (
        dump_directory(args.dump_hashes or ".")
        if args.dump_hashes or args.use_dumped
        else tempfile.TemporaryDirectory
    )

    with directory_context() as working_dir:
        logger.log(f"Working directory: {working_dir}", LOG_LEVEL_DEBUG)

        if not args.use_dumped:
            logger.log("Hashing provided genomes...", LOG_LEVEL_INFO)
            for genome in tqdm(args.genomes):
                hash_kmers(
                    genome,
                    hash_size=args.hash_size,
                    kmer_size=args.min_length,
                    threads=args.threads,
                    canonical=args.canonical,
                    working_dir=working_dir,
                )

        logger.log("Merging hashes...", LOG_LEVEL_INFO)
        merged_hash = merge_hashes(
            args.genomes, min_genomes=min_genomes, working_dir=working_dir,
        )

        logger.log("Extracting UCEs...", LOG_LEVEL_INFO)
        dump_hash(merged_hash, os.path.abspath(args.output))
