#! python
# ===============LICENSE_START=======================================================
# contentai_activity_classifier Apache-2.0
# ===================================================================================
# Copyright (C) 2017-2020 AT&T Intellectual Property. All rights reserved.
# ===================================================================================
# This software file is distributed by AT&T 
# under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============LICENSE_END=========================================================
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
import argparse
import pickle, gzip
from datetime import datetime
import json

import pandas as pd
import numpy as np

import contentaiextractor as contentai

path_root = Path(__file__).parent
if __name__ == '__main__':
    # patch the path to include this object
    path_package = path_root.parent.resolve()
    if path_package not in sys.path:
        sys.path.append(str(path_package))


from contentai_activity_classifier import features, _version, wrapped


def model_discover(path_manifest):
    path_manifest = Path(path_manifest)
    if not path_manifest.exists():
        return None
    df = pd.read_json(path_manifest).fillna('')
    return df


def model_load(path_model, type_model):
    path_model = Path(path_model)
    try:
        if type_model == "sklearn":
            # print(f"{path_model}")
            if path_model.exists():
                if ".gz" in path_model.suffix.lower():
                    return pickle.load(gzip.open(str(path_model.resolve()), 'rb'))
                return pickle.load(path_model.open('rb'))
        elif type_model == "wrapped":
            return wrapped.read_model(path_model)
    except Exception as e:
        print(f"Failed to load model '{path_model.resolve()}' of type '{type_model}' with error '{e}'")
    return None


def classify(input_params=None, args=None, path_local=path_root, version_dict=None):
    # extract data from contentai.content_url
    # or if needed locally use contentai.content_path
    # after calling contentai.download_content()
    print("Downloading content from ContentAI")
    contentai.download_content()

    parser = argparse.ArgumentParser(
        description="""A script to perform model classification""",
        epilog="""
        Launch with classes and model server on default port 
            python -u contentai_activity_classifier/main.py --path_content testing/data/max-launch/video.mp4  \\
                        --path_result testing/class --path_models contentai_activity_classifier/data/models/manifest.json --verbose
    """, formatter_class=argparse.RawTextHelpFormatter)
    submain = parser.add_argument_group('main execution and evaluation functionality')
    submain.add_argument('--path_content', dest='path_content', type=str, default=contentai.content_path, 
                            help='input video path for files to label')
    submain.add_argument('--path_result', dest='path_result', type=str, default=contentai.result_path, 
                            help='output path for samples')
    submain.add_argument('--path_models', dest='path_models', type=str, default=str(path_local.joinpath('data', 'models', 'manifest.json').resolve()),
                            help='manifest path for model information')
    submain.add_argument('--time_interval', dest='time_interval', type=float, default=3,  
                            help='time interval for predictions from models')
    submain.add_argument('--round_decimals', dest='round_decimals', type=int, default=5,  
                            help='rounding decimals for predictions')
    submain.add_argument('--score_min', dest='score_min', type=float, default=0.1,
                            help='apply a minimum score threshold for classes')
    submain.add_argument('--average_predictions', dest='average_predictions', default=False, action='store_true', 
                            help='average predictions for same class name')
    submain.add_argument('--verbose', dest='verbose', default=False, action='store_true', 
                            help='verbosely print operations')

    if args is not None:
        config = vars(parser.parse_args(args))
    else:
        config = vars(parser.parse_args())
    if input_params is not None:
        config.update(input_params)
    config.update(contentai.metadata())

    print(f"Run argments: {config}")

    path_data = Path(config['path_content'])

    # depending on the model specified, attempt to load features
    path_models = Path(config['path_models']).parent
    df_models = model_discover(config['path_models'])
    if df_models is None:
        print(f"Failed to load models or manifest from '{path_models}', aborting")
        return None

    df_predict_all = None
    num_models = 0
    dict_cache = {}
    for type_video, df_models_subv in df_models.groupby('video'):
        for type_audio, df_models_suba in df_models_subv.groupby('audio'):
            list_df = []
            num_models += len(df_models_suba)

            # load features if we can...
            num_expected = 0
            if len(type_video) > 0:     # video only or video and audio case
                list_df.append(features.feature_load(type_video, path_data, dict_cache, config['verbose']))
                num_expected += 1
            if len(type_audio) > 0:   # audio only case
                list_df.append(features.feature_load(type_audio, path_data, dict_cache, config['verbose']))
                num_expected += 1
            list_df = [x for x in list_df if x is not None]

            # for overlapping windows (need to average and combine incoming features)
            nd_features = []
            list_times = []
            if len(list_df) != num_expected:   # no valid features
                print(f"Incomplete feature set for this A/V feature request, skipping these models {list(df_models_suba['name'])}... (found {len(list_df)}, expected {num_expected} feature sets)")
            else:
                for vec, time_begin, time_end, path_segment in features.feature_read_timed(list_df, config['time_interval']):
                    nd_features.append(vec)
                    list_times.append([time_begin, time_end])
                    # print(f"TIME: {time_begin}, {time_end}, {type_audio}, {type_video}, {df_models_suba}")
                nd_features = np.vstack(nd_features)
                df_predict_base = pd.DataFrame(list_times, columns=["time_begin", "time_end"])
                df_predict_base["type_audio"] = type_audio
                df_predict_base["type_video"] = type_video
                df_predict_base["path_video"] = path_segment

                # perform evaluation with correct model
                for idx, row_model in df_models_suba.iterrows():
                    model = model_load(path_models.joinpath(row_model['path']), row_model["framework"])
                    if model is not None:
                        if config['verbose']:
                            print(row_model['name'], nd_features.shape, type_video, type_audio)
                        predict = model.predict_proba(np.array(nd_features))
                        df_predict = df_predict_base.copy()
                        df_predict["score"] = predict[:, 1]
                        df_predict["class"] = row_model['name']
                        df_predict = df_predict[df_predict["score"] > config['score_min']]  # threshold value v1.1.0
                        if df_predict_all is None:
                            df_predict_all = df_predict
                        else:
                            df_predict_all = df_predict_all.append(df_predict, sort=False, ignore_index=True)
    
    # write output of each class and segment
    if version_dict is None:
        version_dict = _version.version()
    dict_result = {'config': {'version':version_dict['version'], 'extractor':version_dict['package'],
                            'input':str(path_data.resolve()), 'timestamp': str(datetime.now()) }, 'results':[] }
    if df_predict_all is None:
        print(f"No predictions made from {num_models} unique models...")

    else:
        if config['average_predictions']:
            df_predict_all = df_predict_all.groupby(['time_begin', 'class']).mean().reset_index(drop=False)
        df_predict_all.sort_values(['time_begin', 'class'], inplace=True)
        df_predict_all = df_predict_all.round({"score": config['round_decimals']})
        dict_result['results'] = df_predict_all.to_dict(orient='records')
        print(f"Created {len(df_predict_all)} total predictions from {num_models} unique models...")

        # write out data if completed
        if len(config['path_result']) > 0:
            path_result = Path(config['path_result'])
            if not path_result.exists():
                path_result.mkdir(parents=True)
            path_result = Path(config['path_result']).joinpath("data.json")
            with path_result.open('wt') as f:
                json.dump(dict_result, f)
            print(f"Written to '{path_result.resolve()}'...")

    # return dict of data
    if not contentai.running_in_contentai:
        return dict_result


if __name__ == "__main__":
    classify()
