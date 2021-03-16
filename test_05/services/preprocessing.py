import pandas as pd  # Dataset loading을 위하여
import numpy as np
import json


class preprocessing(object):
    '''
    Datset이 작아서 한꺼번에 전처리 및 학습, 평가 Dataset 생성
        - 대용량으로 처리하는 경우, Generator 사용하여 일정 batch로 생성진행
        - labeling은 sparse data로 생성하여 판단 진행. 혹은 미리 정해진 category 정보를 확인하고
        classfier용 category 생성
    '''

    def __init__(self):
        self.category_tokenizer = None
        self.num_of_category = 0
        self.num_of_datset = 0


    def loading_dataset(self, filepath, category="species", shuffle=True):
        __readDf = pd.read_csv(filepath)

        if shuffle == True:
            __readDf = __readDf.sample(frac=1)
            __readDf = __readDf.reset_index(drop=True)

        __header = __readDf.columns.tolist()
        __header.remove(category)
        __X_header = __header

        self.num_of_datset = len(__readDf.index)
        print("Total Dataset Num = " + str(self.num_of_datset))

        __X = __readDf[__X_header]
        __Y = __readDf[category]

        # 카테고리 편중 확인
        print(__Y.value_counts())

        # Check Category
        self.__set_category(__Y)

        return __X, __Y

    def __set_category(self, category_series):
        self.category_tokenizer = dict()
        __unique_list = sorted(category_series.unique().tolist())
        for idx, val in enumerate(__unique_list):
            self.category_tokenizer[val] = idx
        self.num_of_category = len(__unique_list)

    def __gen_category(self, species):
        zeros = np.zeros(self.num_of_category)
        __get_category = self.category_tokenizer.get(species)
        (zeros)[__get_category] = 1

        return zeros


    def split(self, X, Y, train=0.6, eval=0.3, valid=0.1):

        __train_idx_end = int(self.num_of_datset * train)
        __eval_idx_end = __train_idx_end + int(self.num_of_datset * eval)

        __numpy_X = X.to_numpy()
        __numpy_Y = np.zeros((150, 3))

        for row, val in enumerate(Y.values.tolist()):
            __get_category = self.category_tokenizer.get(val)
            (__numpy_Y[row])[__get_category] = 1

        __numpy_X = __numpy_X.reshape(self.num_of_datset, 4)
        __numpy_Y = __numpy_Y.reshape(self.num_of_datset, 3)

        __train_X = __numpy_X[:__train_idx_end]
        __train_Y = __numpy_Y[:__train_idx_end]

        __eval_X = __numpy_X[__train_idx_end:__eval_idx_end]
        __eval_Y = __numpy_Y[__train_idx_end:__eval_idx_end]

        __valid_X = __numpy_X[__eval_idx_end:]
        __valid_Y = __numpy_Y[__eval_idx_end:]

        return (__train_X, __train_Y), (__eval_X, __eval_Y), (__valid_X, __valid_Y)

    def save_category_classifier(self, file_path):
        if file_path != None:

            try:
                with open(file_path, 'w') as filedata:
                    json.dump(self.category_tokenizer, filedata)
            except Exception as e:
                print(str(e))

