from tokenizers import ByteLevelBPETokenizer
from transformers import DataCollatorForLanguageModeling, \
    GPT2Config, GPT2LMHeadModel, GPT2Tokenizer, \
    Trainer, TrainingArguments
from datasets import load_dataset

paths = ['code_text_data.txt']
TRAIN_BASE = False

if TRAIN_BASE:
    tokenizer = ByteLevelBPETokenizer()

    tokenizer.train(files=paths, vocab_size=52_000, min_frequency=2, special_tokens=[
        "<s>",
        "<pad>",
        "</s>",
        "<unk>",
        "<mask>",
    ])

    tokenizer.save_model("tokenizer")

tokenizer = GPT2Tokenizer.from_pretrained('tokenizer')

tokenizer.add_special_tokens({
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>"
})

config = GPT2Config(
    vocab_size=tokenizer.vocab_size,
    bos_token=tokenizer.bos_token_id,
    eos_token=tokenizer.eos_token_id,
    pad_token=tokenizer.pad_token_id,
    mask_token=tokenizer.mask_token_id
)
# model = GPT2LMHeadModel(config)  # 从头训练
model = GPT2LMHeadModel.from_pretrained("GPyT_3/checkpoint-33200-loss=1.13").to("cuda")  # 接续训练
data = load_dataset("text", data_files=paths)
print('successfully loaded dataset!')


def encode(lines):
    """

    Args:
        lines: 输入的行

    Returns:
        返回token化后的结果
    """
    token = tokenizer(lines['text'], add_special_tokens=True,
                      truncation=True, max_length=512)
    return token


data.set_transform(encode)
print(data)
data = data['train']

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.15
)

training_args = TrainingArguments(
    output_dir="GPyT_3/",
    overwrite_output_dir=False,
    num_train_epochs=20,
    per_device_train_batch_size=10,
    save_steps=100,
    save_total_limit=10,
    prediction_loss_only=False,
    remove_unused_columns=False,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=data
)

trainer.train()
trainer.save_model("GPyT_3")
