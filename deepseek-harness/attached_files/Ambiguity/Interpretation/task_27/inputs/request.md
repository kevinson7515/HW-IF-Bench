# 本轮任务

You are given a grid of H rows and W columns.
Let (i,j) denote the cell at row i (1 \leq i \leq H) from the top and column j (1 \leq j \leq W) from the left.
The state of the grid is represented by H strings S_1, S_2, \ldots, S_H, each of length W. 
Takahashi wants to paint each not-yet-painted cell so that all the black cells form a rectangle.
More precisely, he wants there to exist a quadruple of integers (a,b,c,d) (1 \leq a \leq b \leq H, 1 \leq c \leq d \leq W) such that:
For each cell (i,j) (1 \leq i \leq H, 1 \leq j \leq W),
if a \leq i \leq b and c \leq j \leq d, the cell is black;
otherwise, the cell is white.
Determine whether this is possible.
Input
The input is given from Standard Input in the following format:
H W
S_1
S_2
\vdots
S_H
Output
If it is possible to paint all the not-yet-painted cells so that the black cells form a rectangle, print Yes; otherwise, print No.
Constraints
- 1 \leq H, W \leq 1000
- H and W are integers.
- Each S_i is a string of length W consisting of #, ., ?.
- There is at least one cell that is already painted black.

本轮适配：澄清需求后，只计算下列小实例并调用save_result提交答案数组；不需要生成完整算法程序。
