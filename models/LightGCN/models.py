import os

import numpy as np
import torch
from sklearn.metrics import accuracy_score, roc_auc_score
from torch_geometric.nn.models import LightGCN


def build(n_node, embedding_dim, num_layers, alpha, weight=None, logger=None, **kwargs):
    """
    best.pth 를 모델에 적용시켜주는 함수
    """

    if weight:
        if not os.path.isfile(weight):
            logger.fatal("Model Weight File Not Exist")
        logger.info("Load model")
        state = torch.load(weight)["model"]
        model = LightGCN(
            num_nodes=n_node,
            embedding_dim=embedding_dim,
            num_layers=num_layers,
            alpha=alpha,
            # **kwargs
        )
        model.load_state_dict(state)
        return model
    else:
        logger.info("No load model")
        model = LightGCN(
            num_nodes=n_node,
            embedding_dim=embedding_dim,
            num_layers=num_layers,
            alpha=alpha,
            # kwargs=kwargs,
        )
        return model


def train(
    model,
    train_data,
    valid_data=None,
    n_epoch=100,
    learning_rate=0.01,
    use_wandb=False,
    weight=None,
    logger=None,
):
    """
    인자로 전달받은 model을 주어진 설정에 맞게 학습시키는 함수
    Args:
        model (LightGCN): LightGCN 모델. 파라미터는 build()에서 지정
        train_data (Dict): train dataset (edge, label)로 구성
        valid_data (Dict, optional): valid dataset (edge, label). Defaults to None.
        n_epoch (int, optional): 에폭의 수. Defaults to 100.
        learning_rate (float, optional): 학습률. Defaults to 0.01.
        use_wandb (bool, optional): wandb 사용 여부. Defaults to False.
        weight (str, optional): best_model.pt 가 저장될 경로. Defaults to None.
        logger (object, optional): _description_. Defaults to None.
    """

    # [1] model을 train 모드로 변경
    model.train()

    # [2] optimizer 설정 (default: Adam)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # [3] best.pth가 저장될 폴더 생성
    if not os.path.exists(weight):
        os.makedirs(weight)

    # [4] valid_data가 없는 경우 : train_data에서 edge정보 1000개 랜덤으로 사용
    # valid_data가 train_data에도 사용되는 문제점이....
    if valid_data is None:
        logger.info(f"No valid_data..!")
        eids = np.arange(len(train_data["label"]))
        eids = np.random.permutation(eids)
        valid_eids = eids[:1000]
        train_eids = eids[1000:]
        edge, label = train_data["edge"], train_data["label"]
        label = label.to("cpu").detach().numpy()
        valid_data = dict(edge=edge[:, valid_eids], label=label[valid_eids])
        train_data = dict(edge=edge[:, train_eids],
                          label=torch.Tensor(label[train_eids]).to("cuda"))

    logger.info(f"Training Started : n_epoch={n_epoch}")
    best_auc, best_epoch = 0, -1
    for e in range(n_epoch):
        # forward

        pred = model.predict_link(train_data["edge"], prob=True)
        loss = model.link_pred_loss(pred, train_data["label"])

        # backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # validation
        with torch.no_grad():
            proba = model.predict_link(valid_data["edge"], prob=True)
            proba = proba.detach().cpu().numpy()
            auc = roc_auc_score(valid_data["label"], proba)
            acc = accuracy_score(valid_data["label"], proba > 0.5)

            # ---- Debugging....
            if auc > best_auc:
                import pandas as pd

                pd.DataFrame({"prediction": proba}).to_csv(
                    "./output/train_sample_result.csv", index_label="id"
                )
            # ----------------

            logger.info(
                f" * In epoch {(e+1):04}, loss={loss:.03f}, acc={acc:.03f}, AUC={auc:.03f}"
            )

        # best.pth를 저장할 경로가 있고, 최고 성능을 보여준 경우
        if weight and auc > best_auc:
            logger.info(
                f" * In epoch {(e+1):04}, loss={loss:.03f}, acc={acc:.03f}, AUC={auc:.03f}, Best AUC"
            )
            best_auc, best_epoch = auc, e
            torch.save(
                {"model": model.state_dict(), "epoch": e + 1},
                os.path.join(weight, f"best_model.pt"),
            )

    # last.pth 저장
    torch.save(
        {"model": model.state_dict(), "epoch": e + 1},
        os.path.join(weight, f"last_model.pt"),
    )
    logger.info(f"Best Weight Confirmed : {best_epoch+1}'th epoch")


def inference(model, data, logger=None):
    model.eval()
    with torch.no_grad():
        pred = model.predict_link(data["edge"], prob=True)
        return pred