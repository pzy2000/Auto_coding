from transformers import GPT2LMHeadModel, GPT2Tokenizer
from time import sleep

NEWLINECHAR = "<N>"

tokenizer = GPT2Tokenizer.from_pretrained('GPyT_1/GPyT_TOK_75GB')

tokenizer.add_special_tokens({
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>"
})

model = GPT2LMHeadModel.from_pretrained("GPyT_1/latest_model").to("cuda")


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
    model_output = model.generate(
        input_ids,
        max_length=maxlength,
        num_beams=5,
        temperature=0.7,
        no_repeat_ngram_size=5,
        num_return_sequence=3,
        return_dict_in_generate=True,
        output_scores=True)
    return model_output, newline_count


def auto_complete(inp, maxlength=100):
    """

    Args:
        inp: 用户输入的代码段
        maxlength: 处理字符的上限,默认为100

    Returns:
        模型生成的新代码
    """
    model_output, _ = generate(inp, maxlength)
    sequence = model_output['sequences'][0]
    decoded = decode_newlines(tokenizer.decode(sequence))
    return decoded


def stop_at_repeat(inp):
    """

    Args:
        inp: 用户输入的代码段

    Returns:
        模型生成的新代码(不会带有重复段落)

    """
    model_output = generate(inp)
    lines = model_output.splitlines(True)
    no_repeat = ""
    for line in lines:
        if no_repeat.count(line) == 0 or line == "\n":
            no_repeat += line
        else:
            return no_repeat
    return no_repeat


while True:
    try:
        with open("keyboard.txt", 'r') as f:
            inpu = f.read()
        predict = auto_complete(inpu)
        print(predict)
    except RuntimeError:
        pass
    sleep(5)
