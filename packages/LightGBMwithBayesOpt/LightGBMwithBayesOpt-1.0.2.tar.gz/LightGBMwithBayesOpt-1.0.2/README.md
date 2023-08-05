## Modeling by **LigthGBM** with hyper-parameter tuning using **Bayesian Optimization**


* 본 패키지는 Microsoft사에서 개발한 Light GBM 알고리즘으로 classification 문제의 학습 및 테스트를 돕는 툴이다.
* 학습의 hyper-parmeter tuning 수행 시, Bayesian Optimization을 통해 방대한 parameter hyperplane 상에서 효율적으로 optimal parameter set을 찾도록 돕는다.
* k-fold cross validation으로 학습을 수행하여 안정적인 성능을 내는 parameter set을 찾는 것을 목표로 한다.
* multiclassification의 경우, 모델링 타켓이 아닌 레이블을 가진 데이터도 활용하며 이들은 오로지 검증/테스트 시에만 활용되도록 제한둔다.
```
예) 모델링 타켓 레이블은 "0플랜 스몰, 0플랜 미디엄, 0플랜 라지"이나, 주어진 데이터의 레이블에는 T플랜 에센스, T플랜 안심2.5G 등 좀 더 다양한 종류를 가질 수 있다. 이들은 평가 시, 정답률을 낮추지만 해당 패키지는 수용하게끔 설계가 되어있다.
```



### *class* LightGBMwithBayesOpt
Bayesian Optimization으로 Light GBM의 hyper-parameter tuning을 수행하고, 최적의 parameter set을 찾을 수 있게 설계됨

1. Input Arguments

|name|default|type|meaning|
|----|-------|----|-------|
|`X`|-|numpy array, pandas dataframe|독립 변수 셋|
|`y`|-|numpy array, list, pandas dataframe/series|종속 변수(only for classification)|
|`n_fold`|-|int|k-fold cross validation의 k|
|`rangeable_params`|-|dictionary|연속형의 범위를 가지는 파라미터의 '파라미터명: (최소값, 최대값)'|
|`int_params`|-|list, numpy array|정수형 및 범주형 파라미터명|
|`n_tuning`|-|int|hyper-parameter tuning 수행 수|
|`target_labels`|-|list, numpy array|관심 타켓 레이블명|
|`selective_params`|None|dictionary|범주형의 값을 가지는 파라미터의 '파라미터명: [범주1, 범주2]'|
|`categorical_feature`|None|list, numpy array|범주형 변수명|
|`metrics`|['mcc']|list, numpy array|hyper-parameter tuning 중 검증 시, 활용하는 메트릭명(지원 메트릭: 'accuary', 'mcc')|
|`metric_larger_better`|True|bool|검증 메트릭의 대소 방향성이 가지는 성능상 의미(단, 복수의 메트릭이 있더라도 두 메트릭 방향은 동일해야 함)|
|`pred_modes`|['prob_first', 'rank_first']|list|검증 시, 예측값을 결정하기 위한 수단명(지원 모드: 'prob_first' and 'rank_first' for multiclassification; 'cut_off' and 'top_percentile' for binary-classification)|
|`thresholds`|None|list|pred_modes가 binary용일 경우, 해당 메트릭에 필요한 기준값|


2. Class Variables

