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
import json

# mlflow setting
def mlflow_set():
    return

def train(model, criterion, optimizer, is_VAE = False):
    # Turn on training mode
    model.train()
    train_loss = 0.0
    start_time = time.time()
    global update_count

    np.random.shuffle(idxlist)
    
    for batch_idx, start_idx in enumerate(range(0, N, args.batch_size)): # 0 ~ 총 데이터 개수까지 batch size만큼 잘라서 indexing
        end_idx = min(start_idx + args.batch_size, N) # 총 데이터 개수를 넘지 않게 min 
        data = train_data[idxlist[start_idx:end_idx]] 
        data = naive_sparse2tensor(data).to(device) # dense representation을 다시 sparse matrix로 변환
        # batch size만큼 잘려서 data가 multi one hot encoding vector 형태로 들어가게 된다. 따라서 user 단위로 명확하게 잘리지 않을 수 있다. 

        optimizer.zero_grad()

        if is_VAE:
          if args.total_anneal_steps > 0:
            anneal = min(args.anneal_cap, 
                            1. * update_count / args.total_anneal_steps)
            # loss function에 사용되는 beta 값을 update에 수에 비례해서 키운다.
            # anneal cap은 beta 값의 상한선이다. default = 0.2
          else:
              anneal = args.anneal_cap

          optimizer.zero_grad()
          recon_batch, mu, logvar = model(data)
          
          loss = criterion(recon_batch, data, mu, logvar, anneal)
        else:
          recon_batch = model(data)
          loss = criterion(recon_batch, data)

        loss.backward()
        train_loss += loss.item()
        optimizer.step()

        update_count += 1

        if batch_idx % args.log_interval == 0 and batch_idx > 0:
            elapsed = time.time() - start_time
            print('| epoch {:3d} | {:4d}/{:4d} batches | ms/batch {:4.2f} | '
                    'loss {:4.2f}'.format(
                        epoch, batch_idx, len(range(0, N, args.batch_size)),
                        elapsed * 1000 / args.log_interval,
                        train_loss / args.log_interval))
            

            start_time = time.time()
            train_loss = 0.0


def evaluate(model, criterion, data_tr, data_te, is_VAE=False):
    # Turn on evaluation mode
    model.eval()
    total_loss = 0.0
    global update_count
    e_idxlist = list(range(data_tr.shape[0]))
    e_N = data_tr.shape[0] # evaluation data의 instance 개수
    n100_list = []
    r20_list = []
    r50_list = []
    
    with torch.no_grad():
        for start_idx in range(0, e_N, args.batch_size):
            end_idx = min(start_idx + args.batch_size, e_N) # N -> e_N으로 수정
            data = data_tr[e_idxlist[start_idx:end_idx]] # TODO : data_tr, data_te의 총 개수가 다르지 않은가? 똑같이 indexing하면 index error 발생 안하나?
            heldout_data = data_te[e_idxlist[start_idx:end_idx]]
            # TODO : 왜 data_tr, data_te 모두 길이가 3000인가?

            data_tensor = naive_sparse2tensor(data).to(device)

            if is_VAE :
              
              if args.total_anneal_steps > 0:
                  anneal = min(args.anneal_cap, 
                                1. * update_count / args.total_anneal_steps)
              else:
                  anneal = args.anneal_cap

              recon_batch, mu, logvar = model(data_tensor)

              loss = criterion(recon_batch, data_tensor, mu, logvar, anneal)

            else :
              recon_batch = model(data_tensor)
              loss = criterion(recon_batch, data_tensor)

            total_loss += loss.item()

            # Exclude examples from training set
            recon_batch = recon_batch.cpu().numpy()
            recon_batch[data.nonzero()] = -np.inf

            n100 = NDCG_binary_at_k_batch(recon_batch, heldout_data, 100)
            r20 = Recall_at_k_batch(recon_batch, heldout_data, 10)
            r50 = Recall_at_k_batch(recon_batch, heldout_data, 50)
            n100_list.append(n100)
            r20_list.append(r20)
            r50_list.append(r50)
 
    total_loss /= len(range(0, e_N, args.batch_size))
    n100_list = np.concatenate(n100_list)
    r20_list = np.concatenate(r20_list)
    r50_list = np.concatenate(r50_list)

    return total_loss, np.mean(n100_list), np.mean(r20_list), np.mean(r50_list)



