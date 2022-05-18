import kfp.components as comp

def split_to_x_y(
    in_data_csv: comp.InputPath('CSV'),
    out_X_csv: comp.OutputPath('CSV'),
    out_y_csv: comp.OutputPath('CSV'),
    log_log: comp.OutputPath('LOG'),
    y_heading: str
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
    y = df[y_heading].copy()
    X = df.drop(y_heading, axis=1)
    print_and_log('split completed')
    X.to_csv(out_X_csv, index=False)
    y.to_csv(out_y_csv, index=False)
