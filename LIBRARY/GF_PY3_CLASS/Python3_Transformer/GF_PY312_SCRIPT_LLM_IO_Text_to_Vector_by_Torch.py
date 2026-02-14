# GF_PY312_SCRIPT_LLM_IO_Text_to_Vector_by_Torch.py
# Create by GF 2025-03-12

# ##################################################

import json
import sys
import torch
import transformers
# ..................................................
AutoTokenizer = transformers.AutoTokenizer

# ##################################################

args = sys.argv

# args[0] 为脚本本身的名称。
# args[1:] 为脚本后面跟随的参数列表。
# 在命令行中使用命令 python script.py arg1 arg2 arg3 来运行脚本并传递参数。

# ##################################################

FILE = open(args[2], mode='r', encoding="utf-8")
TEXT = FILE.read()

JSON_Dataset = json.loads(TEXT)

# Expected JSON Format Example:
# [
#   {"input": "天王盖地虎", "output": "小鸡炖蘑菇"},
#   {"input": "宫保鸡丁", "output': "鱼香肉丝"},
#   {"input": "忧劳 可以兴国", "output": "闭目可以养神"}
# ]

print("[Message] Read %d Rows of JSON Dataset ..." % len(JSON_Dataset))
print("...")

print("[Message] Preview of JSON Dataset in The First 1 Lines:")
print("[\n  %s\n  ...\n]" % str(JSON_Dataset[0]))
print("...")

# ##################################################

# AutoTokenizer 加戟模型可联网拉取, 也可以本地加载。
# 也可外部拉取, 例如:
# git clone https://huggingface.co/deepseek/deepseek-lim-7b

tokenizer = AutoTokenizer.from_pretrained(args[1])

# ##################################################

def one_time_function_tokenize(examples):

    text_list = [
        "<｜begin▁of▁sentence｜>你是一个助手<｜User｜>%s<｜Assistant｜>%s<｜end▁of▁sentence｜>" % (i["input"], i["output"])
        for i in examples
    ]

    tokenized = tokenizer(
        text_list,
        truncation=True,
        return_tensors="pt", # 返回 torch.Tensor 数据类型 (PyTorch 张量)
        max_length=128,
        padding="max_length" # 手动填充到固定长度 (例如 128)
    )

    return tokenized

# ##################################################

tokenized = one_time_function_tokenize(JSON_Dataset)

# ##################################################

formated_dataset = {
    # 'input': [],
    # 'output': [],
    "input_ids": tokenized["input_ids"].squeeze(),
    "attention_mask": tokenized["attention_mask"].squeeze(),
    # "labels": []
}

# 添加 labels 字段 (直接复制 input_ids)
formated_dataset["labels"] = formated_dataset["input_ids"]
# 为什么需要 labels 字段?
# 因果语言模型 (如 LLaMA、GPT) 的训练目标是预测下一个 token, 因此:
# 输入 (input_ids): [token_1, token_2, ..., token_n]
# 标签 (labels): [token_2, ..., token_n, token_{n+1}]
# 但在实际实现中, 通常直接将 labels 设为与 input_ids 相同, 模型内部会自动计算位移损失 (shifted loss)。

# ##################################################

print("[Message] Saved as Tensor dataset ...")
print("...")

torch.save(formated_dataset, "./DATASET_for_LLM_AI_LoRA_IO_Text_Vector.pt")

# ##################################################

print("Processing Completed")

# EOF Signed by GF.
