# 50 条 Agent 评测输入

任务按 1–50 编号。1–17 使用已确定的上一版题目、group_id 和附件，18–50 使用最近整理的题目和附件。所有 503 条附件路径均相对于本目录。第 12–16 题的空附件列表是原配置。

## 准备输入

解压后进入 baseline_fingerprint_50/。用 Python 3.12 或更新版本运行：

```text
python prepare_task.py --verify
python prepare_task.py --all --workspace runs/all_50
```

把生成的任务目录交给 Agent，并以 prompt.md 作为用户输入。仓库和模拟数据会展开到各自工作区。评分材料在 evaluation_only/，只由评测方读取。工作区目录应为新目录。

1–17 的原评测工具、网络或运行环境要求沿用已确定的配置。18–50 的任务资料均随包提供。26–31 的客服题在文件模式下交付处理计划和答复，执行模拟工具需配置 τ²-bench。编码跑分依赖相应的运行环境。source_manifest_50.json 记录来源及附件哈希。
