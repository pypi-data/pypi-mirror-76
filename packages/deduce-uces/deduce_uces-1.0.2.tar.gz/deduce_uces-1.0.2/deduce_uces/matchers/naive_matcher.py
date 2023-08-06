from typing import Generator, List


class NaiveMatcher:
    def __init__(self, genome_path: str):
        self.index = ""
        with open(genome_path) as f:
            for line in f.readlines():
                if not line.startswith(">"):
                    self.index += line.strip()

    def __getitem__(self, sequence) -> Generator[int, None, None]:
        for i in range(len(self.index) - len(sequence) + 1):
            if self.index[i : i + len(sequence)] == sequence:
                yield i

    def match(self, uces_path: str, threads: int = None):
        pass

    def cleanup(self):
        pass
