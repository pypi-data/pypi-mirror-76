import subprocess
import tempfile
from pathlib import Path
from typing import Generator


class BowtieMatcher:
    def __init__(
        self, genome_path: str = None, index_path: str = None, threads: int = 1
    ):
        if not genome_path and not index_path:
            raise ValueError(
                "To use the Bowtie matcher, you need a genome path or index path"
            )

        if index_path:
            self.tempdir = None
            self.working_dir = Path(index_path).parent.absolute()
            self.index = Path(index_path).stem

        else:
            self.tempdir = tempfile.TemporaryDirectory()
            self.working_dir = self.tempdir.name
            self.build_index(genome_path, threads)

        self.matches = {}

    def build_index(self, genome_path: str, threads: int):
        genome_name = Path(genome_path).stem
        command = ["bowtie2-build", "--threads", str(threads), genome_path, genome_name]

        subprocess.run(command, check=True, cwd=self.working_dir, capture_output=True)

        self.index = genome_name

    def match(self, uces_path: str, threads: int = 1):
        command = [
            "bowtie2",
            # Multithreaded search
            "--threads",
            str(threads),
            # Use own index
            "-x",
            self.index,
            # Very fast preset is OK for end-to-end exact matching
            "--very-fast",
            "--end-to-end",
            "--quiet",
            # FASTA format for reads
            "-f",
            "-U",
            uces_path,
        ]

        p = subprocess.run(
            command, check=True, cwd=self.working_dir, capture_output=True
        )

        sam_alignments = [
            line
            for line in p.stdout.decode("utf-8").strip().split("\n")
            if not line.startswith("@")
        ]

        for alignment in sam_alignments:
            sam_components = alignment.split("\t")

            sam_flag = int(sam_components[1])

            if sam_flag & 4 > 0:
                # 0x4 indicates no mapping found
                continue

            sequence = sam_components[9]
            position = int(sam_components[3]) - 1  # Bowtie reports 1-indexed position
            n_mismatches = int(sam_components[16].split(":")[-1])

            if n_mismatches > 0:
                # We're looking for an exact match
                continue

            if sequence in self.matches:
                self.matches[sequence].append(position)
            else:
                self.matches[sequence] = [position]

    def cleanup(self):
        if self.tempdir:
            self.tempdir.cleanup()

    def __getitem__(self, sequence) -> Generator[int, None, None]:
        for position in self.matches.get(sequence, []):
            yield position
