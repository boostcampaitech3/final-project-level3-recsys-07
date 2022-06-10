# What's In Your Closet?

## Light GCN 편

`cluster_id` : 아이템의 중분류와 색상이 모두 동일한 것을 묶어 하나의 클러스터로 생성합니다. 그때의 고유한 클러스터의 번호가 cluster_id 입니다.

`item_id` : 크롤링을 진행한 아이템의 고유한 번호입니다.

위의 설명을 바탕으로 cluster_id와 item_id간의 상호작용 정보를 입력으로 하여 lightGCN 모델을 통해 클러스터와 아이템간의 상호작용 확률을 알아낼 수 있도록 학습했습니다.

이때, cluster_id와 item_id간의 상호작용행렬의 sparsity는 99.4% 정도가 되기 때문에 모든 정보를 사용하게 되면 0으로만 예측을 해도 accuracy 수치가 99.4%가 나와버리는 문제가 발생합니다.

그렇기에 학습에 사용되는 데이터도 상호작용 결과의 비율이 비슷하도록 설정해주었습니다.  

- 클러스터ID, 아이템ID, 상호작용 = 1 : 4799개의 데이터 존재  
- 클러스터ID, 아이템ID, 상호작용 = 0 : 6723개의 데이터 존재 (기존 약 68만개)

여기서 또 주의해야 하는 것은, 상호작용을 하지 않았다고 해서 진짜로 그 클러스터와 아이템이 어울리지 않는다는 것을 의미하지 않습니다. 어울리는데 그런 코디가 없어서 상호작용 정보가 없을 수 있고, 데이터 크롤링 범위에 그런 코디가 없어서 상호작용이 0이라고 표시된 것일 수도 있습니다. 그리고 이 문제를 `LightGCN`이 해결해 줄 수 있을 것이라고 생각했습니다.

---

### 본격적인 모델 실험을 위한 준비사항

Jira Google Drive에 올라간 dataset 사용 (data.zip 소유자: killerwhale)  
위의 데이터셋을 이용하여 전처리 진행 (preprocess branch / preprocess_item.py 실행)  

이후에, 현재 폴더 내에 있는 `make_cluster_item_interaction.ipynb` 로 모든 클러스터와 아이템 사이의 interaction 정보를 리스트로 추출하여 저장

모델 실행 : `python3 train.py`  
추론 진행 : `python3 inference.py`

이때 추론은 모든 클러스터와 아이템 사이의 interaction할 확률을 예측하도록 설정.

---

### 모델 inference 결과

추론 결과, 실제로 interaction을 한 클러스터와 아이템 사이의 확률은 대부분 99%로 정확하게 나왔고, 상호작용을 하지 않았던 아이템과 클러스터 사이에서도 높은 확률로 연결될 수 있는 정보들이 나왔습니다.

---

### 다 필요없고 진짜 최종 정보

Jira - Google Drive에 올라간 `cluster_item_prob.csv` 파일만 사용하면 됩니다.  

csv파일 내부는 `item_id`, `cluster_id`, `prob` 3개의 칼럼으로 이루어져 있으며, 각각 item_id가 cluster_id와 상호작용할 확률을 예측한 결과(prob)를 의미합니다.

streamlit으로 서빙하는 단계에서는 이 csv정보만을 사용해서 한다면, 미리 계산된 정보이기 때문에 매우 빠른 시간안에 inference가 가능합니다.

사용자로 부터 입력받은 아이템의 `cluster_id` 를 추출하고, 그 cluster_id와 가장 상호작용 확률이 높은 아이템들을 추천해주면 될 것 같습니다.

아직 모든 결과를 확인해본 것은 아니라서 Rule-Based와 50:50 으로 섞어서 추천하는 것이 더 만족스러운 결과가 나올 것 같습니다.

---

### 모델 학습 Configuration 정보 (hyperparamter)

```
n_epoch = 10000
learning_rate = 0.005
embedding_dim = 250  # int
num_layers = 6  # int

Result : loss=0.537, acc=0.657, AUC=0.728
```