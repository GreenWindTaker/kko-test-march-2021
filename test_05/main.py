'''
첨부 데이터(problem5.csv)를 이용해 예측합니다.
Tensorflow (with Keras) 기반으로 코드 구성.

python == 3.7.7
tensorflow == 2.4.1
keras == 2.4.3
pandas == 1.2.2

'''

from test_05.services.preprocessing import preprocessing
from test_05.services.train import training
from test_05.services.prediction import prediction
import numpy as np
from tensorflow.keras.backend import clear_session


def run_train():
    '''

    '''

    print("Train and Run")
    clear_session()

    dataset_filepath = "./resources/dataset/problem5.csv"
    model_save_path = "./resources/model/sample.h5"
    category_classifier_path = "./resources/model/category_classifier.json"

    # Data 전처리
    mPreprocessing = preprocessing()
    __x, __y = mPreprocessing.loading_dataset(dataset_filepath, 'species', True)
    mPreprocessing.save_category_classifier(category_classifier_path)

    # 학습 진행 및 평가를 위한 dataset 분배
    (trainX, trainY), (evalX, evalY), (validX, validY) = mPreprocessing.split(__x, __y)

    mTraining = training()
    __model = mTraining.setModel()

    # 모델 구성 확인
    print(__model.summary())

    mTraining.runTrain(__model, trainX, trainY, evalX, evalY, validX, validY, model_save_path)
    print("Done")


def run_prediction():
    print("Prediction Test")
    clear_session()

    dataset_filepath = "./resources/dataset/problem5.csv"
    model_save_path = "./resources/model/sample.h5"
    category_classifier_path = "./resources/model/category_classifier.json"

    # Data 전처리
    mPreprocessing = preprocessing()

    # 일부 학습데이터가 섞일수도 있으나, 전체적인 shuffle 구성으로 테스트.
    __x, __y = mPreprocessing.loading_dataset(dataset_filepath, 'species', True)
    (trainX, trainY), (evalX, evalY), (validX, validY) = mPreprocessing.split(__x, __y)

    # Prediction 진행
    mPrediction = prediction()
    mPrediction.load_model(model_save_path)
    mPrediction.load_classifier(category_classifier_path)

    for (__cache_X, __cache_Y) in zip(validX, validY):
        __input_tensor = np.expand_dims(__cache_X, axis=0)
        __corr_output = np.expand_dims(__cache_Y, axis=0)
        __res = mPrediction.prediction(__input_tensor, False)

        print("Input Tensor : " + str(__input_tensor))
        print("Prediction Value : " + str(__res) + " / Labeling " + str(mPrediction.labeling(__res)))
        print("Real Value : " + str(__corr_output) + " / Labeling " + str(mPrediction.labeling(__corr_output)))
        print("-" * 15)

    print("Done")


if __name__ == "__main__":
    # run_train()
    run_prediction()
