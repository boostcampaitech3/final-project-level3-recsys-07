## 데이터 경로 설정법

/opt/ml/input/data/asset_codishop/view/item/training_data.csv로 현재 파일 경로가 설정되어 있습니다.
- training_data.csv : cluster-item 상호작용 정보를 dense하게 표현한 dataframe (cluster, item, count)
    - 실제 column 명은 (user, item, time)으로 설정해야 됩니다.

## 훈련

train.py 파일을 실행시키면 됩니다. 
만약 Denoising Variational Autoencoder를 훈련시키고 싶으시면, DAE_train.py를 실행시키면 됩니다!