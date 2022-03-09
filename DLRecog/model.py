from keras.models import Sequential
from keras.layers import Conv2D, Dense, BatchNormalization, AveragePooling2D, Flatten, Dropout
from sklearn.model_selection import train_test_split


class RecogModel:
    def __init__(self, input_shape, output_shape):
        self.model = Sequential([
            Conv2D(16, (4, 4), padding="same",
                   activation="sigmoid", input_shape=input_shape),
            Conv2D(32, (4, 4), padding="same", activation="sigmoid"),
            Conv2D(32, (4, 4), padding="same", activation="sigmoid"),

            BatchNormalization(),
            Dropout(0.2),
            AveragePooling2D((2, 2)),

            Conv2D(32, (2, 2), padding="same", activation="sigmoid"),
            Conv2D(32, (2, 2), padding="same", activation="sigmoid"),
            Conv2D(64, (2, 2), padding="same", activation="sigmoid"),

            BatchNormalization(),
            Dropout(0.2),
            AveragePooling2D((4, 4)),

            Flatten(),
            Dense(16, activation="sigmoid"),
            Dense(16, activation="sigmoid"),
            Dense(16, activation="sigmoid"),

            Dropout(0.2),

            Dense(32, activation="sigmoid"),
            Dense(32, activation="sigmoid"),
            Dense(output_shape, activation="softmax")
        ])
        self.hist = None

    def compileModel(self, optimizer_func="adam", loss_func="categorical_crossentropy"):
        self.model.compile(optimizer=optimizer_func,
                           loss=loss_func,
                           metrics=["accuracy"])

    def fitModel(self, trainX, trainY, testY, testX, batch_size=16, epochs=10, train_val_ratio=0.2):
        trainX, valX, trainY, valY = train_test_split(
            trainX, trainY, test_size=train_val_ratio, shuffle=True)
        self.hist = self.model.fit(trainX, trainY, batch_size=batch_size,
                                   verbose=1, epochs=epochs, validation_data=(valX, valY))

    def testModel(self, testX, testY, batch_size=16):
        self.model.evaluate(testX, testY, batch_size=batch_size, verbose=1)

    def saveModel(self, model_name="RecogModel.h5"):
        self.model.save(model_name)
