# -*- coding: utf-8 -*-
# @Time     : 2020-03-19 12:29
# @Author   : beking
import re


def format_word(word):
    if word:
        re.sub(r'\s+', '', word)
        word = str(word).strip()
        return word
