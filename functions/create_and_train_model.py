import kfp.components as comp

def create_and_train_model(
    in_X_train_pkl: comp.InputPath('PKL'),
    in_y_train_pkl: comp.InputPath('PKL'),
    history_pkl: comp.OutputPath('PKL'),
    model_pkl: comp.OutputPath('PKL'),
    log_log: comp.OutputPath('LOG'),
    tokenizer_num_words: int,
    num_epochs:int
    ):
    import keras
    import pickle
    import logging

    logging.basicConfig(
        filename=log_log,
        filemode='w',
        level=logging.DEBUG,
        format='%(levelname)s: %(message)s'
        )

    def print_and_log(message):
        print(message)
        logging.info(message)


    X_train = pickle.load(open(in_X_train_pkl, 'rb'))
    y_train = pickle.load(open(in_y_train_pkl, 'rb'))

    vocab_size = tokenizer_num_words
    seq_length = X_train.shape[1]
    embedding_dim = 100

    model = keras.Sequential([
    keras.layers.Embedding(vocab_size, embedding_dim, input_length=seq_length),
    keras.layers.Bidirectional(keras.layers.LSTM(64)),
    keras.layers.Dense(24, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
    ])
    
    print_and_log('model instantiated')
    
    # compile model

    model.compile(loss='binary_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])
    print_and_log('model compiled')
    # model summary
    print(model.summary())

    history = model.fit(X_train, y_train, 
                    epochs=num_epochs, verbose=1, 
                    validation_split=0.1)
    print_and_log('training complete')
    #pickle history and model
    pickle.dump(history, open(history_pkl, 'wb'))
    pickle.dump(model, open(model_pkl, 'wb'))