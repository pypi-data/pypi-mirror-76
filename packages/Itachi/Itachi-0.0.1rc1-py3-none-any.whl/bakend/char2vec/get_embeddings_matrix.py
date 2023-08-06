# -*- coding: utf-8 -*-
"""
@auther: kebo
@contact: itachi971009@gmail.com

@version: 1.0
@file: get_embedding_matrix.py
@time: 2019/11/29 17:26

这一行开始写关于本文件的说明与解释


"""
import numpy as np
import os
from tqdm import tqdm
from project_config import PROJECT_ROOT_PATH

# 默认embedding文件
default_pretrained_file = os.path.join(PROJECT_ROOT_PATH, "models/char2vec/embedding200.data")


def get_embeddings_matrix(word_index, pretrained_file):
    embeddings_dict = {}
    if not pretrained_file:
        pretrained_file = default_pretrained_file
    f = open(pretrained_file, "r")
    embedding_dim = int(f.readline().split()[1])
    for line in tqdm(f.readlines()):
        values = line.split()
        word = values[0]
        embeddings_dict[word] = np.asarray(values[1:], dtype='float32')
    f.close()
    embedding_matrix = np.zeros((len(word_index) + 1, embedding_dim))
    for word, i in word_index.items():
        embedding_vector = embeddings_dict.get(word)
        if embedding_vector is not None:
            # words not found in embedding index will be all-zeros.
            embedding_matrix[i] = embedding_vector
    return embedding_matrix
