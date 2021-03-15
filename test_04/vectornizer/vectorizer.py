import pandas as pd     # Pandas 이용하여 dtype 판별 및 non-numeric 값에 대한 tokenizer 생성
import pprint as pp     # 디버깅용
import json             # 생성된 tokenizer를 json으로 저장하기 위하여
import numpy as np      # input vector로 생성하기 위하여 numpy 이용.


class Vectorizer(object):
    def __init__(self):
        self.tokenizer = None
        self.readed_df = None

    def fit(self, input_file, save_path=None):
        '''
        Datset이 크지 않음을 가정하고 설계.
            - 실제로 큰 경우, 정렬된 tokenzier를 사용하지 않고
            csv를 chunk로 읽은 이후, row by row의 unique한 값을 나타나는 순서에 의하여 정해지도록 설계한다.
        '''

        print("Fitting to Vectorize")

        if input_file == None:
            input_file = "./resources/problem4.csv"

        __readed_DF = pd.read_csv(input_file)

        # CSV 로딩 디버깅용
        pp.pprint(__readed_DF.head(4))

        __header = __readed_DF.columns

        __tokenizer_inform = dict()

        for __col in __header:
            print("Check Unique Values " + str(__col))

            __cache_series = __readed_DF[__col]

            # dataset의 column name이 중복되지 않는다는 전제하에 진행.
            __tokenizer_inform[__col] = dict()

            # Numeric Data인 경우, tokenizer 생성 없이 값 그대로 사용.
            __flag = pd.api.types.is_numeric_dtype(__cache_series)
            __tokenizer_inform[__col]['numeric'] = __flag

            '''
            Non-Numeric Data인 경우, pandas의 series에 대한 unique값을 확인하고.
            이를 정렬한 tokenizer를 생성하여 vectorize 진행.
            
                - 입력 Dataset에 대한 특별한 전처리 없음이 생성하였음.
                    ex : 대소문자 일괄통일, 띄어쓰기 보정, 한자 및 특수기호 제거
                    
                - 위에 언급하였듯이, 대용량 파일 처리를 위해서는 pandas의 chunk를 이용하여 batch 처리를 진행하며
                이때 생성하는 tokenizer는 정렬없이 언급되는 순서에 의하여 index가 정해짐.
                --> 이때도 hashmap을 이용하자.
                
                - Numeric 및 non-numeric 에 대한 확인이 어려우므로, 이는 이미 사전에 정의를 진행하고,
                혹시 모를 error값을 제거하기 위하여 각 row by row의 처리를 진행할때, 확인을 한다.
                --> generater를 이용하여 생성과 동시에 데이터 처리를 진행해도 될듯.
            '''

            if __flag == False:
                __cache_info = dict()
                __unique_list = sorted(__cache_series.unique().tolist())

                for idx, val in enumerate(__unique_list):
                    __cache_info[val] = idx
                __tokenizer_inform[__col]['tokenizer'] = __cache_info

        # Debug 차원에서 fitting이 완료된 정보를 확인
        pp.pprint(__tokenizer_inform)

        self.tokenizer = __tokenizer_inform

        # Tokenzier를 저장하는 경우
        if save_path != None:

            try:
                with open(save_path, 'w') as filedata:
                    json.dump(__tokenizer_inform, filedata)
            except Exception as e:
                print(str(e))

    def generate(self, input_file, shuffle=False):

        if self.tokenizer == None:
            print("Tokenizer가 정의되지 않았습니다. Tokenizer 정의를 진행합니다.")
            self.fit(input_file)

        __readed_df = pd.read_csv(input_file)
        if shuffle == True:
            __readed_df = __readed_df.sample(frac=1)

        for __, row in __readed_df.iterrows():
            _vectorize = self.__vector_gen(row)

            yield _vectorize
        return None

    def __vector_gen(self, row):
        __array_list = list()
        for __col in self.tokenizer:
            __numeric = self.tokenizer[__col].get('numeric')

            __val = row[__col]
            if __numeric == False:
                __tokenizer = self.tokenizer[__col].get('tokenizer')
                __num_val = __tokenizer.get(__val)
                __array_list.append(__num_val)
            else:
                __array_list.append(__val)

        # Numpy Array로 변환
        __np_array = np.array(__array_list)
        return __np_array
