# 四类任务的差异化处理

> 每题 `meta.json` 的 `kind` 字段：`implement`（默认）/ `research` / `train` / `lab`。四类共用同一套文件结构和四层判分，差别在"用户写什么"和"判分测什么"。

## implement（默认，约 40 题）

- **用户写**：一个函数或小类（课上从零构建过的那块代码）
- **判分**：示例 + 性质 + 边界 + 与参考解对照
- **节奏**：标准循环，按 `minutes` 时间盒
- 例：`kv-cache-append`、`softmax-cross-entropy`、`adam-step`

## research（对着论文写）

- **用户写**：论文的核心方法实现
- **判分**：按论文声明的方程与性质出题（例如"DPO 在 policy=reference 时 loss 等于 log 2"）
- **额外材料**：`meta.json` 有 `paper` 字段（标题/作者/年份/arXiv 链接）
- **节奏**：
  1. 先读 `problem.md` 里给出的方程——**方程就是 spec，不许自己发挥**
  2. 允许读论文摘要帮助理解，但代码必须对着 `problem.md` 的方程写
  3. 时间盒 ×1.5（读论文本来就慢）
- 例：`dpo-loss`、`clip-contrastive-loss`、`rectified-flow-loss`、`ddpm-forward-noising`

## train（预算内训练到目标）

- **用户写**：一个 `train(...)` 训练循环
- **判分**：用题目**不告知的种子**在保留集上测指标；同时检查步数不超预算、同种子可复现、输入未被篡改
- **关键约束**：
  - `meta.json` 的 `budget.steps` 是硬上限，超了直接挂
  - `meta.json` 的 `target.value` 是必须达到的指标线（参考解留有余量）
  - 数据生成器在 `support.py`（题目提供，用户可读）
  - 训练中调用 `practice_check.report(step, loss)` 记录曲线
- **节奏**：
  1. 先跑通 1 个 epoch 看 loss 曲线形状对不对，再调预算内配置
  2. 时间盒 ×2（训练本身要跑）
  3. 不达标时的排查顺序：学习率符号 → 是否漏了 bias 更新 → 是否没 shuffle → 数据标准化
- 例：`train-xor-mlp`、`train-spirals-mlp`、`train-char-bigram`

## lab（跑实验答题）

- **用户写**：不是代码主体——跑一段实验，改一个变量、测效应，**用数字回答问题**
- **判分**：答案与参考运行的结果比对
- **节奏**：
  1. 先读清楚"要改哪个变量、要测什么、答案是什么格式"
  2. 实验要可复现：记下种子、配置、命令
  3. 答案必须带数字和单位，"大概变好了"不算
  4. 时间盒 ×1.5
- 例：`lab-learning-rate-sweep`、`lab-bias-variance`、`lab-sampling-temperature`、`lab-quantization-bits`、`lab-sglang-l4-serving`

## 排程差异速查

| kind | 时间盒 | 失败降级 | 重考方式 |
|---|---|---|---|
| implement | ×1 | 降难度 | 遮住 solution 重写 |
| research | ×1.5 | 回对应课补方程理解 | 重新对齐方程再写 |
| train | ×2 | 按排查顺序修，不换题（换题=白练） | 同配置复跑达标 |
| lab | ×1.5 | 检查实验设计（变量没控住） | 重跑实验报数 |
