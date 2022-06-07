import argparse
import time
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from scipy import sparse
from dataset import *
from dataloader import *
from loss import *
from model import *
from torch.nn import Softmax


if __name__ == '__main__':
    ## 각종 파라미터 세팅
    parser = argparse.ArgumentParser(description='PyTorch Variational Autoencoders for Collaborative Filtering')

    parser.add_argument('--data', type=str, default='/opt/ml/input/data/train/',
                        help='Movielens dataset location')

    parser.add_argument('--lr', type=float, default=1e-4,
                        help='initial learning rate')
    parser.add_argument('--wd', type=float, default=0.00,
                        help='weight decay coefficient')
    parser.add_argument('--batch_size', type=int, default=500,
                        help='batch size')
    parser.add_argument('--epochs', type=int, default=20,
                        help='upper epoch limit')
    parser.add_argument('--total_anneal_steps', type=int, default=200000,
                        help='the total number of gradient updates for annealing')
    parser.add_argument('--anneal_cap', type=float, default=0.2,
                        help='largest annealing parameter')
    parser.add_argument('--seed', type=int, default=1111,
                        help='random seed')
    parser.add_argument('--cuda', action='store_true',
                        help='use CUDA')
    parser.add_argument('--log_interval', type=int, default=100, metavar='N',
                        help='report interval')
    parser.add_argument('--save', type=str, default='model.pt',
                        help='path to save the final model')
    args = parser.parse_args([])

    # Set the random seed manually for reproductibility.
    torch.manual_seed(args.seed)

    #만약 GPU가 사용가능한 환경이라면 GPU를 사용
    if torch.cuda.is_available():
        args.cuda = True

    device = torch.device("cuda" if args.cuda else "cpu")
    print("Now using device : ", device)

    print(args)

    ###################
    print("Load and Preprocess Movielens dataset")
    # Load Data
    uim = pd.read_csv("/opt/ml/input/workspace/CF/Non-DL/FISM/user_movie_interaction.csv")
    item_id = np.array(list(uim)[1:])
    user_id = uim["user"].to_numpy()
    uim_np = uim.to_numpy()[:, 1:]

    print("Done!")

    ###############################################################################
    # Load the model
    ###############################################################################

    f = open(args.save, 'rb')
    model  = torch.load(f)
    ###############################################################################
    # Training code
    ###############################################################################

    update_count = 0

    model.eval()
    result = list()

    for i in range(31360) : 
        user = user_id[i]
        data = uim_np[i]
        data = torch.FloatTensor(data)
        probability, _, _ = model(data)
        probability = Softmax(probability)
        probability[data.nonzero()] = -np.inf
        idx = np.argpartition(probability, -10)[-10:]
        items = item_id[idx]
        for item in items :
            result.append((user, item))



        
        
        #recon_batch = model(data_tensor)
        #recon_batch = recon_batch.cpu().detach()
        #recon_batch[data.nonzero()] = -np.inf
        #batch_users = recon_batch.shape[0]
        #for row in recon_batch :
        #    user_id = unique_uid[user_cnt]
        #    idx = np.argpartition(row, -10)[-10:]
        #    item_id = unique_sid[idx]
        #    for item in item_id :
        #        result.append((user_id, item))
        #    user_cnt += 1

    info = pd.DataFrame(result, columns=['user','item'])
    info.to_csv("submission.csv",index=False)

    print("Inference Done!")