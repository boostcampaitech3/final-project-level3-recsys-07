import os
import random
import torch

import numpy as np


# logger 출력 format을 위한 함수
class process:
    def __init__(self, logger, name):
        self.logger = logger
        self.name = name

    def __enter__(self):
        self.logger.info(f"{self.name} - Started")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info(f"{self.name} - Complete")


# random soeed 고정
def setSeeds(seed=42):
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True


# logger 반환
def get_logger(logger_conf):
    import logging
    import logging.config

    logging.config.dictConfig(logger_conf)
    logger = logging.getLogger()
    return logger


# class의 정보를 dication으로 반환
def class2dict(f):
    return dict(
        (name, getattr(f, name)) for name in dir(f) if not name.startswith("__")
    )