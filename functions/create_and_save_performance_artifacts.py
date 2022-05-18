import kfp.components as comp


def create_and_save_performance_artifacts(
    model_pkl: comp.InputPath('PKL'), 
    X_test_pkl: comp.InputPath('PKL'), 
    y_test_pkl: comp.InputPath('PKL'),
    confusion_matrix_pkl: comp.OutputPath('PKL'),
    log_log: comp.OutputPath('LOG')
    ):

    import pickle
    from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
    import seaborn as sns
    import numpy as np
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

    model = pickle.load(open(model_pkl, 'rb'))
    X_test = pickle.load(open(X_test_pkl, 'rb'))
    y_test = pickle.load(open(y_test_pkl,'rb'))

    print_and_log('pickled artifacts loaded')

    
    y_pred = model.predict(X_test)
    
    def encode(x):
        if x > 0.5:
            return 1
        else: 
            return 0
    def categorise(x):
        if x == 1:
            return 'positive'
        else:
            return 'negative'
        
    v_encode = np.vectorize(encode)
    v_categorise = np.vectorize(categorise)
    y_pred = v_encode(y_pred).reshape(y_test.shape)
    
    y_test_categorised = v_categorise(y_test)
    y_pred_categorised = v_categorise(y_pred)
    
    print_and_log('encoding of test data complete')

    metrics = {
        'Accuracy':accuracy_score(y_test, y_pred),
        'Precision':precision_score(y_test, y_pred),
        'Recall':recall_score(y_test, y_pred)
    }
    
    
    print(f"Accuracy:\t{metrics['Accuracy']:.2f}")
    print(f"Precision:\t{metrics['Precision']:.2f}")
    print(f"Recall:\t\t{metrics['Recall']:.2f}")
    
    print_and_log(f"Accuracy:\t{metrics['Accuracy']:.2f}")
    print_and_log(f"Precision:\t{metrics['Precision']:.2f}")
    print_and_log(f"Recall:\t\t{metrics['Recall']:.2f}")

    
    confusion_matrix = confusion_matrix(y_test_categorised, y_pred_categorised, labels=['positive', 'negative'])
    print("Confusion matrix", confusion_matrix)
    
    pickle.dump(confusion_matrix, open(confusion_matrix_pkl,'wb'))
    # confusion_matrix = sns.heatmap(confusion_matrix_data/np.sum(confusion_matrix_data), annot=True, fmt='.2%')
