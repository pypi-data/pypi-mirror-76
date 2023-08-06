from os.path import isfile, join, exists



class GenericDataLoader():
    def __init__(self, base_path='.', vidfeat_path=None, audfeat_path=None, label_path=None, sep=',', 
                 label_type='multi-csv', min_label_count=5, col_id=0, col_label=1):
        # Convert all arguments to class vars
        arguments = locals()
        for k, v in arguments.items():
            setattr(self, k, v)


    def load_feature(self, feature_dir):
        import re
        import os
        import h5py
        import numpy as np

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


    def get_labels_new (self):
        import pandas as pd
        path_train_label = join(self.base_path, self.label_path)
        label_df = pd.read_csv(path_train_label, sep=self.sep)
        label_df['path'] = label_df['path'].str.replace(".mp4", "")
        return label_df


    def preprocess (self, label_df, video_features, audio_features):        # simplified version of the one in modeling.py
        import numpy as np

        def l2norm(x):
            return np.sqrt(x.dot(x))

        targets=[]
        features=[]
        vidnames=[]
        shape_test = None
        for idx, row in label_df.iterrows():
            video_name = row[self.col_id]
            vec = None
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
            if shape_test is not None and vec is not None and shape_test != vec.shape:
                print(f"Error: Vector size {vec.shape} inconsistent with prior {shape_test} (sample {video_name}")
            elif vec is not None:
                targets.append(row[self.col_label])
                vidnames.append(video_name)
                features.append(vec)
                shape_test = vec.shape
        print(f"Associated {len(vidnames)} labels to {len(label_df)} audio/video features...")
        return np.array(features, dtype='float32'), targets, vidnames



    def load_XY_paths (self):
        labels = self.get_labels_new()
        video_features = self.load_feature(self.vidfeat_path)       # a dict
        audio_features = self.load_feature(self.audfeat_path)       # a dict
        return self.preprocess (labels, video_features, audio_features)


# For testing and example usage.
if __name__ == "__main__":
    #pl = GenericDataLoader(vidfeat_path='/n/docroot10/projects/emotion/data/DigitalLQ/features/video_feature.hdf5', audfeat_path='/n/docroot10/projects/emotion/data/DigitalLQ/features/audio_feature.hdf5', label_path='DigitalLQ_labels.csv', label_type='multi-csv')
    #pl = GenericDataLoader(vidfeat_path='emotions_video.hdf5', audfeat_path='emotions_audio.hdf5', label_path='ugc_labels.csv')
    pl = GenericDataLoader(vidfeat_path='./models/UGC/emotions_video.hdf5', label_path='ugc_labels.csv')
    X,y,paths = pl.load_XY_paths()
    print ("Done.")
