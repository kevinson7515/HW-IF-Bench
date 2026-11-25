# 端侧部署论文摘记

- AWQ 通过激活分布识别显著权重并缩放，做低比特仅权重推理；论文包含 TinyChat 的部署实验。https://arxiv.org/abs/2306.00978
- LLM-Pruner 研究依赖感知结构剪枝，以梯度信息估计重要性，并使用 LoRA 恢复性能。模型参数减少、实际时延及任务精度须分别比较。https://arxiv.org/abs/2305.11627
- MiniLLM 使用反向 KL 的生成式蒸馏目标并设计训练策略。学生模型输出质量与不同解码设置关联。https://arxiv.org/abs/2306.08543
- FlashAttention 以分块减少 GPU 高带宽显存和片上 SRAM 间的读写，执行精确 attention。原论文中的 GPU 结果受硬件和序列长度约束。https://arxiv.org/abs/2205.14135


## 可核验来源

- https://arxiv.org/abs/2306.00978
- https://arxiv.org/abs/2305.11627
- https://arxiv.org/abs/2306.08543
- https://arxiv.org/abs/2205.14135
