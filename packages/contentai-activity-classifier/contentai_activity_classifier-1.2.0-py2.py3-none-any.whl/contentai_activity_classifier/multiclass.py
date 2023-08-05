import numpy as np
import h5py
import pandas as pd
from sklearn.metrics import confusion_matrix, fbeta_score, accuracy_score, classification_report
from sklearn.metrics import roc_curve, auc, precision_recall_fscore_support, roc_auc_score
from sklearn.metrics import average_precision_score, precision_recall_curve
from sklearn.preprocessing import normalize, minmax_scale
from sklearn.model_selection import cross_validate, cross_val_predict
import os
import json




def create_model (config):
    from pydoc import locate
    print (f"Creating model:  {config['estimator']}")
    print (f"    parameters:  {config['est_params']}")
    model_type = locate(config['estimator'])
    init = json.loads(config['est_params'])
    xmodel = model_type(**init)
    return xmodel



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m', '--model_path', type=str, default='', help="specify where the model should be written")
    parser.add_argument('--framework', type=str, default='sklearn', help="model framework e.g. sklearn, keras, etc")
    parser.add_argument('--estimator', type=str, default='sklearn.linear_model.LogisticRegression', help='specify the estimator to use')
    parser.add_argument('--est_params', type=str, default='{}', help='estimator parameters')
    #parser.add_argument('--est_params', type=str, default='{"C":4.0,"random_state":0,"max_iter":500,"class_weight":"balanced","solver":"lbfgs"}', help='estimator parameters')
    parser.add_argument('-j', '--jobs', type=int, default=-1, help='how many cpus to use for cross_val_predict (-1 means all)')
    parser.add_argument('-f', '--folds', type=int, default=10, help='how many folds to use for cross_val_predict')
    parser.add_argument('--method', type=str, default='predict_proba', help='the prediction method to use')
    parser.add_argument('--mode', choices=['audio', 'video', 'audvid'], default='audio', help='feature modality')
    parser.add_argument('--adjust_probs', default=False, action='store_true', help='normalize probabilities')
    parser.add_argument('-o', '--output_dir', type=str, default=None, help='where to write output files')
    #parser.add_argument('-d', '--data_type', type=str, default='Generic', help='input data format')
    parser.add_argument('-l', '--label_path', type=str, required=True, help='relative path for input label (simple txt, one line or Labelstudio JSON)')
    parser.add_argument('-v', '--vidfeat_path', type=str, default='', help='relative path for video features')
    parser.add_argument('-a', '--audfeat_path', type=str, default='', help='relative path for audio features')
    parser.add_argument('--col_id', default=0, help='name or index of the ID column in the label file')
    parser.add_argument('--col_label', default=1, help='name or index of the label column in the label file')



    config = vars(parser.parse_args())
    print ("Using parameters:", config)

    model = create_model(config)

    '''
    if config['data_type'] == 'UGC':
        from ugc_loader import UGC_DataLoader
        loader = UGC_DataLoader()
    elif config['data_type'] == 'Popcorn':
        from popcorn_loader import PopcornDataLoader
        loader = PopcornDataLoader(mode=config['mode'])
    elif config['data_type'] == 'Generic':
    '''
    from data_loader import GenericDataLoader
    loader = GenericDataLoader(**{k:config[k] for k in ['label_path','vidfeat_path','audfeat_path','col_id','col_label']})
    train_X, train_Y, paths = loader.load_XY_paths()

    print ("Starting cross validation")
    list_classes = sorted(set(train_Y))
    probs = cross_val_predict(model, train_X, train_Y, cv=config['folds'], n_jobs=config['jobs'], method=config['method'])  #predict_proba')
    print ("Done!")

    pred_y = np.argmax(probs, -1)
    pred_y = [list_classes[x] for x in pred_y]
    test_Y = train_Y
    pred = pred_y

    class_performance = {}
    class_performance['performance'] = {}

    try:
        print (classification_report(test_Y, pred_y))
    except Exception as err:
        print ("classification_report:", err)

    try:
        f1 = fbeta_score(test_Y, pred_y, beta=1, average='micro')
        acc = accuracy_score(test_Y, pred_y)
        print(f'f-score: {f1}, accuracy score: {acc}')
    except Exception as err:
        print ("f1/acc:", err)

    try:
        CM = confusion_matrix(train_Y, pred_y, labels=None, sample_weight=None)
        print (CM)
        class_performance['confusion_matrix'] = str(CM)
    except Exception as err:
        print ("confusion_matrix:", err)

    try:
        precision, recall, fbeta_score, _ = precision_recall_fscore_support(test_Y, pred, average=None, labels=None, sample_weight=None)
        class_performance['performance']['precision'] = precision
        class_performance['performance']['recall'] = recall
        class_performance['performance']['f1'] = fbeta_score
    except Exception as err:
        print ("precision_recall_fscore_support:", err)

    try:
        class_performance['performance']['ap'] = average_precision_score(test_Y, pred)
    except Exception as err:
        print ("average_precision_score:", err)

    try:
        class_performance['report'] = classification_report(test_Y, pred, output_dict=True)
    except Exception as err:
        print ("classification_report B:", err)

    try:
        fpr, tpr, thresholds = roc_curve(test_Y, probs)
        roc_auc = auc(fpr, tpr)
        class_performance['performance']['auc'] = roc_auc
    except Exception as err:
        print ("roc_curve/auc:", err)

    try:
        if config['adjust_probs']:
            from sklearn.preprocessing import MinMaxScaler
            mms = MinMaxScaler()
            zz = mms.fit_transform(probs)
            probs = [aa/sum(aa) for aa in zz]
        class_performance['performance']['roc_auc_score'] = roc_auc_score(test_Y, probs, average='macro', multi_class='ovr')
    except Exception as err:
        print ("roc_auc_score:", err)

    try:
        class_performance['performance']['accuracy_score'] = accuracy_score(test_Y, pred)
    except Exception as err:
        print ("accuracy_score:", err)

    if config['output_dir'] is not None:
        from pathlib import Path
        import pickle
        path_out = Path(config['output_dir'])
        if not path_out.exists():
            path_out.mkdir(parents=True)
            print ("Created path:", path_out)
        path_perform = path_out / Path('performance.pkl')
        with path_perform.open(mode='wb') as fp:
            pickle.dump (class_performance, fp)
    else:
        print (class_performance)

