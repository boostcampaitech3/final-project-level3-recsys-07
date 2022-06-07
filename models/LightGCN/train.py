import torch
import os

from config import CFG, logging_conf
from datasets import prepare_dataset
from models import build, train
from utils import class2dict, get_logger


# 학습을 위한 기본 설정 (logger, cuda option, device)
logger = get_logger(logging_conf)
use_cuda = torch.cuda.is_available() and CFG.use_cuda_if_available
device = torch.device("cuda" if use_cuda else "cpu")
print(device)


def main():

    # SAVE OUTPUT
    output_dir = "output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    logger.info("Task Started")
    logger.info("[1/1] Data Preparing - Start")

    # (1) train_data : train_data에 대한 edge, label (dict)
    # (2) test_data : test_data에 대한 edge, label (dict)
    # (3) n_node : train + test data 에 존재하는 모든 interaction의 수
    train_data, test_data, n_node = prepare_dataset(
        device, CFG.basepath, verbose=CFG.loader_verbose, is_train=True, logger=logger.getChild("data")
    )
    logger.info("[1/1] Data Preparing - Done")
    
    
    logger.info("[2/2] Model Building - Start")
    model = build(
        n_node,
        embedding_dim=CFG.embedding_dim,
        num_layers=CFG.num_layers,
        alpha=CFG.alpha,
        logger=logger.getChild("build"),
        **CFG.build_kwargs,
    )
    model.to(device)
    logger.info("[2/2] Model Building - Done")


    logger.info("[3/3] Model Training - Start")
    train(
        model,
        train_data,
        n_epoch=CFG.n_epoch,
        learning_rate=CFG.learning_rate,
        use_wandb=CFG.user_wandb,
        weight=CFG.weight_basepath,
        logger=logger.getChild("train"),
    )
    logger.info("[3/3] Model Training - Done")


    logger.info("Task Complete")


if __name__ == "__main__":
    main()