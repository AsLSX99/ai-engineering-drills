# ai-engineering-drills

> 开源 AI 工程**"从零手搓"特训教练**（SKILL）——驱动 [AI Engineering from Scratch](https://github.com/rohitg00/ai-engineering-from-scratch) 的 `practice/` 题库：**51 道自动判分练习**，从 softmax、反向传播到 KV cache、Flash Attention、LoRA、PPO、BM25，配防剧透机制、分层提示、四层判分复盘和间隔重复排期。

"看完教程觉得懂了，一写就废"——这是所有技术学习的死穴。课程仓库给你 51 道带判分器的题，本 Skill 补上教练该干的事：**选题、守规矩、卡节奏、逼复盘、安排复习**。

## 与"读课型"学习的关系

| | 学习型 Skill（上课） | 本 Skill（特训） |
|---|---|---|
| 管什么 | 输入：读课、理解、考核 | 输出：写代码、过判分、抗遗忘 |
| 单位 | 一节课 | 一道题 |
| 过关标准 | 复述 + 解释 + 3 题 | 判分器四层全绿 + 复盘三件套 |
| 记忆机制 | 项目验收 | 间隔重复（1→3→7→14→30 天） |

两者独立，可只装一个，可同时装，互不依赖。

## 仓库结构

```
ai-engineering-drills/
├── SKILL.md                        # 主文档：建队模式 + 训练模式 + 6 条铁律
├── README.md
├── LICENSE
├── references/
│   ├── collections.md              # 12 集合 × 51 题地图 + 按目标推荐队列
│   ├── drill-protocol.md           # 特训循环、判分四层、失败诊断表、变异体挑战
│   └── task-kinds.md               # implement/research/train/lab 四类任务差异
├── templates/
│   ├── drill-plan.md               # 训练计划（目标/队列/里程碑/规则）
│   └── drill-log.md                # 特训日志（重要场次的证据归档）
└── scripts/
    └── drill.py                    # 队列 + 间隔重复记账（纯标准库）
```

## 题库长什么样

每道题一个目录（`practice/<id>/`），10 个文件各司其职：

| 文件 | 作用 |
|---|---|
| `problem.md` | 题面：任务、输入输出表、约束、示例 |
| `starter.py` | 函数签名骨架，全是 `NotImplementedError` |
| `tests.py` | **四层自动判分**：Examples → Properties → Edge cases → Reference |
| `hints.md` | 2-5 条分级提示，从点拨到关键思路 |
| `solution.py` / `notes.md` | 参考解与通关笔记——**通过后才解锁** |
| `mutants/` | 3-6 个故意写错的解，判分必须全部拒收 |
| `meta.json` | 难度、预计分钟、出处课、所属集合、时间限制 |

四类任务：`implement`（写函数）、`research`（按论文方程实现）、`train`（预算内训练到目标指标）、`lab`（跑实验用数字答题）。

## 如何使用

**① 作为 Agent 技能安装**
把本仓库整个目录克隆/复制到你的 AI Agent 识别技能的目录下，目录名保持 `ai-engineering-drills`，确保 `SKILL.md` 直接位于该目录内。同时把[课程仓库](https://github.com/rohitg00/ai-engineering-from-scratch)克隆到任意位置——脚本会自动向上查找它的 `practice/` 目录。

**② 直接当开场指令**
把 `SKILL.md` 全文发给你的 Agent，再说一句"带我练题"。

**③ 只用记账脚本**
`scripts/drill.py` 与课程无关，任何"有一批任务要间隔重复"的场景都能用：
```bash
python drill.py add softmax-cross-entropy kv-cache-append adam-step
python drill.py next
python drill.py log softmax-cross-entropy --result pass --hints 1 --minutes 18
python drill.py status
```

## 环境准备

| 依赖 | 用途 | 获取方式 |
|---|---|---|
| **AI Agent**（Claude Code / Codex / 其他支持 SKILL.md 的宿主） | 执行特训协议 | 你现有的工具链 |
| **课程仓库** | 题库与判分器 | `git clone --depth 1 https://github.com/rohitg00/ai-engineering-from-scratch.git` |
| **Python ≥ 3.9 + numpy** | 跑判分（判分器依赖 numpy） | `pip install numpy` |

判分命令（Skill 会替你拼好）：

```bash
python <课程仓库>/scripts/practice/run.py <题id> <你的代码.py>
```

输出按四层组织，每条失败带 `expected / actual / meaning`（这条检查在防什么错）——**让失败信息教你**。

## 核心机制

### 防剧透（最重要的一条）
`solution.py`、`notes.md`、`mutants/` 在全绿之前对你和 Agent 都封印。提示走 `hints.md` 分级节奏：
**读失败信息自定位 → Hint 1 → Hint 2 → … → 4 条用尽才开放参考解第一段**，且每给一条提示，你要先讲"这条对应我代码哪一行"。开放参考解的题会被标记，**2 天后强制重考**（遮住参考解重写）。

### 判分四层（按层读失败）
| 层 | 挂了意味着 |
|---|---|
| Examples | 根本逻辑写错 |
| Properties | 公式有偏差（漏 scale、漏 mask、数值不稳） |
| Edge cases | 边界没想、该抛的错没抛 |
| Reference | 细节错位（off-by-one、覆盖顺序、精度） |

### 通关三件套（缺一不算 pass）
1. 对照 `solution.py` 说差距
2. 读 `notes.md` 用自己的话讲"为什么这样写才对"
3. **变异体挑战**：逐个 `mutant` 说出"哪一层哪条检查会拒收它"——说不上就是知识盲区

### 间隔重复（drill.py 自动排期）
```
pass +1天 → +3天 → +7天 → +14天 → +30天 → 毕业
hints 用 3-4 条 → 间隔减半        hints 超限 → +2天重考
fail → +1天                        连续 2 次 fail → 降档换题
```

### 会话节奏
每次会话最多 2 题；按 `meta.json` 的 `minutes` 时间盒，超时 50% 未绿记 fail 明天续；断更不补作业，从到期队列自然恢复。

## 快速开始

1. 克隆课程仓库：`git clone --depth 1 https://github.com/rohitg00/ai-engineering-from-scratch.git`
2. `pip install numpy`
3. 安装本 Skill（或把 `SKILL.md` 发给你的 Agent）
4. 说 **"带我练题"** / **"今天练什么"** → 走建队模式，拿到 `drill-plan.md` 和 5-8 道起手题
5. 之后每次：`next` 取题 → 写 → 判分 → 分层提示 → 全绿 → 复盘三件套 → 自动排期

## 推荐起手队列

**面试突击（6 题）**：`softmax-cross-entropy` → `mlp-backprop` → `scaled-dot-product-attention` → `kv-cache-append` → `adam-step` → `gradient-descent-linear-regression`

**学完 Transformer 巩固（3 题）**：`scaled-dot-product-attention` → `multi-head-split-merge` → `kv-cache-append`

完整 12 集合地图见 `references/collections.md`。

## 设计原则

1. **代码从用户键盘出来**——Agent 不代写，口述代写也算抄
2. **判分器是唯一裁判**——"我觉得对了"不是证据
3. **失败信息是教材**——先读 `meaning:` 自定位，提示永远慢一拍
4. **封印到通关**——参考解和变异体提前看，训练就失效了
5. **复盘才算完成**——三件套走完才 `log pass`
6. **抗遗忘靠排期**——学完不复习，两周后归零；间隔重复自动算

## 常见问题

**Q：和课程仓库自带的 skills 什么关系？**
互补。本 Skill 是独立实现的训练协议与记账工具，不依赖其内部状态格式，可单独用、可裁剪。

**Q：题目会更新吗？**
会——Skill 不复制任何题目，题库以课程仓库 `practice/` 为准，上游 `git pull` 即同步。本仓库的 `collections.md` 是速查索引，权威归属以每题 `meta.json` 为准。

**Q：只有 Python 会用，numpy 没学过怎么办？**
题面和判分器会替你挡住大部分 numpy 细节；卡在 numpy 用法上时，按协议回 `meta.json` 的 `lesson` 指向的那节课补读。

**Q：进度文件要提交到 git 吗？**
建议提交（复盘资产）；想私有就加进 `.gitignore`。

**Q：能用在其他题库吗？**
`drill.py`（队列+间隔重复）完全通用；协议层换掉 `collections.md` 即可套任何带自动判分的练习集。

## 致谢

- 题库、判分器与全部课件：[rohitg00/ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch)（MIT）
- 本仓库只提供训练协议与记账工具，题目与判分版权归原作者所有

## License

[MIT](./LICENSE)