if __name__ == '__main__':
    ## 각종 파라미터 세팅
    parser = argparse.ArgumentParser(description='PyTorch Variational Autoencoders for Collaborative Filtering')

    parser.add_argument('--data', type=str, default='/opt/ml/input/data/asset_codishop/view/item/',
                        help='Movielens dataset location')

    parser.add_argument('--lr', type=float, default=1e-4,
                        help='initial learning rate')
    parser.add_argument('--wd', type=float, default=0.00,
                        help='weight decay coefficient')
    parser.add_argument('--batch_size', type=int, default=500,
                        help='batch size')
    parser.add_argument('--epochs', type=int, default=1,
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

    device = torch.device("cuda" if args.cuda else "cpu") #GPU가 있다면 device로 설정
    print("Now using device : ", device)

    print(args)

    ###################
    print("Load and Preprocess Movielens dataset")
    # Load Data
    DATA_DIR = args.data
    raw_data = pd.read_csv(os.path.join(DATA_DIR, 'training_data.csv'), header=0) # train_ratings.csv dataframe으로 불러오기.
    #만약 첫번째 행이 열 이름이라면 header=0, 열 이름이 없다면 header=None
    print("원본 데이터\n", raw_data)

    raw_data, user_activity, item_popularity = filter_triplets(raw_data, min_uc=0, min_sc=0)
    #제공된 훈련데이터의 유저는 모두 5개 이상의 리뷰가 있습니다.
    print("5번 이상의 리뷰가 있는 유저들로만 구성된 데이터\n",raw_data)
    #user_activity, item_popularity = get_count(raw_data, 'user'), get_count(raw_data, 'item')
    print("유저별 리뷰수\n",user_activity)
    print("아이템별 리뷰수\n",item_popularity)

    # Shuffle User Indices
    unique_uid = user_activity.index # User_ID 추출 [11, 14, ... 138493]
    
    print("(BEFORE) unique_uid:",unique_uid)
    np.random.seed(98765)
    idx_perm = np.random.permutation(unique_uid.size) # np.random.permutation(N) = 1~N까지의 숫자를 shuffle해서 array로 반환
    unique_uid = unique_uid[idx_perm] # user_id를 무작위로 섞어준다
    print("(AFTER) unique_uid:",unique_uid)

    n_users = unique_uid.size #31360
    n_heldout_users = 200

    ###############################################################################
    # Data set
    ###############################################################################

    # Split Train/Validation/Test User Indices
    #tr_users = unique_uid[:(n_users - n_heldout_users * 2)] # user_id 0 ~ 25359
    tr_users = unique_uid[ : n_heldout_users * 2]
    vd_users = unique_uid[(n_users - n_heldout_users * 2) : (n_users - n_heldout_users)] # user_id 25360 ~ 28359
    te_users = unique_uid[(n_users - n_heldout_users) : ] # user_id 28360 ~ 31360

    #주의: 데이터의 수가 아닌 사용자의 수입니다!
    print("훈련 데이터에 사용될 사용자 수:", len(tr_users)) #25360개
    print("검증 데이터에 사용될 사용자 수:", len(vd_users)) #3000개
    print("테스트 데이터에 사용될 사용자 수:", len(te_users)) #3000개

    ##훈련 데이터에 해당하는 아이템들
    #Train에는 전체 데이터를 사용합니다.
    train_plays = raw_data.loc[raw_data['user'].isin(tr_users)] # tr_users에 있는 user_id만 추출해서 시청 기록 추출
    # train_plays = user, item, time으로 구성된 dataframe
    # dataframe.isin(value) -> dataframe의 각 요소가 value라는 리스트안에 있는지 True, False 값을 반환한다.
    # raw_data.loc[index]의 index는 boolean 값으로 구성된 array가 와도 된다.

    ##아이템 ID
    unique_sid = pd.unique(train_plays['item']) #train_user들이 본 item_id 추출 -> 실제론 모든 item_id 추출

    # show_id : index , user_id : index 형식의 dictionary 
    show2id = dict((sid, i) for (i, sid) in enumerate(unique_sid))
    profile2id = dict((pid, i) for (i, pid) in enumerate(unique_uid))
    #id2show = dict((i, sid) for (i, sid) in enumerate(unique_sid))
    #id2profile = dict((i, pid) for (i, pid) in enumerate(unique_uid))

    pro_dir = os.path.join(DATA_DIR, 'pro_sg')

    if not os.path.exists(pro_dir):
        os.makedirs(pro_dir)

    with open(os.path.join(pro_dir, 'unique_sid.txt'), 'w') as f:
        for sid in unique_sid:
            f.write('%s\n' % sid)

    #Validation과 Test에는 input으로 사용될 tr 데이터와 정답을 확인하기 위한 te 데이터로 분리되었습니다.
    vad_plays = raw_data.loc[raw_data['user'].isin(vd_users)] # vad_plays = vd_users 안에 있는 유저들의 행 (user, item, time) 만 불러옴
    vad_plays = vad_plays.loc[vad_plays['item'].isin(unique_sid)] # 추출된 vad_plays 중 item_id가 unique_sid안에 있는 행만 남긴다 -> 실제로 변화 없음
    vad_plays_tr, vad_plays_te = split_train_test_proportion(vad_plays) # 유저가 시청한 영화 중 20%를 입력 값으로 넣지 않고 뺴 놓은다.
    # vad_plays_tr shape : (397924, 3) vad_plays_te shape :(98001, 3) 

    test_plays = raw_data.loc[raw_data['user'].isin(te_users)]
    test_plays = test_plays.loc[test_plays['item'].isin(unique_sid)]
    test_plays_tr, test_plays_te = split_train_test_proportion(test_plays)
    # test_plays_tr shape : (393157, 3) test_plays_te shape : (96791, 3) 


    # 총 4,168,598개의 (user_index, item_index) instance
    train_data = numerize(train_plays, profile2id, show2id) 
    train_data.to_csv(os.path.join(pro_dir, 'train.csv'), index=False)

    # 총 495,925개의 (user_index, item_index) instance
    vad_data_tr = numerize(vad_plays_tr, profile2id, show2id) 
    vad_data_tr.to_csv(os.path.join(pro_dir, 'validation_tr.csv'), index=False)

    vad_data_te = numerize(vad_plays_te, profile2id, show2id)
    vad_data_te.to_csv(os.path.join(pro_dir, 'validation_te.csv'), index=False)

    # 총 489,948개의 (user_index, item_index) instance
    test_data_tr = numerize(test_plays_tr, profile2id, show2id) 
    test_data_tr.to_csv(os.path.join(pro_dir, 'test_tr.csv'), index=False)

    test_data_te = numerize(test_plays_te, profile2id, show2id)
    test_data_te.to_csv(os.path.join(pro_dir, 'test_te.csv'), index=False)

    print("Done!")

    
    ###############################################################################
    # Load data
    ###############################################################################

    loader = DataLoader(args.data)

    n_items = loader.load_n_items()
    train_data = loader.load_data('train') # "(user_index, item_index) 1" 형식의 instance 모음 (index 값을 기준으로 정렬되어 있다)
    vad_data_tr, vad_data_te = loader.load_data('validation') # "(user_index, item_index) 1" 형식의 instance 모음 (index 값을 기준으로 정렬되어 있다)
    test_data_tr, test_data_te = loader.load_data('test') # "(user_index, item_index) 1" 형식의 instance 모음 (index 값을 기준으로 정렬되어 있다)

    N = train_data.shape[0] # train_data instance의 개수 
    idxlist = list(range(N)) # 0 ~ 4,168,598

    ###############################################################################
    # Build the model
    ###############################################################################

    p_dims = [200, 600, n_items] 
    #q_dims = [n_items, 600, 200]
    model = MultiVAE(p_dims=p_dims, ).to(device)

    optimizer = optim.Adam(model.parameters(), lr=1e-3, weight_decay=args.wd) # Multi VAE 모델은 weight decay = 0 사용하지 않음
    criterion = loss_function_vae # Multi VAE loss function :  KL Divergence 

    ###############################################################################
    # Training code
    ###############################################################################

    best_n100 = -np.inf
    update_count = 0

    for epoch in range(1, args.epochs + 1):
        epoch_start_time = time.time()
        train(model, criterion, optimizer, is_VAE=True)
        val_loss, n100, r20, r50 = evaluate(model, criterion, vad_data_tr, vad_data_te, is_VAE=True)
        print('-' * 89)
        print('| end of epoch {:3d} | time: {:4.2f}s | valid loss {:4.2f} | '
                'n100 {:5.3f} | r20 {:5.3f} | r50 {:5.3f}'.format(
                    epoch, time.time() - epoch_start_time, val_loss,
                    n100, r20, r50))
        print('-' * 89)

        n_iter = epoch * len(range(0, N, args.batch_size))


        # Save the model if the n100 is the best we've seen so far.
        if n100 > best_n100:
            with open(args.save, 'wb') as f:
                torch.save(model, f)
            best_n100 = n100



    # Load the best saved model.
    with open(args.save, 'rb') as f:
        model = torch.load(f)

    # Run on test data.
    test_loss, n100, r20, r50 = evaluate(model, criterion, test_data_tr, test_data_te, is_VAE=True)
    print('=' * 89)
    print('| End of training | test loss {:4.2f} | n100 {:4.2f} | r20 {:4.2f} | '
            'r50 {:4.2f}'.format(test_loss, n100, r20, r50))
    print('=' * 89)