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
model = GPT2LMHeadModel.from_pretrained("/root/AUTOCoder/GPyT_3/checkpoint-2500").to("cuda")


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


def generate(inp, maxlength=100):
    """

    Args:
        inp: 用户输入的代码段
        maxlength: 处理字符的上限,默认为100

    Returns:
        模型生成的新代码 和 新代码的行数

    """
    inp = encode_newlines(inp)
    newline_count = inp.count(NEWLINECHAR)
    input_ids = tokenizer.encode(inp, return_tensors="pt").to("cuda")
    try:
        model_output = model.generate(
            input_ids,
            max_length=maxlength,
            num_beams=5,
            temperature=1,
            no_repeat_ngram_size=5,
            # num_return_sequence=3,
            return_dict_in_generate=True,
            output_scores=True)
        return model_output, newline_count
    except IndexError as e:
        # print(e)
        pass


def auto_complete(inp, maxlength=100):
    """

    Args:
        inp: 用户输入的代码段
        maxlength: 处理字符的上限,默认为100

    Returns:
        模型生成的新代码
    """
    try:
        model_output, _ = generate(inp, maxlength)
        sequence = model_output['sequences'][0]
        decoded = decode_newlines(tokenizer.decode(sequence))
        return decoded
    except TypeError as e:
        # print("TypeError:", e)
        return ""


def stop_at_repeat(inp):
    """

    Args:
        inp: 用户输入的代码段

    Returns:
        模型生成的新代码(不会带有重复段落)

    """
    model_output = generate(inp)
    lines = model_output['sequences'].splitlines(True)
    no_repeat = ""
    for line in lines:
        if no_repeat.count(line) == 0 or line == "\n":
            no_repeat += line
        else:
            return no_repeat
    return no_repeat


def count(i):
    return 1


mode = input("请输入数字,选择启动方式：1、命令行格式 2、后台钩子模式:")

if mode == "1":
    while True:
        try:
            inpu = input("> ")
            predict = auto_complete(inpu)
            predict = predict.replace("N>", "\n")
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
            predict = auto_complete(inpu)
            print(predict)
        except RuntimeError:
            pass
        sleep(5)
        os.system('cls')
