import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, normalize
from sklearn.model_selection import cross_validate, cross_val_predict
import os
from os.path import isfile, join, exists
import h5py
import json
from sklearn.metrics import roc_curve, auc, precision_recall_fscore_support,confusion_matrix, classification_report
from sklearn.metrics import average_precision_score, precision_recall_curve
import pickle

import datetime
import re

import matplotlib.pyplot as plt
import wrapped


def create_model (config):
    from pydoc import locate
    print (f"Creating model:  {config['estimator']}")
    print (f"    parameters:  {config['est_params']}")
    model_type = locate(config['estimator'])
    init = json.loads(config['est_params'])
    xmodel = model_type(**init)
    return xmodel


def load_labels(filename, label_type=''):
    labels=[]
    seen_file = {}
    num_files = 0
    with open(filename, 'rt') as f:
        is_header = True
        for line in f:
            fields = line.strip().split('|')
            if is_header :
                is_header = False
                continue
            num_files += 1
            video_name = os.path.basename(fields[0]).replace(".mp4", "")
            if len(label_type)==0 or label_type=='binary-csv':
                label = int(fields[1])
                labels.append({'path': video_name, 'class': label})
            if label_type=='multi-csv':
                if video_name not in seen_file:  # first time to see this one?
                    seen_file[video_name] = len(labels)
                    labels.append({'path': video_name, fields[1]: 1})
                else:  # otherwise, append to existing
                    labels[seen_file[video_name]][fields[1]] = 1

    # convert from labels/text to binarized (int) instances)
    df = pd.DataFrame(labels).fillna(0).set_index('path', drop=True)
    print(list(df.columns))
    print(f"From {num_files} raw files, found {len(df)} (labaled) samples vs {len(labels)} (input file) samples with {len(list(df.columns))} unique classes")
    return df


def load_labels_json(label_dir):
    labels=[]

    # { "completions": [ { "id": 151001, "lead_time": 10.796,
    #     "result": [ { "from_name": "multiple", "id": "zua_TfRQ7b", "to_name": "video", "type": "choices", 
    #         "value": { "choices": [ "Bullet" ] } } ] } ],
    #   "data": { "path": "/clips/PromoMGMMakingofGOLDENEYE8o3vMnKqhLQ_clip_00072.mp4", "video": ... },
    #   "id": 151 }
    re_clean = re.compile(r"[^0-9A-Za-z_-]+")  # name filtering

    num_files = 0
    for f in os.listdir(label_dir):   # loop through all label dir
        path_label = join(label_dir, f)
        if isfile(path_label) and f.endswith(".json"):
            with open(path_label, 'rt') as j:
                dict_label = json.load(j)
                num_files += 1
                if 'data' in dict_label and 'completions' in dict_label:
                    obj_sample = {'path': re_clean.sub('', os.path.splitext(os.path.basename(dict_label['data']['path']))[0]) }
                    num_labels = 0
                    for completion_obj in dict_label['completions']:
                        if 'result' in completion_obj:
                            for label_obj in completion_obj['result']:
                                if 'value' in label_obj and 'choices' in label_obj['value']:
                                    for label_name in label_obj['value']['choices']:
                                        obj_sample[label_name] = 1
                                        num_labels += 1
                    labels.append(obj_sample)

                        # end labels
                    # end completions
                # valid completion
            # end json file

    # convert from labels/text to binarized (int) instances)
    df = pd.DataFrame(labels).fillna(0).set_index('path', drop=True)
    print(df.sum(axis=0))
    print(f"From {num_files} raw files, found {len(df)} vs {len(labels)} samples with {len(list(df.columns))} classes")
    return df


