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
from datetime import datetime
import argparse
import json
from scipy.spatial.distance import cdist

from io import BytesIO
import tempfile

import pandas as pd
import numpy as np
import h5py

path_root = Path(__file__).parent
if __name__ == '__main__':
    # patch the path to include this object
    path_package = path_root.parent.resolve()
    if path_package not in sys.path:
        sys.path.append(str(path_package))

import contentaiextractor as contentai
from contentai_activity_classifier import _version

def feature_flatten(x, include_norm=True):
    if type(x) != pd.Series: # safety to avoid "double flatten" from creation + read
        return x
    
    # print(f"MERGE1: {x.shape, type(x), len(x), x}")
    if len(x) == 1:  # just one item in series
        # print(f"LEN1 return {x} type {x.shape}, len {len(x)}, shape2 {x.values[0].shape}, type {type(x)}")
        return x.values
    x = x.mean(axis=0)
   
    vec = np.reshape(x, (1, x.shape[0]))
    # print(f"MERGE4: {vec.shape, type(vec), len(vec), vec}")
    vec_norm = vec * 1 / feature_l2norm(vec)
    return vec_norm


def feature_l2norm(x):
    # print(f"NORM: {x.shape, type(x), len(x), x}")
    return np.linalg.norm(x.astype(np.float32), 2)


def feature_read_timed(df_list, time_interval=1.5, dim_exemplar=0):
    """Function to read features from video + audio into single vector in time intervals (seconds)"""

    time_begin = 0
    list_paths = set()
    for df in df_list:   # iterate through all frames for unique names
        list_paths |= set(df["video_path"].unique())
    list_paths = list(list_paths)  # convert back to a list

    if time_interval is None or time_interval == 0:  # specified no end? go for max!
        time_interval = 0
        for df in df_list:
            time_interval = max(df["time_end"].max(), time_interval)

    while True:
        time_end = time_begin + time_interval

        for path_segment in list_paths:
            vec = None
            for df in df_list:
                df_sub = df[(df["video_path"] == path_segment) & ((df["time_begin"] >= time_begin) | (df['time_end'] > time_begin)) & (df["time_begin"] < time_end)]
                if len(df_sub) > 0:
                    # print(df_sub)
                    vec_new = feature_flatten(df_sub["features"])[0]
                    if vec is None:   # if there was no video, just take audio
                        vec = vec_new
                    else:       # if there was audio, normalize and concatenate
                        vec = vec * 1.0 / feature_l2norm(vec)
                        vec_new = vec_new * 1.0 / feature_l2norm(vec_new)
                        vec = np.hstack((vec, vec_new))

                    # print(f" SHAPE: {'empty' if vec is None else vec.shape}, VEC: {'none' if vec is None else vec.shape}")
            if vec is None or len(vec) == 0:
                break
            
            dim_feat = len(vec) if len(vec.shape)==1 else vec.shape[1]
            if dim_exemplar == 0:
                dim_exemplar = dim_feat
                print(f"INFO: A/V features dimensionality examplar from '{path_segment} @ {time_begin}, {time_end}'; found {dim_feat} features")
            if dim_exemplar != dim_feat:   # check for consistency in A/V features
                print(f"ERROR: A/V features not consistent for time ({path_segment} @ {time_begin}, {time_end}); expected {dim_exemplar}, found {dim_feat} features")
            else:
                yield vec, time_begin, time_end, path_segment
        time_begin = time_end   # update time
        if vec is None:
            break            
    return None, time_begin, time_end   # nothing left


def feature_load(extractor_name, path_source, dict_cache={}, verbose=False, flatten=False, recursive=False):
    if extractor_name in dict_cache:   # cache hit? return! (NOTE: no robustness between recursive + non-recursive)
        return dict_cache[extractor_name]
    df_combined = None
    if recursive:  # recursive mode will get a new DataFrame and concatenate into one monster one.
        num_directories = 0
        num_valid = 0
        for path_search in Path(path_source).rglob("*"):
            if path_search.is_dir() and extractor_name in str(path_search):
                df_new = feature_load(extractor_name, path_search, {}, verbose=False, flatten=flatten)  # recurse to load features
                if df_new is not None:   # valid result?
                    path_rel = path_search.parent.relative_to(path_source)
                    df_new["video_path"] = df_new["video_path"].apply(lambda x: str(path_rel.joinpath(x)))  # add prefix
                    if df_combined is None:
                        df_combined = df_new
                    else:
                        df_combined = df_combined.append(df_new, sort=False, ignore_index=True)
                    num_valid += 1
            # end valid dir
            num_directories += 1
        # end search for 
        if verbose:
            print(f"Recursive scan for extractor {extractor_name} in {str(path_source)}, found {num_directories} directories with {num_valid} sources")
            print(f"Data frame dimensionality: {df_combined.shape} with {df_combined['video_path'].unique()} unique paths.")
    else:
        if extractor_name in ["dsai_videocnn", "dsai_vggish"]:
            df_combined = feature_load_hdf5(extractor_name, path_source, flatten=flatten, verbose=verbose)

    if df_combined is not None:
        dict_cache[extractor_name] = df_combined   # save it for next run
    return df_combined    # reutrn the cached version


