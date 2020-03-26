from hashlib import md5
from typing import List
import time


def md5_str(s: str):
    """
    计算字符串的md5值
    """
    x = md5()
    x.update(s.encode('utf8'))
    y = x.hexdigest()
    return y


