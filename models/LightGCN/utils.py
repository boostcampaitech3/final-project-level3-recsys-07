import os
import random

import numpy as np
import torch


class process:
    def __init__(self, logger, name):
        self.logger = logger
        self.name = name

    def __enter__(self):
        self.logger.info(f"{self.name} - Started")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info(f"{self.name} - Complete")


def setSeeds(seed=42):
    # 랜덤 시드를 설정하여 매 코드를 실행할 때마다 동일한 결과를 얻게 합니다.
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True


def get_logger(logger_conf):
    import logging
    import logging.config

    logging.config.dictConfig(logger_conf)
    logger = logging.getLogger()
    return logger


def class2dict(f):
    return dict(
        (name, getattr(f, name)) for name in dir(f) if not name.startswith("__")
    )