def feature_load_hdf5(extractor_name, path_source, flatten=False, verbose=False):
    # no caching at this level...
    path_features = None
    is_temporary = False
    df_active = None
    if contentai.running_in_contentai:   # running in contentai?
        dict_keys = None
        try:
            dict_keys = contentai.keys(extractor_name)
        except Exception as e:
            print(f"Error retrieving keys for {extractor_name}...'{e}'")
        if verbose:
            print(f"KEYS: {dict_keys}, EXTRACTOR: {extractor_name}")
        if dict_keys is not None and 'keys' in dict_keys:   # valid contentai data store?
            dict_keys = dict_keys['keys']   # derference the keys so we can use them
            if "data.json" in dict_keys  and "data.hdf5" in dict_keys:   # confirmed JSON + HDF5 package
                dict_timing = None
                try:
                    dict_timing = contentai.get_json(extractor_name, "data.json")
                except Exception as e:
                    print(f"Error retrieving 'data.json' for {extractor_name}...'{e}'")

                data_feat = b''
                if dict_timing is not None:  # good prior data
                    df_active = pd.json_normalize(dict_timing)
                    if verbose:
                        print(f"ENTRIES: {df_active}")
                    data_feat = b''
                    try:
                        data_feat = contentai.get_bytes(extractor_name, "data.hdf5")
                    except Exception as e:
                        print(f"Error retrieving 'data.hdf5' for {extractor_name}...'{e}'")

                    if verbose:
                        # print(f"DATA: {data_feat}, TYPE: {type(data_feat)}")
                        print(f"BINARY h5: {len(data_feat)}")
                    is_temporary = True

                if len(data_feat) > 0:
                    if type(data_feat) == str:
                        buffer_string = BytesIO(data_feat.encode('utf-8'))   # open io buffer
                    else:
                        buffer_string = BytesIO(data_feat)   # open io buffer
                    temp_obj = tempfile.NamedTemporaryFile(mode='w+b', suffix='.hdf5', delete=False)   # get temp file
                    if verbose:
                        print(f"TEMPFILE: {temp_obj.name}")
                    temp_obj.seek(0)   # close prior name
                    chunk_size = pow(2, 15)
                    len_written = 0
                    while True:   # write buffer to disk
                        data = buffer_string.read(chunk_size)
                        if not data:
                            break
                        temp_obj.write(data)
                        len_written += len(data)
                    temp_obj.close()

                    path_features = Path(temp_obj.name)
                    print(f"Wrote binary data of length '{len_written}' to temp file '{temp_obj.name}' ({extractor_name})")

    else:  # do we need to load it locally?
        path_source = Path(path_source).parent
        path_timing = path_source.joinpath(extractor_name, "data.json")
        if not path_timing.exists():
            path_timing = Path(str(path_timing.resolve()) + ".gz")
        if path_timing.exists():
            df_active = pd.read_json(path_timing)
        if verbose:
            print(f"FEATURES Loaded: {extractor_name}, {path_features}")
        path_features = Path(path_source).joinpath(extractor_name, "data.hdf5")

    # print(f"{path_features} -> {path_timing}")
    if df_active is None or path_features is None:
        if Path(path_features).is_dir():
            print(f"Failed to load features '{path_features}' or timing data was empty, aborting")
        return None

    if verbose:
        print(df_active)
    df_active.sort_values(['video_path', 'time_begin'], inplace=True)
    df_features = pd.DataFrame()

    has_alias = "video_alias" in list(df_active.columns)
    with h5py.File(path_features, "r") as f:   # read hdf5 file via its structure
        for video_name in f.keys():
            feature = list(f[video_name][()])

            #          video_path  idx   time_begin     time_end video_alias
            # 0         shazam@0.0    0     0.000000     0.666667      shazam
            # 1         shazam@0.0    1     0.666667     1.333333      shazam
            # 12159  shazam@5700.0  449  5999.333333  6000.000000      shazam
            # 12160  shazam@5700.0  450  6000.000000  6000.666667      shazam
            
            df_new = df_active[df_active['video_path'] == video_name].copy()
            df_new["features"] = feature
            df_features = df_features.append(df_new)
    df_active = df_features
    df_features = None

    # clean up temp file (do it now because thigns are already loaded!)
    if is_temporary and path_features.exists():
        path_features.unlink()

    if has_alias:   # was there an alias column here to fix?
        if df_active.duplicated('time_begin').any():   # only proceed if duplicates
            count_raw = len(df_active)
            # There is an issue where the a frame may be repeated at the end of one clip and the start of another
            #   we can find it by sorting by video path (which has clip timing) and the begin time of the frame
            # first, strop off the timing from the clip
            df_active["sync"] = df_active["video_path"].apply(lambda x: float(x.split('@')[-1]))
            # next, sort by clip and absolute timing
            df_active.sort_values(['time_begin', 'sync', 'video_alias'], inplace=True, ascending=False)
            # drop duplicate rows
            df_active.drop_duplicates(['time_begin', 'sync', 'video_alias'], keep='first', inplace=True)
            count_dedup = len(df_active)
            print(f"Reduced original from {count_raw} to {count_dedup} rows by duplicate during hdf5 feature load...")
        # rename with alias to get to the right place
        df_active["video_path"] = df_active["video_alias"]
        # del df_active["video_alias"]
        if verbose:
            print(f"Removed alias column 'video_alias' during hdf5 feature load...")

    # print("----------------------------------------\n", extractor_name, "\n", df_active)

    # update cached versions
    if flatten:
        df_new = df_active.head(1).copy()   # clone the first entry
        df_new["time_begin"] = df_active["time_begin"].min()
        df_new["time_end"] = df_active["time_end"].max()
        df_new["features"] = [feature_flatten(df_active["features"])]
        df_active = df_new  # update with flattened version
    
    return df_active


