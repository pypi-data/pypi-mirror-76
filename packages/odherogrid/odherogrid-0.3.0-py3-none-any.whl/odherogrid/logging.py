from pathlib import Path
from typing import Union

from loguru import logger

from .settings import CONFIG_DIR

LOGS_DIR: Path = CONFIG_DIR / "logs" 


def logsetup(*, logdir: Union[str, Path]=None) -> None:
    p = logdir or LOGS_DIR
    p = p / "odhg_{time}.log"
    logger.add(p)
    logger.level()

