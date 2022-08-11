from transformers import GPT2LMHeadModel, GPT2Tokenizer

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
    return inp.replace("\n", NEWLINECHAR)


def decode_newlines(inp):
    return inp.replace(NEWLINECHAR, "\n")


def generate(inp, maxlength=100):
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
    model_output, count = generate(inp, maxlength)
    sequence = model_output['sequences'][0]
    decoded = decode_newlines(tokenizer.decode(sequence))
    return decoded


def stop_at_repeat(inp):
    model_output = generate(inp)
    lines = model_output.splitlines(True)
    no_repeat = ""
    for l in lines:
        if no_repeat.count(l) == 0 or l == "\n":
            no_repeat += l
        else:
            return no_repeat
    return no_repeat


inp = """# create a game:"""
optimized = auto_complete(inp, 128)
print(optimized)
