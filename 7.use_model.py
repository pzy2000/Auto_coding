import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# import tensorflow as tf
import transformers
# tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from time import sleep

NEWLINECHAR = "<N>"
transformers.logging.set_verbosity_error()
tokenizer = GPT2Tokenizer.from_pretrained('tokenizer')
import os

os.environ["USE_TORCH"] = "True"
tokenizer.add_special_tokens({
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>"
})
# model = GPT2LMHeadModel.from_pretrained("/home/ise/pzy/AUTOCoder/GPyT_3/checkpoint-2500").to("cuda")
model = GPT2LMHeadModel.from_pretrained("GPyT_3/checkpoint-12500").to("cuda")


def encode_newlines(inp):
    """

    Args:
        inp: 用户输入的代码段

    Returns:
        对输入进行换行符替换操作后，输出

    """
    return inp.replace("\n", NEWLINECHAR)


def decode_newlines(inp):
    """

    Args:
        inp: 模型输出的未经处理的语句

    Returns:
        输出将鬼画符替换为换行符后的结果

    """
    return inp.replace(NEWLINECHAR, "\n")


def generate(code, max_length=100):
    '''Takes input code, replaces newline chars with <N>,
    tokenizes, feeds thru model, decodes,
    then reformats the newlines back in'''
    newlinechar = "<N>"
    converted = code.replace("\n", newlinechar)
    tokenized = tokenizer.encode(converted, return_tensors='pt').to("cuda")
    resp = model.generate(tokenized, max_length=max_length).to("cuda")

    decoded = tokenizer.decode(resp[0])
    reformatted = decoded.replace("<N>", "\n")
    return reformatted


def auto_complete(inp, maxlength=100):
    """

    Args:
        inp: 用户输入的代码段
        maxlength: 处理字符的上限,默认为100

    Returns:
        模型生成的新代码
    """
    try:
        model_output = generate(inp, maxlength)
        sequence = model_output['sequences'][0]
        decoded = decode_newlines(tokenizer.decode(sequence))
        return decoded
    except TypeError as e:
        # print("TypeError:", e)
        return ""


def stop_at_repeat(model_out):
    lines = model_out.splitlines(True)
    no_repeat = ""
    for l in lines:
        if no_repeat.count(l) == 0 or l == "\n":
            no_repeat += l
        else:
            return no_repeat
    return no_repeat


def next_line_only(original, model_out):
    orig_nl = original.count("\n")
    one_more_lines = [l for l in model_out.splitlines(True)][:orig_nl + 1]
    one_more_line = "".join(one_more_lines)
    return one_more_line


def count(i):
    return 2


def postprocess(origin_output):
    processed_output = origin_output.replace("N>", "\n")
    return processed_output


mode = input("请输入数字,选择启动方式：0、命令行格式（加强版）1、命令行格式 2、后台钩子模式: 3、生成器模式 4、多段预输入模式")

if mode == "0":
    while True:
        try:
            inpu = input(">>> ")
            m = generate(inpu)
            predict = stop_at_repeat(m)
            predict = postprocess(predict)
            print("Autocompleted:")
            print()
            print(predict)
        except RuntimeError:
            pass
        except IndexError:
            pass

elif mode == "1":
    while True:
        try:
            inpu = input(">>> ")
            predict = generate(inpu)
            predict = postprocess(predict)
            print("Autocompleted:")
            print()
            print(predict)
        except RuntimeError:
            pass
        except IndexError:
            pass

elif mode == "2":
    while True:
        try:
            with open("keyboard.txt", 'r') as f:
                inpu = f.read()
            predict = stop_at_repeat(inpu)
            print(predict)
        except RuntimeError:
            pass
        sleep(5)
        os.system('cls')

elif mode == "3":
    while True:
        try:
            inpu = input(">>> ")
            m = generate(inpu)
            predict = next_line_only(inpu, m)
            predict = postprocess(predict)
            print("Autocompleted:")
            print()
            print(predict)
        except RuntimeError:
            pass
        except IndexError:
            pass

elif mode == "4":
    try:
        inpu = '''#include "mainwindow.h"
#include <QApplication>'''
        predict = generate(inpu)
        predict = postprocess(predict)
        print("Autocompleted:")
        print()
        print(predict)
    except RuntimeError:
        pass
    except IndexError:
        pass