def load_feature(feature_dir):
    video_features = {}
    if feature_dir is None or not exists(feature_dir):   # invalid directory?
        return video_features
    re_clean = re.compile(r"[^0-9A-Za-z_-]+")  # name filtering

    if isfile(feature_dir):   # use the JSON directory to load
        feature_files = [feature_dir]
    else:
        feature_files = [join(feature_dir, f) for f in os.listdir(feature_dir) if isfile(join(feature_dir, f)) and f.endswith(".hdf5")]
    for file_path in feature_files:
        with h5py.File(file_path, "r") as f:
            for video_name in f.keys():
                feature = f[video_name][()]
                #if feature.shape and (feature.shape[0] > 1 or len(feature.shape) > 1):      # breaks if e.g. shape==(2048,)
                if feature.shape and len(feature.shape) > 1:
                    feature = np.mean(feature, axis=0)
                video_features[re_clean.sub('', video_name)] = feature
    if len(video_features):
        print(f"Loaded {len(video_features)} features with example dimensionality {video_features[list(video_features.keys())[0]].shape} (source '{feature_dir}') ")
    return video_features


def l2norm(x):
    return np.sqrt(x.dot(x))


def preprocess(df_labels, video_features={}, audio_features={}, class_name=None):
    targets=[]
    features=[]
    video_names=[]
    if class_name is None and df_labels is not None:   # need a class name, pull first?
        class_name = df_labels.columns[0]

    num_found = 0
    list_names = list(video_features.keys())
    if len(list_names) < 1:
        list_names = list(audio_features.keys())
    
    shape_test = None
    for video_name in list_names:
        new_label = 0.0
        vec = None
        if df_labels is not None and video_name in df_labels.index:
            new_label = df_labels.loc[video_name][class_name]
            num_found += 1
        if video_name in video_features:
            vec = video_features[video_name]
        if video_name in audio_features:
            audio_vec = audio_features[video_name]
            if vec is None:
                vec = audio_vec
            else:
                vec = vec * 1.0/l2norm(vec)
                audio_vec = audio_vec * 1.0/l2norm(audio_vec)
                vec = np.concatenate( (vec, audio_vec), axis=0 )
        if shape_test is not None and shape_test != vec.shape:
            print(f"Error: Vector size {vec.shape} inconsistent with prior {shape_test} (sample {video_name}")
        elif vec is not None:
            targets.append(new_label)
            video_names.append(video_name)
            features.append(vec)
            shape_test = vec.shape
    print(f"Associated {num_found} labels to {len(list_names)} audio/video features...")
    return np.array(targets, dtype='float32'), np.array(features, dtype='float32'), video_names


def check_dir(filename):
    from pathlib import Path
    parent_dir = Path(filename).parent
    if not parent_dir.exists():
        parent_dir.mkdir(parents=True)
        print ("Created path:", parent_dir)



