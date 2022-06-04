import os
from scipy import sparse
import pandas as pd
import numpy as np
import torch

class DataLoader():
    '''
    Load Movielens dataset
    '''
    def __init__(self, path):
        
        self.pro_dir = os.path.join(path, 'pro_sg')
        assert os.path.exists(self.pro_dir), "Preprocessed files do not exist. Run data.py"

        self.n_items = self.load_n_items()
    
    def load_data(self, datatype='train'):
        if datatype == 'train':
            return self._load_train_data()
        elif datatype == 'validation':
            return self._load_tr_te_data(datatype)
        elif datatype == 'test':
            return self._load_tr_te_data(datatype)
        else:
            raise ValueError("datatype should be in [train, validation, test]")
        
    def load_n_items(self):
        unique_sid = list()
        with open(os.path.join(self.pro_dir, 'unique_sid.txt'), 'r') as f:
            for line in f:
                unique_sid.append(line.strip())
        n_items = len(unique_sid)
        return n_items
    
    def _load_train_data(self):
        path = os.path.join(self.pro_dir, 'train.csv') 
        
        tp = pd.read_csv(path) # 
        n_users = tp['uid'].max() + 1 # 유저의 수는 유저 index의 최대 값 + 1
        # train data는 shuffle된 유저 index 0 ~ 25359 번째 까지 0부터 순서대로 포함되어 있기 때문에 max + 1 해도 된다.

        rows, cols = tp['uid'], tp['sid']
        data = sparse.csr_matrix((np.ones_like(rows),
                                 (rows, cols)), dtype='float64',
                                 shape=(n_users, self.n_items))
        # sparse matrix를 압축된 형태로 변경해준다. M x N sparse matrix -> 실제로 값이 0이 아닌 칸에 대해 (x, y) value 반환
        # row = user_index, col = item_index, value = 모든 값이 1인 vector
        return data
    
    def _load_tr_te_data(self, datatype='test'):
        tr_path = os.path.join(self.pro_dir, '{}_tr.csv'.format(datatype))
        te_path = os.path.join(self.pro_dir, '{}_te.csv'.format(datatype))

        tp_tr = pd.read_csv(tr_path)
        tp_te = pd.read_csv(te_path)

        start_idx = min(tp_tr['uid'].min(), tp_te['uid'].min()) # 가장 index가 작은 유저 index = start_idx
        end_idx = max(tp_tr['uid'].max(), tp_te['uid'].max()) # end_idx = 가장 index가 큰 유저

        rows_tr, cols_tr = tp_tr['uid'] - start_idx, tp_tr['sid'] # rows_tr를 0부터 시작하게끔, sid는 그대로
        rows_te, cols_te = tp_te['uid'] - start_idx, tp_te['sid'] # rows_te를 0부터 시작하게끔, sid는 그대로

        data_tr = sparse.csr_matrix((np.ones_like(rows_tr),
                                    (rows_tr, cols_tr)), dtype='float64', shape=(end_idx - start_idx + 1, self.n_items))
        data_te = sparse.csr_matrix((np.ones_like(rows_te),
                                    (rows_te, cols_te)), dtype='float64', shape=(end_idx - start_idx + 1, self.n_items))
        return data_tr, data_te

def sparse2torch_sparse(data):
    """
    Convert scipy sparse matrix to torch sparse tensor with L2 Normalization
    This is much faster than naive use of torch.FloatTensor(data.toarray())
    https://discuss.pytorch.org/t/sparse-tensor-use-cases/22047/2
    """
    samples = data.shape[0]
    features = data.shape[1]
    coo_data = data.tocoo()
    indices = torch.LongTensor([coo_data.row, coo_data.col])
    row_norms_inv = 1 / np.sqrt(data.sum(1))
    row2val = {i : row_norms_inv[i].item() for i in range(samples)}
    values = np.array([row2val[r] for r in coo_data.row])
    t = torch.sparse.FloatTensor(indices, torch.from_numpy(values).float(), [samples, features])
    return t

def naive_sparse2tensor(data):
    return torch.FloatTensor(data.toarray())