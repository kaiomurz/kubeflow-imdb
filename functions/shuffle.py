import kfp.components as comp


def shuffle(
    in_data_csv: comp.InputPath('CSV'),
    out_data_csv: comp.OutputPath('CSV'),
    log_log: comp.OutputPath('LOG'),
    shuffle: bool,
    fraction: float    
    ):

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

    df = pd.read_csv(in_data_csv)

    print_and_log('data read')

    if shuffle:
        df = df.sample(frac=1)
        df = df.reindex(range(df.shape[0]))
        print_and_log('shuffle complete')

    end_index = int(fraction* df.shape[0])
    df = df[:end_index]
    print_and_log('fraction of dataset extracted')
    df.to_csv(out_data_csv, index=False)