|name|type|meaning|
|----|----|-------|
|`X`|numpy array, pandas dataframe|독립 변수 셋|
|`y`|numpy array|종속 변수|
|`num_y`|numpy array|`y`의 레이블 인코딩값|
|`data_set`|light gbm dataset|Light GBM 학습을 지원하는 데이터 구조(`X`와 `y`를 포함)|
|`target_labels`|list, numpy array|관심 타켓 레이블명|
|`num_class`|int|관심 타켓 레이블수|
|`label_dist`|pandas series|관심 타켓 레이블의 분포|
|`categorical_feature`|list, numpy array|범주형 변수명|
|`nfold`|int|k-fold cross validation의 k|
|`selective_params`|dictionary|범주형의 값을 가지는 파라미터의 '파라미터명: [범주1, 범주2, ...]'|
|`rangeable_params`|dictionary|모든 타입의 파라티터의 '파라미터명: (최소값, 최대값)'; 단, 범주형의 경우는 범주를 레이블 인코딩하여 그 중 최소/최대값으로 표현함|
|`int_params`|list, numpy array|정수형 및 범주형 파라미터명|
|`metrics`|list, numpy array|hyper-parameter tuning 중 검증 시, 활용하는 메트릭명|
|`metric_larger_better`|bool|검증 메트릭의 대소 방향성이 가지는 성능상 의미|
|`pred_modes`|list, numpy array|검증 시, 예측값을 결정하기 위한 수단명|
|`thresholds`|list, numpy array|pred_modes가 binary용일 경우, 해당 메트릭에 필요한 기준값|
|`n_tuning`|int|hyper-parameter tuning 수행 수|
|`parameter_tuner`|bayesian optimizer|hyper-parameter tuning을 수행하는 튜너|
|`parameter_perf`|pandas dataframe|각 hyper-parameter tuning의 파라미터 셋과 그 성능|
|`best_parameter`|dictionary|optimal parameter set|

3. Class Functions

|name|inputs|return value|work|
|----|------|------------|----|
|`do_parameter_tuning`|-|bayesian optimizer(`parameter_tuner`)|hyper-parameter tuning을 수행|
|`do_train_with_given_parameter`|params: parameter set; data_set: light gbm dataset of 독립 변수 셋과 종속 변수|light gbm classifier|주어진 data_set에 대해 주어진 parameter set으로 학습|
|`make_saveable_object`|-|[`label_dist`, `parameter_perf`, `best_parameter`, best model]; best model: model trained with `best_parameter` of `data_set`|본 클래스의 주요 결과들을 리스트형 반환|


### *class* LightGBMEvaluator
주어진 Light GBM 모델로 주어진 독립 변수 셋을 예측할 수 있고,
여러 방법으로 레이블을 추출가능하며, 
추출된 레이블과 실제값의 Accuracy와 Matthew's Correlational Coefficient를 측정가능하게 지원한다.

1. Input Arguments

|name|default|type|meaning|
|----|-------|----|-------|
|`model`|-|light gbm classifier|light gbm으로 학습된 모델|
|`X`|-|numpy array, pandas dataframe|독립 변수 셋|
|`target_labels`|-|list, numpy array|관심 타켓 레이블|
|`y`|None|list, numpy array, pandas dataframe/series|종속 변수|
|`given_ids`|None|list, numpy array, pandas dataframe/series|데이터의 primary key|

2. Class Variables

|name|type|meaning|
|----|----|-------|
|`target_labels`|list, numpy array|관심 타켓 레이블|
|`model`|light gbm classifier|light gbm으로 학습된 모델|
|`X`|numpy array, pandas dataframe|독립 변수 셋|
|`y`|numpy array|종속 변수|
|`new_y`|numpy array|종속 변수의 레이블 인코딩된 값(`y`가 string 타입일 때만 생성)|
|`have_new_y`|bool|`new_y`가 존재할 때 True, 그렇지 않다면 False|
|`ids`|list, numpy array, pandas dataframe/series|데이터의 primary key(`given_ids`으로 주어질 때만 생성)|


3. Class Functions

|name|inputs|return value|work|
|----|------|------------|----|
|`score_predict`|raw: True/False|numpy array for binary, pandas dataframe for multiclass|raw=True, raw_score를; raw=False, softmax된 score를 출력|
|`label_predict`|scores: numpy array for binary, pandas dataframe for multiclass; mode: 'prob_first' and 'rank_first' for multiclass; 'cut_off' and 'top_percentile' for binary; thresholds: pred_modes가 binary용일 경우, 해당 메트릭에 필요한 기준값(<= 1); add_ids: True/False|list for add_ids=False, pandas dataframe for add_ids=True|inputs에 따라 다양한 방식으로 레이블 추출|
|`measure_pred_with_true`|pred_list: list of 추출된 레이블; mode: 'accuracy'/'mcc'|정확도 또는 mcc값|주어진 레이블과 실제 레이블 간의 비교값(성능)|


