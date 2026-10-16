# 12 栈

> LeetCode Hot 100 个人题库 · Python 3 标准参考答案

## 20. 有效的括号（简单）
**核心模式：** 栈 / 匹配

**题意摘要：** 判断括号字符串是否正确闭合并保持类型匹配。

**标准思路：** 左括号入栈；遇到右括号时要求栈非空且栈顶是对应左括号。扫描结束后栈必须为空。

```python
class Solution:
    def isValid(self, s: str) -> bool:
        mp = {')':'(', ']':'[', '}':'{'}
        stack = []
        for ch in s:
            if ch in mp:
                if not stack or stack.pop() != mp[ch]:
                    return False
            else:
                stack.append(ch)
        return not stack
```

**复杂度：** 时间 O(n)，空间 O(n)。

**关键易错点：** 右括号到来时必须检查空栈；最后还要检查是否残留左括号。

## 155. 最小栈（中等）
**核心模式：** 辅助栈 / 同步最小值

**题意摘要：** 实现 push/pop/top/getMin，所有操作 O(1)。

**标准思路：** 维护普通栈和 min_stack；每次 push 同步压入“截至当前位置的最小值”，pop 时两栈同步弹出。

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.mins = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.mins:
            self.mins.append(val)
        else:
            self.mins.append(min(val, self.mins[-1]))

    def pop(self) -> None:
        self.stack.pop()
        self.mins.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.mins[-1]
```

**复杂度：** 每个操作 O(1)，空间 O(n)。

**关键易错点：** 若辅助栈只在更小时入栈，则遇到重复最小值时要特别处理；同步栈更稳。

## 394. 字符串解码（中等）
**核心模式：** 栈 / 状态保存

**题意摘要：** 把形如 k[encoded] 的字符串展开，支持嵌套。

**标准思路：** 扫描字符：数字累积倍数；遇到 [ 把当前字符串和倍数入栈并重置；遇到 ] 弹出上一层并拼接；普通字符加入当前字符串。

```python
class Solution:
    def decodeString(self, s: str) -> str:
        stack = []
        cur = ''
        num = 0
        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)
            elif ch == '[':
                stack.append((cur, num))
                cur = ''
                num = 0
            elif ch == ']':
                prev, k = stack.pop()
                cur = prev + cur * k
            else:
                cur += ch
        return cur
```

**复杂度：** 时间 O(输出长度)，空间 O(嵌套深度 + 输出临时空间)。

**关键易错点：** 倍数可能是多位数，需 num = num*10 + digit。

## 739. 每日温度（中等）
**核心模式：** 单调递减栈

**题意摘要：** 对每一天，返回还要等几天才会遇到更高温度；没有则 0。

**标准思路：** 栈保存尚未找到更高温度的下标，且对应温度单调递减。新温度更高时持续弹栈并填写距离。

```python
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        ans = [0] * n
        stack = []
        for i, t in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < t:
                j = stack.pop()
                ans[j] = i - j
            stack.append(i)
        return ans
```

**复杂度：** 时间 O(n)，空间 O(n)。

**关键易错点：** “下一个更大元素”是单调栈最经典识别信号。

## 84. 柱状图中最大的矩形（困难）
**核心模式：** 单调递增栈 + 哨兵

**题意摘要：** 给定柱高，求能形成的最大矩形面积。

**标准思路：** 维护下标单调递增栈。遇到更矮柱时，弹出的柱高 h 以当前位置为右边界、弹栈后的新栈顶为左边界。两端加 0 哨兵统一结算。

```python
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        arr = [0] + heights + [0]
        stack = [0]
        ans = 0
        for i in range(1, len(arr)):
            while arr[stack[-1]] > arr[i]:
                h = arr[stack.pop()]
                width = i - stack[-1] - 1
                ans = max(ans, h * width)
            stack.append(i)
        return ans
```

**复杂度：** 时间 O(n)，空间 O(n)。

**关键易错点：** 宽度公式 i-stack[-1]-1 是核心；左右 0 哨兵可消除边界特判。
