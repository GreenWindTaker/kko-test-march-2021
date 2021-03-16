from tensorflow.keras.layers import Input, Conv1D, Dense, Flatten
from tensorflow.keras.models import Model, save_model


class training(object):
    def __init__(self):
        pass

    def setModel(self):
        input_layer = Input(shape=(4, 1))

        conv1 = Conv1D(filters=32, kernel_size=4, padding='same', activation='relu')(input_layer)
        conv2 = Conv1D(filters=16, kernel_size=4, padding='same', activation='relu')(conv1)

        pooling = Flatten()(conv2)

        dense_1 = Dense(8, activation='relu')(pooling)
        dense_2 = Dense(4, activation='relu')(dense_1)

        classifier = Dense(3, activation='softmax')(dense_2)

        __model = Model(input_layer, classifier)

        __model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return __model

    def runTrain(self, model, trainX, trainY, evalX, evalY, validX, validY, savepath=None):
        # Callback은 tensorlog를 이용하여 구성하나, 추가로
        history_callback = model.fit(trainX, trainY,
                                     epochs=1000,
                                     verbose=0,
                                     validation_data=(evalX, evalY))

        if savepath != None:
            __Save_model = save_model(model, filepath=savepath)

        score = model.evaluate(validX, validY, verbose=0)

        print('Valid loss :' + str(score[0]))
        print('Valid accuracy:' + str(score[1]))
