import os
from xmlrpc.client import Boolean

import pandas as pd
import torch

from typing import Dict, List, Optional, Union


def prepare_dataset(
    device: str, 
    basepath: str, 
    is_train: bool,
    verbose:bool=True, 
    logger=None,
    ) -> Union[Dict[List[int], int], Dict[List[int], int], int]:

    """train과 test 데이터셋을 만들어주는 함수
    Args:
        device (str): cpu 또는 cuda:0 선택
        basepath (str): 데이터셋이 저장된 폴더 경로
        verbose (bool, optional): 데이터셋 정보를 출력할 것인지. Defaults to True.
        logger (object, optional): 데이터셋 정보를 출력할 logger. Defaults to None.
    Returns:
        train_data_proc (dict) : train_data에 대한 edge, label 생성
        test_data_proc (dict) : test_data에 대한 edge, label 생성
        len(id2index) (dict) : 모든 interaction의 수
    """

    # basepath로 부터 train_data.csv + test_data.csv 합친 것 불러오기
    data = load_data(basepath, is_train)

    # 불러온 data를 answerCode를 기준으로 다시 train과 test로 분리
    if is_train:
        train_data, test_data = separate_data(data)
    else:
        train_data = data
        test_data = data

    # user2index, assessmentItemID2index 계산
    id2index = indexing_data(data)

    # Graph 정보 생성: dict(Edge, Label)
    # - Edge : userID <----> assessmentItemID
    # - Label : answerCode
    train_data_proc = process_data(train_data, id2index, device)
    test_data_proc = process_data(test_data, id2index, device)

    if verbose:
        print_data_stat(train_data, "Train", logger=logger)
        print_data_stat(test_data, "Test", logger=logger)

    return train_data_proc, test_data_proc, len(id2index)


def load_data(basepath: str, is_train: bool) -> pd.DataFrame:
    """
    train과 test 데이터셋을 불러와서 합친 후,
    userID와 assessmentItemID 쌍이 고유한 것들만 남기고
    나머지는 제거한다.
    Args:
        basepath (str): 데이터셋이 존재하는 폴더 경로
    Returns:
        data (pd.DataFrame): train과 test set이 합쳐진 데이터셋
    """

    if is_train:
        path = os.path.join(basepath, 'item_cluster_interaction.csv')
    else:
        path = os.path.join(basepath, 'item_cluster_all_interaction.csv')

    print (f"[INFO] 아이템(옷)과 클러스터의 상호작용 여부 정보를 {path} 로 부터 가져옵니다.")
    data = pd.read_csv(path, dtype={'item_id': str, 'cluster_id': str, 'interaction': int})
    data.drop_duplicates(subset=["item_id", "cluster_id"], keep="last", inplace=True)

    return data


def separate_data(data: pd.DataFrame) -> Union[pd.DataFrame, pd.DataFrame]:
    """
    data를 train과 test data로 재분리
    - answerCode >= 0  : train data
    - answerCode == -1 : test data
    Args:
        data (pd.DataFrame): train+test data
    Returns:
        train_data (pd.DataFrame)
        test_data (pd.DataFrame)
    """

    data = data.sample(frac=1, random_state=1).reset_index()
    
    total_len = len(data)
    train_len = int(total_len * 0.8)
    
    train_data = data.iloc[:train_len]
    test_data  = data.iloc[train_len:]

    print ("[INFO] 학습데이터와 테스트 데이터로 나눕니다. train시에는 학습을, inference에는 테스트데이터만 사용합니다.")
    print (f"Train data의 수 : {len(train_data)}")
    print (f"Test data의 수 : {len(test_data)}")
    return train_data, test_data


def indexing_data(data: pd.DataFrame) -> Dict[int, List[int]]:
    """
    user를 0부터 다시 번호 매기기 (0 ~ n_user - 1)
    assessmentItemID 다시 번호 매기기 (0 ~ n_item - 1)
    Args:
        data (pd.DataFrame): train+test data
    Returns:
        id_2_index (dict): userID 또는 assessmentItemID를 reindexing 한 table
    """
    item_id, codi_id = (
        sorted(list(set(data.item_id))),
        sorted(list(set(data.cluster_id))),
    )
    n_item, n_codi = len(item_id), len(codi_id)

    userid_2_index = {str(v): i for i, v in enumerate(item_id)}
    itemid_2_index = {str(v): i + n_item for i, v in enumerate(codi_id)}
    id_2_index = dict(userid_2_index, **itemid_2_index)

    return id_2_index


def process_data(data: pd.DataFrame, id_2_index: Dict[int, int], device: str) -> Dict[List[int], int]:
    """
    user와 item을 edge로 연결하고, edge에 대한 정답을 label로 지정
    Args:
        data (pd.DataFrame): train+test data
        id_2_index (dict): userID 또는 assessmentItemID를 reindexing 한 table
        device (str): cpu 또는 cuda:0 선택
    Returns:
        dict(list(), list()): edge와 label list
    """
    edge, label = [], []
    for item_id, codi_id, inter in zip(data.item_id, data.cluster_id, data.interaction):
        uid, iid = id_2_index[item_id], id_2_index[codi_id]
        edge.append([uid, iid])
        label.append(inter)

    edge = torch.LongTensor(edge).T
    label = torch.LongTensor(label)

    return dict(edge=edge.to(device), label=label.to(device))


def print_data_stat(data: pd.DataFrame, name: str, logger) -> None:
    itemid, codiid = list(set(data.item_id)), list(set(data.cluster_id))
    n_user, n_item = len(itemid), len(codiid)

    logger.info(f"{name} Dataset Info")
    logger.info(f" * Num. item    : {n_user}")
    logger.info(f" * Max. item   : {max(itemid)}")
    logger.info(f" * Num. codi_id    : {n_item}")
    logger.info(f" * Num. Records  : {len(data)}")