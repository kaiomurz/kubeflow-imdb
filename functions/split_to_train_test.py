import kfp.components as comp

def split_to_train_test(
    in_X_pkl: comp.InputPath('PKL'),
    in_y_pkl: comp.InputPath('PKL'),
    out_X_train_pkl: comp.OutputPath('PKL'),
    out_X_test_pkl: comp.OutputPath('PKL'),
    out_y_train_pkl: comp.OutputPath('PKL'),
    out_y_test_pkl: comp.OutputPath('PKL'),
    log_log: comp.OutputPath('LOG'),
    split: float
    ):

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
  
    # check to see if X and y are of same length

    X = pickle.load(open(in_X_pkl, 'rb'))
    y = pickle.load(open(in_y_pkl, 'rb'))
   
    split_index = int(split*len(y))    
    X_train = X[:split_index]
    X_test = X[split_index:]
    print_and_log('X split')
    y_train = y[:split_index]
    y_test = y[split_index:]
    print_and_log('y split')

    for obj, file_name in zip(
        [X_train, y_train, X_test, y_test],
        [out_X_train_pkl, out_y_train_pkl, out_X_test_pkl, out_y_test_pkl]
        ):
        print(obj, type(obj), "\n")#, obj[0], "\n\n")
        pickle.dump(obj, open(file_name,'wb'))
    print_and_log('objects pickled')