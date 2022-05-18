import kfp.components as comp

def encode_target(
    in_y_csv: comp.InputPath('CSV'),
    out_y_pkl: comp.OutputPath('PKL'),
    log_log: comp.OutputPath('LOG')
    ):
    from sklearn.preprocessing import LabelEncoder
    import pandas as pd
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

    y = pd.read_csv(in_y_csv)

    encoder = LabelEncoder()
    encoded_y = pd.Series(encoder.fit_transform(y))
    print_and_log('target encoded')
    pickle.dump(encoded_y, open(out_y_pkl, 'wb'))