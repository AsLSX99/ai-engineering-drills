# 题库地图：12 个集合 × 51 道题

> 建队选方向用。权威归属以每题 `meta.json` 的 `collections` 字段为准（一题可属多集合）；下表是代表性题目的速查索引。查询命令：
> ```bash
> grep -l '"collections": \["<集合id>"\]' <课程仓库>/practice/*/meta.json
> ```

## 集合一览

| 集合 ID | 标题 | 练什么 | 代表题 |
|---|---|---|---|
| `math-foundations` | Math foundations | 矩阵运算、梯度、优化的 numpy 实现 | gradient-descent-linear-regression、pairwise-distances、power-iteration |
| `classical-ml` | Classical ML | 从方程写出来的传统模型 | logistic-regression、kmeans-step、gini-best-split |
| `deep-learning-core` | Deep learning core | 损失、反向传播、归一化 | mlp-backprop、softmax-cross-entropy、batch-norm、layer-norm-rms-norm、inverted-dropout、focal-loss |
| `optimizers` | Optimizers | 一次一条更新规则 | sgd-momentum、adam-step |
| `transformers-from-scratch` | Transformers from scratch | 注意力、多头、位置编码 | scaled-dot-product-attention、multi-head-split-merge、sinusoidal-positional-encoding、rope、grouped-query-attention、flash-attention-online-softmax |
| `llm-inference` | LLM inference | 分词、采样、缓存、量化 | bpe-merge-step、beam-search、top-k-top-p-sampling、kv-cache-append、lora-forward、int8-quantization、speculative-decoding-acceptance |
| `rl-basics` | RL basics | 回报、优势、目标函数 | discounted-returns、generalized-advantage-estimation、q-learning-update、ppo-clip-loss、grpo-advantages |
| `rag-building-blocks` | RAG building blocks | 稀疏/密集检索打分 | bm25、cosine-top-k、reciprocal-rank-fusion |
| `agent-building-blocks` | Agent building blocks | agent 循环周边的解析与校验 | tool-call-parser |
| `papers-to-code` | Papers to code | 按论文方程实现核心方法 | dpo-loss、clip-contrastive-loss、rectified-flow-loss、ddpm-forward-noising |
| `train-tiny-models` | Train tiny models | 带步数预算训练小模型到目标分数 | train-xor-mlp、train-spirals-mlp、train-softmax-blobs、train-sine-regression、train-char-bigram |
| `experiment-labs` | Experiment labs | 改一个变量、测效应、用数字回答 | lab-learning-rate-sweep、lab-bias-variance、lab-sampling-temperature、lab-quantization-bits、lab-sglang-l4-serving |

## 按目标推荐队列

**刚学完一课想巩固（最常见）**
- 学了损失函数 → softmax-cross-entropy → focal-loss
- 学了 Transformer → scaled-dot-product-attention → multi-head-split-merge → kv-cache-append
- 学了推理优化 → flash-attention-online-softmax → rope → int8-quantization
- 学了 RAG → bm25 → cosine-top-k → reciprocal-rank-fusion
- 学了 agent → tool-call-parser（后续题会随仓库增长）

**面试前突击（高频考点，按此顺序）**
1. softmax-cross-entropy（easy，必考）
2. mlp-backprop（反向传播手搓）
3. scaled-dot-product-attention（attention 一步）
4. kv-cache-append（推理工程）
5. adam-step（优化器）
6. gradient-descent-linear-regression（经典）

**从零补数学手感**
gradient-descent-linear-regression → pairwise-distances → power-iteration → gini-best-split

**挑战关（hard / 特殊类型）**
- research 类：dpo-loss、clip-contrastive-loss（对着论文方程写）
- train 类：train-spirals-mlp、train-char-bigram（预算内练到目标）
- lab 类：lab-sglang-l4-serving（跑实验答题）

## 难度与时长分布

- `easy` 多为单函数实现，`meta.json` 的 `minutes` 约 3-25
- `medium` 多为类 + 多方法 + 边界报错，约 25-45
- `hard` 多为完整机制（flash attention、DPO），约 45-120
- 排程以 `minutes` 为准，不靠猜
