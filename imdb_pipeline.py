
import imp
import kfp
import kfp.components as comp


######################################
########## IMPORT FUNCTIONS ##########
######################################

from functions.download_and_save_data import download_and_save_data_from_s3
from functions.shuffle import shuffle
from functions.split_to_x_y import split_to_x_y
from functions.encode_target import encode_target
from functions.clean_text import clean_text
from functions.preprocess_text import preprocess_text
from functions.split_to_train_test import split_to_train_test
from functions.create_and_train_model import create_and_train_model
from functions.create_and_save_performance_artifacts import create_and_save_performance_artifacts

# dsl-compile --py imdb_pipeline.py --output imdb_pipeline.yaml
# https://github.com/kubeflow/pipelines/tree/sdk/release-1.8/samples/core


#####################################################
########## CONVERT FUNCTIONS TO COMPONENTS ##########
#####################################################

base_image = "kaiomurz/kubeflow-imdb:latest"

download_and_save_data_from_s3_op = kfp.components.create_component_from_func(
    download_and_save_data_from_s3,
    base_image=base_image
)

shuffle_op = kfp.components.create_component_from_func(
    shuffle,
    base_image=base_image
)

split_to_x_y_op = kfp.components.create_component_from_func(
    split_to_x_y,
    base_image=base_image
)

encode_target_op = kfp.components.create_component_from_func(
    encode_target,
    base_image=base_image
)

clean_text_op = kfp.components.create_component_from_func(
    clean_text,
    base_image=base_image
)

preprocess_text_op = kfp.components.create_component_from_func(
    preprocess_text,
    base_image=base_image
)

split_to_train_test_op = kfp.components.create_component_from_func(
    split_to_train_test,
    base_image=base_image    
)
create_and_train_model_op = kfp.components.create_component_from_func(
    create_and_train_model,
    base_image=base_image
)
create_and_save_performance_artifacts_op = kfp.components.create_component_from_func(
    create_and_save_performance_artifacts,
    base_image=base_image
)

# test_pickling_op = kfp.components.create_component_from_func(
#     test_pickling,
#     base_image=base_image
# )
# pickle_load_test_op = kfp.components.create_component_from_func(
#     pickle_load_test,
#     base_image=base_image
# )
# split_to_train_test_op = kfp.components.create_component_from_func(
#     split_to_train_test,
#     base_image=base_image
# )



###########################################
########## CREATING THE PIPELINE ##########
###########################################


@kfp.dsl.pipeline(
    name='imdb_pipeline',
    description='Pipeline to train and serve sentiment analysis model on IMDB dataset'
)
def imdb_pipeline(
    aws_access_key_id: str,
    aws_secret_access_key: str,
    Bucket: str='imdb-kubeflow',
    Key: str='data.csv',
    y_heading: str='sentiment',
    tokenizer_num_words: int=1000,
    shuffle: bool=True,
    split: float = 0.8,
    fraction: float=0.1,
    num_epochs: int=10
    ):

    download_and_save_data_from_s3_task = download_and_save_data_from_s3_op(
        Bucket, 
        Key,
        aws_access_key_id,
        aws_secret_access_key
    )

    shuffle_task = shuffle_op(
        download_and_save_data_from_s3_task.outputs['data_csv'],
        shuffle,
        fraction
    )

    split_to_x_y_task = split_to_x_y_op(
        shuffle_task.outputs['out_data_csv'],
        y_heading
    )

    encode_target_task = encode_target_op(
        split_to_x_y_task.outputs['out_y_csv']
    )

    clean_text_task = clean_text_op(
        split_to_x_y_task.outputs['out_X_csv']        
    )

    preprocess_text_task = preprocess_text_op(
        clean_text_task.outputs['out_X_csv'],
        tokenizer_num_words
    )
    split_to_train_test_task = split_to_train_test_op(
        preprocess_text_task.outputs['out_X_pkl'],
        encode_target_task.outputs['out_y_pkl'],
        split
    )
    create_and_train_model_task = create_and_train_model_op(
        split_to_train_test_task.outputs['out_X_train_pkl'],
        split_to_train_test_task.outputs['out_y_train_pkl'],
        tokenizer_num_words,
        num_epochs
    )
    create_and_save_performance_artifacts_task = create_and_save_performance_artifacts_op(
        create_and_train_model_task.outputs['model_pkl'],
        split_to_train_test_task.outputs['out_X_test_pkl'],
        split_to_train_test_task.outputs['out_y_test_pkl']
    )

    # test_pickling_task = test_pickling_op(
    #     split_to_train_test_task.outputs['out_X_train_pkl'],
    #     split_to_train_test_task.outputs['out_y_train_pkl'],
    #     split_to_train_test_task.outputs['out_X_test_pkl'],
    #     split_to_train_test_task.outputs['out_y_test_pkl']
    # )

    # pickle_load_test_task = pickle_load_test_op(
    #     preprocess_text_task.outputs['out_X_pkl']
    # )
    # split_to_train_test_task = split_to_train_test_op(
    #     download_and_save_data_from_s3_task.outputs['data_csv'],
    #     split=0.8,
    #     shuffle=True  
    # )

    # def pickle_load_test(
#     in_X_pkl: comp.InputPath('PKL')
#     ):
#     import pickle
#     X = pickle.load(open(in_X_pkl, 'rb'))    
    

# def test_pickling(
#     in_X_train_pkl: comp.InputPath('PKL'),
#     in_y_train_pkl: comp.InputPath('PKL'),
#     in_X_test_pkl: comp.InputPath('PKL'),    
#     in_y_test_pkl: comp.InputPath('PKL')
#     ):
#     import pickle
#     import numpy

#     X_train = pickle.load(open(in_X_train_pkl, 'rb'))
#     y_train = pickle.load(open(in_y_train_pkl, 'rb'))
#     X_test = pickle.load(open(in_X_test_pkl, 'rb'))
#     y_test = pickle.load(open(in_y_test_pkl, 'rb'))

#     objs = {
#         'X train':X_train,
#         'y train': y_train,
#         'X test': X_test,
#         'y test': y_test
#         }

#     for obj in objs:
#         print(obj, type(objs[obj]), objs[obj].shape, "\n")
        
#         for i in range(3):
#             print(objs[obj][i], "\n")
#         print("#####################################################, \n\n\n")    
