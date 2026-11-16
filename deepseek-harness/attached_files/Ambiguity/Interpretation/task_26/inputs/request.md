# 本轮任务

There are N bags, labeled bag 1, bag 2, \ldots, bag N.
Bag i (1 \leq i \leq N) contains A_i stones.
Takahashi can perform the following operation any number of times, possibly zero:
Choose two bags A and B, and move stones from bag A into bag B.
Find the number of different possible values for the following after repeating the operation.
- B_1 \oplus B_2 \oplus \cdots \oplus B_N, where B_i is the final number of stones in bag i.
Here, \oplus denotes bitwise XOR.
About bitwise XOR
For non-negative integers a and b, the bitwise XOR a \oplus b is defined as follows:
In the binary representation of a \oplus b, the digit in the 2^k place (k \ge 0) is 1 if and only if exactly one of the digits in the 2^k place of a and b is 1; otherwise, it is 0.
For example, 3 \oplus 5 = 6 (in binary, 011 \oplus 101 = 110).
In general, for k non-negative integers x_1, x_2, \ldots, x_k, their bitwise XOR x_1 \oplus x_2 \oplus \cdots \oplus x_k is defined as (\cdots((x_1 \oplus x_2) \oplus x_3) \oplus \cdots) \oplus x_k, which does not depend on the order of x_1, x_2, \ldots, x_k.
It can be proved that under the constraints of this problem, the number of possible values is finite.
Input
The input is given from Standard Input in the following format:
N
A_1 A_2 \ldots A_N
Output
Print the number of different possible values for B_1 \oplus B_2 \oplus \cdots \oplus B_N after repeating the operation.
Constraints
- 2 \leq N \leq 12
- 1 \leq A_i \leq 10^{17}
- All input values are integers.

本轮适配：澄清需求后，只计算下列小实例并调用save_result提交答案数组；不需要生成完整算法程序。
