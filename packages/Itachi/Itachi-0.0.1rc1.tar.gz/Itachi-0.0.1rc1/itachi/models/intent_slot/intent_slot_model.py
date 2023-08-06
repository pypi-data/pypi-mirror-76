# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: itachi971009@gmail.com

@version: 1.0
@file: intent_slot_model.py
@time: 2020/3/24 11:13

这一行开始写关于本文件的说明与解释


"""
import tensorflow as tf
import numpy as np

from itachi.models.model import Model


class IntentSlotModel(Model):
    def __init__(self):
        super(IntentSlotModel).__init__()

    def call(self, inputs, training=None, mask=None):
        raise NotImplementedError

    def train(self):
        pass
