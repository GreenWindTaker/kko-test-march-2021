'''
첨부 데이터(problem5.csv)를 이용해 예측합니다.
'''

from test_05.services.preprocessing import preprocessing
from test_05.services.train import training
import pprint as pp


def train_and_valid():
    '''
    Tensorflow (with Keras) 기반으로 코드 구성.
    tensorflow ==2.4.1
    keras == 2.4.3
    pandas ==1.2.2
    '''
    print("Train and Run")

    datset_filepath = "./resources/dataset/problem5.csv"
    model_save_path = "./resources/model/sample.h5"

    mPreprocessing = preprocessing()
    __x, __y = mPreprocessing.loading_dataset(datset_filepath, 'species', True)

    pp.pprint(__x)
    pp.pprint(__y)

    (trainX, trainY), (evalX, evalY), (validX, validY) = mPreprocessing.split(__x, __y)

    mTraining = training()
    __model = mTraining.setModel()

    print(__model.summary())

    mTraining.runTrain(__model, trainX, trainY, evalX, evalY, validX, validY, model_save_path)
    print("Done")


if __name__ == "__main__":
    train_and_valid()
