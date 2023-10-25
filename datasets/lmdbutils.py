"""
#   Copyright (C) 2022 BAIDU CORPORATION. All rights reserved.
#   Author     :   tanglicheng@baidu.com
#   Date       :   2022-02-10
"""
import io
import os
import lmdb
import json
from PIL import Image, ImageFile
import numpy as np

ImageFile.LOAD_TRUNCATED_IMAGES = True

def load_lmdb(lmdb_path):
    """
    load_lmdb
    """
    lmdb_path = os.path.join(lmdb_path)
    env = lmdb.open(
        lmdb_path,
        max_readers=32,
        readonly=True,
        lock=False,
        readahead=False,
        meminit=False,
    )
    return env


def load_json(json_path):
    """
    load_json
    """
    with open(json_path) as f:
        meta = json.load(f)

    return meta


def read_data_from_lmdb(env, lmdb_key):
    """
    read_data_from_lmdb
    """
    with env.begin(write=False) as txn:
        data = txn.get(lmdb_key.encode())
        data = deserialize_data(data)
    return data



def deserialize_data(data):
    """
    deserialize_data
    """
    if data is None:
        return None

    buf = io.BytesIO()
    buf.write(data)
    buf.seek(0)
    img = Image.open(buf)

    unpacked_data = {
        "img": img
    }

    return unpacked_data
