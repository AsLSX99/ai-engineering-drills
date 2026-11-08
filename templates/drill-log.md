# 特训日志（drill-log.md）

> 每次会话结束追加一节。**重要场次才写**（首次攻克 hard、hints-exceeded 重考、变异体挑战、连续失败诊断）——常规题以 `drill-progress.json` 的机器记录为准。

---

## [YYYY-MM-DD] · 题目 [id]（[难度] · [kind]） · 结果 [pass / fail]

**耗时**：[X 分钟 / 时间盒 Y 分钟] · **hints**：[0-4 / exceeded]

### 题意复述（过关才动笔）

- 输入/输出/约束：[一句话]
- 易错点（他自己列的）：[如"容量满时要抛错且状态不变"]

### 起手方案

[数据结构 + 主流程 + 边界清单，两三行]

### 判分记录

| 层 | 结果 | 失败的 meaning（摘录） |
|---|---|---|
| Examples | | |
| Properties | | |
| Edge cases | | |
| Reference | | |

最终：`X of Y checks pass.`

### 提示与卡点

- 用到第几条 hint：[N]，对应改了哪行：[一句话]
- 病根（对照失败诊断表）：[哪一行 / 不适用]

### 复盘三件套

- [ ] 对照 solution 的差距：[结构/边界/numpy 用法]
- [ ] notes 用自己的话：[为什么这样写才对]
- [ ] 变异体挑战：[N 个 mutant 说中 M 个，没说中的是……]

### 记账

```
python scripts/drill.py log [id] --result [pass|fail] --hints [N|exceeded] --minutes [X]
```

下次到期：[日期]（脚本自动排期）

---
