import kfp.components as comp

def preprocess_text(
    in_X_csv: comp.InputPath('CSV'),
    out_X_pkl: comp.OutputPath('PKL'),
    log_log: comp.OutputPath('LOG'),
    tokenizer_num_words: int
    ):
    import pandas as pd
    from keras.preprocessing.text import Tokenizer
    from keras.preprocessing.sequence import pad_sequences
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


    tokenizer_num_words = int(tokenizer_num_words)
    X = pd.read_csv(in_X_csv)    
    # tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=tokenizer_num_words, oov_token='<OOV>')
    tokenizer = Tokenizer(num_words=tokenizer_num_words, oov_token='<OOV>')
    tokenizer.fit_on_texts(X['review'])
    print_and_log('tokenizer fit complete')
    sequences = tokenizer.texts_to_sequences(X['review'])
    print_and_log('text-to-sequences complete')
    padded = pad_sequences(sequences, padding='post', maxlen=750)
    print_and_log('padding complete')
    print(padded[0])
    pickle.dump(padded, open(out_X_pkl, 'wb'))
