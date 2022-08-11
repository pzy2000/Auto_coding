# Auto_coding
An auto coding tool for python,off-brand github-copliot,trained with GPT2 transformer and github public repos codes

It contains a GPT2 model trained from scratch (not fine tuned) on Python code from Github. Overall, it was ~80GB of pure Python code, the current model is a mere 2 epochs through this data, so it may benefit greatly from continued training and/or fine-tuning.

Input to the model is code, up to the context length of 1024.
# 使用指南
按照代码文件前的阿拉伯数字顺序运行即可，注意把数据文件和模型放到指定位置，路径不要有中文。

# Here's a quick example of using this model:
```python
from transformers import AutoTokenizer, AutoModelWithLMHead

tokenizer = AutoTokenizer.from_pretrained("Sentdex/GPyT")
model = AutoModelWithLMHead.from_pretrained("Sentdex/GPyT")

'''copy and paste some code in here'''
inp = """import"""

newlinechar = "<N>"
converted = inp.replace("\n", newlinechar)
tokenized = tokenizer.encode(converted, return_tensors='pt')
resp = model.generate(tokenized)

decoded = tokenizer.decode(resp[0])
reformatted = decoded.replace("<N>","\n")

print(reformatted)
```
# Should produce:
```python
import numpy as np
import pytest

import pandas as pd
```
