# GF_PY312_SCRIPT_LLM_AI_LoRA_by_HFTF4.py
# Create by GF 2025-03-12

# ##################################################

import datasets
import peft
import torch
import transformers
import sys
# ..................................................
AutoTokenizer        = transformers.AutoTokenizer
AutoModelForCausalLM = transformers.AutoModelForCausalLM # Model Loading.
Dataset              = datasets.Dataset
Trainer              = transformers.Trainer
TrainingArguments    = transformers.TrainingArguments    # Training Parameters in Optimize -General.
LoraConfig           = peft.LoraConfig                   # Training Parameters in Configure -LoRA.
get_peft_model       = peft.get_peft_model
TaskType             = peft.TaskType
args                 = sys.argv
# ..................................................
Base_Model_Path      = args[1]
Train_Data_Path      = args[2]

# ##################################################

print("[Message] Traning Dataset Loading in Progress ...")
print("...")

Train_Dataset = torch.load(Train_Data_Path)
Train_Dataset = Dataset.from_dict(Train_Dataset)

print("[Message] Preview of Traning Dataset in The First 1 Lines:")
print(Train_Dataset[0])
print("...")

# ##################################################

# AutoTokenizer 加戟模型可联网拉取, 也可以本地加载。
# 也可外部拉取, 例如:
# git clone https://huggingface.co/deepseek/deepseek-lim-7b

tokenizer = AutoTokenizer.from_pretrained(Base_Model_Path)

# ##################################################

print("[Message] Model Loading in Progress ...")
print("...")

model = AutoModelForCausalLM.from_pretrained(
    Base_Model_Path,            # 基础模型路径
    torch_dtype=torch.bfloat16, # 半精度节省显存
    device_map="auto"           # 多卡自动分配
)


model.enable_input_require_grads()
# model.enable_input_require_grads() 是 Hugging Face Transformers 库中的一个方法,
# 用于确保模型的输入张量 (input tensors) 在反向传播时计算梯度。
# 注意: 开启梯度检查点时, 需要执行该方法。
# - 具体作用:
#   1. 默认行为:
#       在 PyTorch 中, 输入张量通常不会自动计算梯度 (requires_grad=False),
#       因为输入通常是数据，而不是需要优化的参数。
#   2. 启用梯度计算:
#       调用 enable_input_require_grads() 后,
#       模型的输入张量会被标记为需要计算梯度 (requires_grad=True),
#       这样在反向传播时, 输入张量的梯度会被保留。
# - 使用场景:
#   1. 自定义训练逻辑:
#       如果你需要在训练过程中对输入数据进行某种优化 (例如对抗训练、输入扰动等),
#      可能需要输入张量的梯度。
#   2. 特定任务需求:
#       某些任务 (如生成对抗网络 GANs 或某些强化学习任务) 可能需要对输入数据进行梯度计算。

print("[Message] Model Information:")
print(model) # 输出模型信息
print("...")

# 预期输出:
# >>> print(model)
# Qwen2ForCausalLM(
#   (model): Qwen2Model(
#     (embed_tokens): Embedding(151936, 1536)
#     (layers): ModuleList(
#       (0-27): 28 x Qwen2DecoderLayer(
#         (self_attn): Qwen2Attention(
#           (q_proj): Linear(in_features=1536, out_features=1536, bias=True)
#           (k_proj): Linear(in_features=1536, out_features=256, bias=True)
#           (v_proj): Linear(in_features=1536, out_features=256, bias=True)
#           (o_proj): Linear(in_features=1536, out_features=1536, bias=False)
#         )
#         (mlp): Qwen2MLP(
#           (gate_proj): Linear(in_features=1536, out_features=8960, bias=False)
#           (up_proj): Linear(in_features=1536, out_features=8960, bias=False)
#           (down_proj): Linear(in_features=8960, out_features=1536, bias=False)
#           (act_fn): SiLU()
#         )
#         (input_layernorm): Qwen2RMSNorm((1536,), eps=1e-06)
#         (post_attention_layernorm): Qwen2RMSNorm((1536,), eps=1e-06)
#       )
#     )
#     (norm): Qwen2RMSNorm((1536,), eps=1e-06)
#     (rotary_emb): Qwen2RotaryEmbedding()
#   )
#   (lm_head): Linear(in_features=1536, out_features=151936, bias=False)
# )
#
# 其中的 self_attn: Qwen2Attention
# - 这是一个自注意力模块，命名为 Qwen2Attention。
# - 它包含了 4 个线性变换层 (Linear), 分别用于计算查询(Query), 键(Key),
#   值(Value) 和 输出(Output)。
# 其中的 mlp: Qwen2MLP
# - 这是一个多层感知机模块, 命名为 Qwen2MLP。
# - 它包含了 3 个线性变换层 (Linear) 和 1 个激活函数 (SiLU)
# 注意其中的 q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj
# - 这几层权重就是我们要微调学习的参数。

# ##################################################

Training_Modules = [
    "q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"
]

print("[Message] Selected Training Modules:")
print(Training_Modules)
print("...")

print("[Message] Training Parameters in Configure -LoRA ...")
peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    target_modules=Training_Modules,
    inference_mode=False,  # 训练模式
    r=8,                   # Lora 的秩 (rank), 表示低秩矩阵的维度
    lora_alpha=32,         # LoRA 的缩放因子, 通常随 r 一起调整
    lora_dropout=0.1       # LoRA 层的 dropout 概率
)
model = get_peft_model(model, peft_config)
model.print_trainable_parameters()
print("...")
	
# 预期输出:
# trainable params: 9,232,384 || all params: 1,786,320,384 || trainable%: 0.5168

# ##################################################

print("[Message] Training Parameters in Optimize -General ...")
print("...")

training_args = TrainingArguments(
    output_dir="./tuning_checkpoint",
    per_device_train_batch_size=2,  # 3090 显卡建议设为 4
    gradient_accumulation_steps=2,  # 显存不足时增大此值
    logging_steps=20,
    num_train_epochs=2,
    save_steps=25,
    save_total_limit=2,
    learning_rate=1e-4,
    save_on_each_node=True,
    gradient_checkpointing=True
)

# ##################################################

data_collator = transformers.DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

print("[Message] Model Training in Progress ...")
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=Train_Dataset,
    data_collator=data_collator,  # 显式定义数据动态填充逻辑
    tokenizer=tokenizer
)
trainer.train()
print("...")

# 保存 LoRA 权重
model.save_pretrained("./tuning_weights")
tokenizer.save_pretrained("./tuning_tokenizer")

# ##################################################

print("Processing Completed")

# EOF Signed by GF.
