# What's In Your Closet?

## Rule Based Model 편

`cluster_id` : 아이템의 중분류와 색상이 모두 동일한 것을 묶어 하나의 클러스터로 생성합니다. 그때의 고유한 클러스터의 번호가 cluster_id 입니다.

`item_id` : 크롤링을 진행한 아이템의 고유한 번호입니다.

---

### 모델 실행을 위한 준비 사항

먼저 `LightGCN`의 readme.md를 따라 실행합니다.

이후에, `final-project-level3-recsys-07/preprocessing` 내에 있는 `cluster_item_interaction_matrix.py` 를 실행하여 cluster interaction matrix를 만듭니다. 

`cluster_rule_based.py`에서 클러스터 상호작용 행렬, 아이템 정보 데이터, 그리고 Light-GCN 결과 값 데이터 경로를 지정해줍니다. 

---
