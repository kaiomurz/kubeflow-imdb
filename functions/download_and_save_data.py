import kfp.components as comp

def download_and_save_data_from_s3(
    Bucket: str,
    Key: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    data_csv: comp.OutputPath('CSV'),
    log_log: comp.OutputPath('LOG')
    ):

    import boto3
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
    
    # create s3 connection
    s3 = boto3.client(
        's3', 
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
        )
    print_and_log('S3 connection established')

    # download file
    s3.download_file(Bucket, Key, data_csv)

    print_and_log('data downloaded to S3')