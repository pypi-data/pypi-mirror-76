# import pandas as pd
# import numpy as np


def cardinality_cutter(data, sample_threshold=50):
    cardinality = data.select_dtypes(exclude='number').nunique()
    cat_features = cardinality[cardinality <= sample_threshold].index.tolist()
    return cat_features