def difference(input_params=None, args=None):
    """Method to compute the similarity of several clips according to their low-level features..."""

    parser = argparse.ArgumentParser(
        description="""A script to perform clip similarity""",
        epilog="""
        Difference compute for all features in a file 
            python features.py --feature_file video.hdf5 audio.hdf5 --path_content features/dummy.txt --path_result results
        Difference between testing files
            python -u contentai_activity_classifier/features.py --path_content testing/data/dummy.txt \\ 
                    --feature_type dsai_videocnn dsai_vggish --path_result testing/dist
    """, formatter_class=argparse.RawTextHelpFormatter)
    submain = parser.add_argument_group('main execution and evaluation functionality')
    submain.add_argument('--path_content', dest='path_content', type=str, default=contentai.content_path, 
                            help='input feature path for files to compute (can reference non-existing file)')
    submain.add_argument('--path_result', dest='path_result', type=str, default=contentai.result_path, 
                            help='output path for samples')
    submain.add_argument('--round_decimals', dest='round_decimals', type=int, default=5,  
                            help='rounding decimals for predictions')
    submain.add_argument('--metric', dest='metric', type=str, default="cosine", 
                            help='distance metric for compute (default=cosine); others from *scipy.spatial.distance.cdist*')
    submain.add_argument('--feature_type', dest='feature_type',  nargs='+', default=None,
                            help='specify one or more feature files (located within "path_content")')
    submain.add_argument('--quiet', dest='quiet', default=False, action='store_true', 
                            help='quiet print operations')

    if args is not None:
        config = vars(parser.parse_args(args))
    else:
        config = vars(parser.parse_args())
    if input_params is not None:
        config.update(input_params)
    config.update(contentai.metadata())

    print(f"Run argments: {config}")

    path_data = Path(config['path_content'])
    if config['feature_type'] is None:
        print(f"No valid feature files detected, aborting.")
        return None
    if not path_data.exists():
        print(f"Input content path does not exist '{str(path_data)}'")
        return None
    if not path_data.is_dir():
        path_data = path_data.parent

    # depending on the model specified, attempt to load features
    list_df = []
    dict_cache = {}
    for file_feat in config['feature_type']:
        df = feature_load(file_feat, str(path_data), dict_cache, flatten=True, recursive=True, verbose=not config['quiet'])
        if df is not None:
            list_df.append(df)

    print(f"Found {len(list_df)} different feature sources...")

    # for now, we'll sample to get all features
    df_dist = None
    if len(list_df) != 0:   # no valid features
        # currently, this operation will cache all features in memory, if this is too heavy
        # it can be modified to run in stages...
        list_clips = []
        nd_features = []
        dim_exemplar = 0
        for vec, time_begin, time_end, path_segment in feature_read_timed(list_df, None, dim_exemplar):
            # NOTE: we don't care about begin/end because we're averaging the whole clip
            list_clips.append(path_segment)
            nd_features.append(vec)
            if dim_exemplar == 0:
                dim_exemplar = vec.shape[1]
                # print(f"LEN: {vec.shape[1]}, examplar {dim_exemplar}")
        nd_features = np.vstack(nd_features)
        df_dist = pd.DataFrame(cdist(nd_features, nd_features, metric=config['metric']), 
                        columns=list_clips, index=list_clips).round(config['round_decimals'])

        nd_features = None
        print(f"Computed distance matrix for {len(df_dist)} videos...")

    # write output of each class and segment
    version_dict = _version.version()
    dict_result = {'config': {'version':version_dict['version'], 'extractor':version_dict['package'],
                            'input':str(path_data.resolve()), 'timestamp': str(datetime.now()) }, 'results':{} }
    if df_dist is None:
        print(f"No predictions made from {num_models} unique models...")
    else:
        dict_result['results'] = df_dist.to_dict(orient='index')

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
    difference()