def evaluate_class(config, train_labels, class_name, train_video_features, train_audio_features, 
                    test_labels=None, test_video_features=None, test_audio_features=None):
    class_performance = {}

    # stack featurees for training
    train_Y, train_X, train_clip_names = preprocess(train_labels, train_video_features, 
                                                    train_audio_features, class_name)
    class_performance['train_samples'] = train_Y

    #model = mymodel(C = config['model_cost'], random_state=0, max_iter=max_iter, class_weight='balanced', solver='lbfgs').fit(train_X, train_Y)
    trained = None

    # testing process (either from test features or as cross-validation)
    if (len(test_video_features) < 1 and len(test_audio_features) < 1) or test_labels is None:   # missing both test data sets
        model = create_model(config)
        test_Y = train_Y
        probs = cross_val_predict(model, train_X, train_Y, cv=config['folds'], n_jobs=config['jobs'], method=config['method'])  #predict_proba')
        model = None        # release memory
    else:   # both audio and video test data available
        if trained is None:
            trained = create_model(config).fit(train_X, train_Y)
        test_Y, test_X, test_clip_names = preprocess(test_labels, test_video_features, test_audio_features, class_name)
        probs = getattr(trained, config['method'])(test_X)

    if len(config['model_path']):   # save model as well?
        if trained is None:
            trained = create_model(config).fit(train_X, train_Y)
        path_model = join(config['base_path'], f"{config['model_path']}-{class_name}.pkl")
        print(f"Saving created model to the specified path '{path_model}'.")
        check_dir (path_model)
        if config['framework'] == 'sklearn':
            with open(path_model, 'wb') as f:
                pickle.dump(trained, f)
        elif config['framework'] == 'wrapped':
            wrapped.write_model (trained, path_model)
        else:
            print ("ERROR:  Can't save model with framework '%s'" % config['framework'])
        class_performance['path'] = path_model

    # convert from probability to predictions
    if len(probs.shape) > 1:
        probs = probs[:,1]
    pred = probs.copy()
    pred[pred >= 0.5] = 1
    pred[pred < 0.5] = 0

    CM = confusion_matrix(test_Y, pred, labels=None, sample_weight=None)
    class_performance['confusion_matrix'] = str(CM)
    precision, recall, fbeta_score, _ = precision_recall_fscore_support(test_Y, pred, average='binary', labels=None, sample_weight=None)
    class_performance['performance'] = {}

    class_performance['performance']['precision'] = precision
    class_performance['performance']['recall'] = recall
    class_performance['performance']['f1'] = fbeta_score
    class_performance['performance']['ap'] = average_precision_score(test_Y, pred)

    # print('precision: {} recall: {}  f_score: {}'.format(precision, recall, fbeta_score)) 
    # print(classification_report(test_Y, pred))
    class_performance['report'] = classification_report(test_Y, pred, output_dict=True)

    fpr, tpr, thresholds = roc_curve(test_Y, probs)
    roc_auc = auc(fpr, tpr)
    # print('roc_auc is: %s' % roc_auc)
    class_performance['performance']['auc'] = roc_auc

    if len(config['performance_path']):   # save performance as well?
        from pathlib import Path
        path_output = join(config['base_path'], config['performance_path'])
        path_output = os.path.splitext(path_output)[0] + f"-{class_name}.pkl"
        check_dir (path_output)
        with open(path_output, 'wb') as f:
            pickle.dump(class_performance, f)
        str_time = datetime.datetime.now().strftime('%m-%d-%yT%H:%M:%S')

        # update 4/7 to print out performance in pivoted format
        path_output = join(config['base_path'], config['performance_path'])
        metric_list = ['precision', 'recall', 'f1', 'auc']
        if not exists(path_output):   # if file didn't exist, write header
            f = open(path_output, 'wt')
            f.write(f"class,{','.join(metric_list)},timestamp\n")
        else:   # otherwise, write in append mode
            f = open(path_output, 'at')
        f.write(f"{class_name},{','.join([str(class_performance['performance'][x]) for x in metric_list])},{str_time}\n")
        f.close()

        # update 4/7, output ROC curve as well
        path_figure = os.path.splitext(path_output)[0] + f"-{class_name}-ROC.png"
        plt.figure()
        lw = 2
        plt.plot(fpr, tpr, color='darkorange',
                lw=lw, label=f"ROC curve (area = {round(roc_auc,4)}, positives: {test_Y.sum()})")
        plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f"ROC Curve - {class_name} (positives: {test_Y.sum()})")
        plt.legend(loc="lower right")
        # plt.show()
        plt.savefig(path_figure)

        # update 4/8, output PR curve as well
        # https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html#sphx-glr-auto-examples-model-selection-plot-precision-recall-py
        path_figure = os.path.splitext(path_output)[0] + f"-{class_name}-PR.png"
        precision, recall, thresholds = precision_recall_curve(test_Y, probs)
        plt.figure()
        plt.step(recall, precision, where='post')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        plt.title(f"PRs  Curve - {class_name} (AP={round(class_performance['performance']['ap'], 4)} positives: {test_Y.sum()})")
        # plt.show()
        plt.savefig(path_figure)


    if len(config['output_path']):   # save output as well?
        path_output = join(config['base_path'], config['output_path'])
        _, test_X, test_clip_names = preprocess(test_labels, test_video_features, test_audio_features)
        if len(test_X) < 1:
            print("Error: Prediction output requested but no valid test samples/features were provided.")
        else:
            if trained is None:
                trained = create_model(config).fit(train_X, train_Y)
            if config['method'] == 'predict_proba':
                preds = trained.predict_proba(test_X)
                preds = preds[:,1]
            else:
                pred = trained.predict(test_X).astype(int)
                preds = pred
            if not exists(path_output):   # if file didn't exist, write header
                f = open(path_output, 'wt')
                f.write("path,class,score,prediction\n")
            else:   # otherwise, write in append mode
                f = open(path_output, 'at')

            for idx_s in range(len(test_clip_names)):
                f.write(f"\"{test_clip_names[idx_s]}\",{class_name},{preds[idx_s]},{pred[idx_s]}\n")
            f.close()

            print(f"Saving {len(preds)} test predictions to the specified path '{path_output}'.")

        # o_f = open("explosion_audio_only.txt", "wt")
        # o_f.write("video_clip_name\ttarget\tpredicted\n")
        # for i in range(n_test):
        #     o_f.write('{}\t{}\t{}\n'.format(test_clip_names[i], test_Y[i], preds[i]))
        # o_f.close()

    #pickle.dump(model, open('lr_audio_model.sav', 'wb'), protocol=2)
    return class_performance


