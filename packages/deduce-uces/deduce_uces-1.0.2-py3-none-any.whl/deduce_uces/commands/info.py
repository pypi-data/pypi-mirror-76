import shutil

from deduce_uces.Logger import LOG_LEVEL_INFO, LOG_LEVEL_WARNING

DEPENDENCIES = [
    ("jellyfish", ["find"]),
    ("bowtie2", ["align"]),
    ("minimap2", ["extend"]),
]


def command_info(args, logger):
    logger.log("dedUCE version 1.0.2", LOG_LEVEL_INFO)
    logger.log("Checking dependencies...", LOG_LEVEL_INFO)

    for dep in DEPENDENCIES:
        path = shutil.which(dep[0])

        if path:
            logger.log(f"Found {dep[0]} at {path}", LOG_LEVEL_INFO)
        else:
            logger.log(
                f"Missing dependency {dep[0]}! These features won't be available: {', '.join(dep[1])}",
                LOG_LEVEL_WARNING,
            )
