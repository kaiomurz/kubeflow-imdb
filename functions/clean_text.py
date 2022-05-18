import kfp.components as comp

def clean_text(
    in_X_csv: comp.InputPath('CSV'),
    out_X_csv: comp.OutputPath('CSV'),
    log_log: comp.OutputPath('LOG')
    ):
    print("clean_text")
    import pandas as pd
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


    X = pd.read_csv(in_X_csv)
    sentences = []

    for sentence in X['review']:
        #remove line breaks and change to lower case
        sentence = sentence\
            .replace('<br /><br />', ' ')\
            .lower()
        
        sentences.append(sentence)
    print_and_log('text cleaned')
    X = pd.DataFrame({'review':sentences})
    X.to_csv(out_X_csv, index=False)