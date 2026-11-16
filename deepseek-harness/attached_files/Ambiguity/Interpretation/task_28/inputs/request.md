# 本轮任务

You are given three integer sequences of length N, namely A=(A_1,A_2,\ldots,A_N), B=(B_1,B_2,\ldots,B_N), and C=(C_1,C_2,\ldots,C_N), and an integer K.
For each of the N^3 choices of integers i,j,k (1\leq i,j,k\leq N), compute the value A_iB_j + B_jC_k + C_kA_i. Among all these values, find the K-th value.
Input
The input is given from Standard Input in the following format:
N K
A_1 A_2 \ldots A_N
B_1 B_2 \ldots B_N
C_1 C_2 \ldots C_N
Output
Print the answer.
Constraints
- 1\leq N \leq 2\times 10^5
- 1\leq K \leq \min(N^3,5\times 10^5)
- 1\leq A_i,B_i,C_i \leq 10^9
- All input values are integers.

本轮适配：澄清需求后，只计算下列小实例并调用save_result提交答案数组；不需要生成完整算法程序。