def main(config={}, args=None):
    """ Main modeling capability"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="""A script to launch modeling""",
        epilog="""
        Example of training a single class with textual video labels.
            python modeling.py -b /n/nestor612-data/code/jdong/explosion -v experiments/3D/train_features \\ 
                -a experiments/audio/train -l train/train.txt -m model
        Example of training multiple classes, predict on all features, save to disk.
            python modeling.py  -l ../../content/labels/videos/completions/ -v ../../content/video_feature.hdf5 \\ 
                -o ../../content/labels/videos/predictions.csv -V ../../content/video_feature.hdf5
    """, formatter_class=argparse.RawTextHelpFormatter)
    submain = parser.add_argument_group('main execution and evaluation functionality')
    
    submain.add_argument('-b', '--base_path', type=str, default='.', help='base path prefix for features, labels, etc.')
    submain.add_argument('-l', '--label_path', type=str, required=True, help='relative path for input label (simple txt, one line or Labelstudio JSON)')
    submain.add_argument('-v', '--vidfeat_path', type=str, default='', help='relative path for video features')
    submain.add_argument('-a', '--audfeat_path', type=str, default='', help='relative path for audio features')
    submain.add_argument('-o', '--output_path', type=str, default='', help='relative path for output CSV file')
    submain.add_argument('-p', '--performance_path', type=str, default='', help='relative path for performance CSV file')
    submain.add_argument('-j', '--jobs', type=int, default=-1, help='how many cpus to use for cross_val_predict (-1 means all)')
    submain.add_argument('-f', '--folds', type=int, default=10, help='how many folds to use for cross_val_predict')

    submain.add_argument('--min_label_count', type=int, default=5, help='minimum count of labels for a class to be trained')
    submain.add_argument('--label_type', type=str, default='', help='specify label type provided, if skipped, auto-detect (binary-csv, json, multi-csv)')
    submain.add_argument('--estimator', type=str, default='sklearn.linear_model.LogisticRegression', help='specify the estimator to use')
    submain.add_argument('--est_params', type=str, default='{}', help='estimator parameters')
    #submain.add_argument('--est_params', type=str, default='{"C":4.0,"random_state":0,"max_iter":500,"class_weight":"balanced","solver":"lbfgs"}', help='estimator parameters')
    submain.add_argument('--method', type=str, default='predict_proba', help='the prediction method to use')

    submain = parser.add_argument_group('testing data options')
    submain.add_argument('-L', '--label_test_path', type=str, default=None, help='relative path for test input label (simple txt, one line or Labelstudio JSON)')
    submain.add_argument('-V', '--vidfeat_test_path', type=str, default='', help='relative path for test video features')
    submain.add_argument('-A', '--audfeat_test_path', type=str, default='', help='relative path for test audio features')

    submain = parser.add_argument_group('model serialization options')
    submain.add_argument('-m', '--model_path', type=str, default='', help="specify where the model should be written")
    submain.add_argument('--framework', type=str, default='sklearn', help="model framework e.g. sklearn, keras, etc")

    if args is None:
        config_defaults = vars(parser.parse_args())
    else:
        config_defaults = vars(parser.parse_args(args))
    config_defaults.update(config)
    config = config_defaults

    path_vidfeat = join(config['base_path'], config['vidfeat_path']) if len(config['vidfeat_path']) else None
    path_audfeat = join(config['base_path'], config['audfeat_path']) if len(config['audfeat_path']) else None
    if not (path_vidfeat is not None and exists(path_vidfeat)) and not (path_audfeat is not None and exists(path_audfeat)):
        print(f"Please provide either a valid video feature path '{path_vidfeat}' or audio feature path '{path_audfeat}', aborting.")
        parser.print_help()
        return -1

    # load training labels, training feature dataset
    path_train_label = join(config['base_path'], config['label_path'])
    if not exists(path_train_label):
        print(f"Please provide a valid label input path '{path_train_label}', aborting.")
        parser.print_help()
        return -1

    if isfile(path_train_label):
        train_labels = load_labels(path_train_label, config['label_type'])
    else:
        train_labels = load_labels_json(path_train_label)
    df_label_count = train_labels.sum(axis=0)
    for idx_class, count_class in df_label_count.items():
        if count_class < config['min_label_count']:
            del train_labels[idx_class]
            print(f"Dropping class {idx_class} because only {count_class} labels...")

    train_video_features = load_feature(path_vidfeat)
    train_audio_features = load_feature(path_audfeat)

    # load testing labels (if provided), training feature dataset
    test_labels = None
    if config['label_test_path'] is not None:
        path_test_label = join(config['base_path'], config['label_test_path'])
        if exists(path_test_label):
            if isfile(path_test_label):
                test_labels = load_labels(path_test_label, config['label_type'])
            else:
                test_labels = load_labels_json(path_test_label)

    test_video_features = load_feature(join(config['base_path'], config['vidfeat_test_path']) if len(config['vidfeat_test_path']) else None)
    test_audio_features = load_feature(join(config['base_path'], config['audfeat_test_path']) if len(config['audfeat_test_path']) else None)

    if len(config['output_path']):   # if asked for saving CSV and it exists, delete first
        path_output = join(config['base_path'], config['output_path'])
        if exists(path_output):
            os.unlink(path_output)

    # perform training and evaluation for each class
    for class_name in list(train_labels.columns):
        import datetime
        print ()
        print (datetime.datetime.now())
        print(f"Training and evaluating class '{class_name}'...")
        dict_performance = evaluate_class(config, train_labels, class_name, train_video_features, train_audio_features, 
                                        test_labels, test_video_features, test_audio_features)
        print(f"... performance {dict_performance['performance']}...")


    # generate final performance graph from generated assets
    if len(config['performance_path']) > 0:
        perf_path = join(config['base_path'], config['performance_path'])
        path_figure = os.path.splitext(perf_path)[0] + f"-performance.png"
        df_performance = pd.read_csv(perf_path).sort_values(['timestamp', 'class'])   # sort by timestamp
        df_performance['timestamp'] = pd.to_datetime(df_performance['timestamp'], format='%m-%d-%yT%H:%M:%S')
        class_name = df_performance["class"].unique()   # count classes involved
        df_performance = df_performance[df_performance['timestamp'] >= df_performance.iloc[-len(class_name)]['timestamp']]   # pick recent run
        timestamp_now = df_performance.iloc[-1]['timestamp']   # save timestamp before delete
        del df_performance['timestamp']
        df_performance.sort_values(by='class', inplace=True)
        ax = df_performance.plot.bar(x='class', rot=45)
        plt.grid(b=True, which='major', color='#666666', linestyle='-')
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        plt.ylabel('Performance')
        plt.ylim([0.0, 1.15])
        plt.subplots_adjust(bottom=0.3)   # extra space at bottom 
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=5, fancybox=True, shadow=True)
        plt.title(f"Overall Performance {len(class_name)} Classes (run at {timestamp_now})")
        plt.savefig(path_figure)

    print("All done.")


if __name__ == '__main__':
    main({})
