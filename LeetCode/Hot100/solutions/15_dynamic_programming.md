# 15 动态规划

> LeetCode Hot 100 个人题库 · Python 3 标准参考答案

## 70. 爬楼梯（简单）
**核心模式：** 一维 DP / Fibonacci

**题意摘要：** 每次爬 1 或 2 阶，求到第 n 阶的方法数。

**标准思路：** 到第 i 阶只能从 i-1 或 i-2 来，因此 dp[i]=dp[i-1]+dp[i-2]；用两个变量滚动。

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        a, b = 1, 2
        for _ in range(3, n + 1):
            a, b = b, a + b
        return b
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 先明确 dp[i] 的定义与 dp[1]/dp[2] 初值。

## 118. 杨辉三角（简单）
**核心模式：** 二维递推

**题意摘要：** 生成杨辉三角前 numRows 行。

**标准思路：** 每行两端为 1，中间位置等于上一行相邻两个数之和。

```python
class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        ans = []
        for i in range(numRows):
            row = [1] * (i + 1)
            for j in range(1, i):
                row[j] = ans[i - 1][j - 1] + ans[i - 1][j]
            ans.append(row)
        return ans
```

**复杂度：** 时间 O(numRows²)，空间 O(numRows²)（输出）。

**关键易错点：** 第 i 行长度为 i+1（这里 i 从 0 开始）。

## 198. 打家劫舍（中等）
**核心模式：** 一维 DP / 相邻互斥

**题意摘要：** 不能偷相邻房屋，求最大可偷金额。

**标准思路：** 到当前房屋 i 时，要么不偷：沿用上一状态；要么偷：得到前前状态+当前金额。用 prev2/prev1 滚动。

```python
class Solution:
    def rob(self, nums: List[int]) -> int:
        prev2 = 0
        prev1 = 0
        for x in nums:
            prev2, prev1 = prev1, max(prev1, prev2 + x)
        return prev1
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 状态转移是 max(不偷当前, 偷当前)，典型“相邻不能同时选”。

## 279. 完全平方数（中等）
**核心模式：** 完全背包 / 最短组合数

**题意摘要：** 用若干完全平方数凑出 n，求最少数量。

**标准思路：** dp[x] 表示凑出 x 的最少个数。对每个 x 枚举不超过 x 的平方数 j²，转移 dp[x]=min(dp[x], dp[x-j²]+1)。

```python
class Solution:
    def numSquares(self, n: int) -> int:
        dp = [0] + [float('inf')] * n
        squares = [i * i for i in range(1, int(n ** 0.5) + 1)]
        for x in range(1, n + 1):
            for sq in squares:
                if sq > x:
                    break
                dp[x] = min(dp[x], dp[x - sq] + 1)
        return dp[n]
```

**复杂度：** 时间 O(n√n)，空间 O(n)。

**关键易错点：** 也可把 0..n 看作图节点做 BFS；DP 更统一。

## 322. 零钱兑换（中等）
**核心模式：** 完全背包 / 最少硬币数

**题意摘要：** 硬币可无限次使用，求凑成 amount 的最少硬币数；无法凑成返回 -1。

**标准思路：** dp[x] 表示凑出金额 x 的最少硬币数，初始 inf，dp[0]=0。对每个金额枚举 coin 更新 dp[x-coin]+1。

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        for x in range(1, amount + 1):
            for coin in coins:
                if coin <= x:
                    dp[x] = min(dp[x], dp[x - coin] + 1)
        return -1 if dp[amount] == float('inf') else dp[amount]
```

**复杂度：** 时间 O(amount·len(coins))，空间 O(amount)。

**关键易错点：** 目标是“最少数量”而不是“方案数”；状态含义不同，转移形式也不同。

## 139. 单词拆分（中等）
**核心模式：** DP / 前缀可达

**题意摘要：** 判断字符串能否由字典中的一个或多个单词拼接而成，单词可重复使用。

**标准思路：** dp[i] 表示 s[:i] 能否拆分。若存在 j<i，使 dp[j] 为真且 s[j:i] 在字典中，则 dp[i]=True。

```python
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        words = set(wordDict)
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True
        max_len = max(map(len, wordDict)) if wordDict else 0
        for i in range(1, n + 1):
            for j in range(max(0, i - max_len), i):
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break
        return dp[n]
```

**复杂度：** 最坏时间 O(n²·切片代价)，空间 O(n+字典)。

**关键易错点：** dp[0]=True 是空前缀的关键基例。

## 300. 最长递增子序列（中等）
**核心模式：** 贪心 + 二分 tails

**题意摘要：** 求严格递增子序列的最大长度。

**标准思路：** tails[i] 保存“长度为 i+1 的递增子序列能达到的最小尾值”。对每个 x，用 lower_bound 找第一个 >=x 的位置替换；若不存在则追加。

```python
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        tails = []
        for x in nums:
            l, r = 0, len(tails)
            while l < r:
                m = (l + r) // 2
                if tails[m] < x:
                    l = m + 1
                else:
                    r = m
            if l == len(tails):
                tails.append(x)
            else:
                tails[l] = x
        return len(tails)
```

**复杂度：** 时间 O(n log n)，空间 O(n)。

**关键易错点：** tails 本身通常不是某条实际 LIS，只维护各长度的最小可能尾值。

## 152. 乘积最大子数组（中等）
**核心模式：** DP / 同时维护最大最小乘积

**题意摘要：** 求乘积最大的非空连续子数组。

**标准思路：** 负数会把最大与最小互换，因此每个位置同时维护以它结尾的 max_prod 和 min_prod。遇到负数先交换两者，再更新。

```python
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        max_prod = min_prod = ans = nums[0]
        for x in nums[1:]:
            if x < 0:
                max_prod, min_prod = min_prod, max_prod
            max_prod = max(x, max_prod * x)
            min_prod = min(x, min_prod * x)
            ans = max(ans, max_prod)
        return ans
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 最大子数组和只需一个状态；乘积题必须额外保留“最小负积”，它可能被下一个负数翻成最大正积。

## 416. 分割等和子集（中等）
**核心模式：** 0/1 背包

**题意摘要：** 判断能否把数组分成两个元素和相等的子集。

**标准思路：** 总和必须为偶数。问题转为是否能选若干元素凑出 target=sum/2。用一维 0/1 背包布尔 dp，容量必须从大到小遍历。

```python
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2:
            return False
        target = total // 2
        dp = [False] * (target + 1)
        dp[0] = True
        for x in nums:
            for s in range(target, x - 1, -1):
                dp[s] = dp[s] or dp[s - x]
        return dp[target]
```

**复杂度：** 时间 O(n·target)，空间 O(target)。

**关键易错点：** 0/1 背包一维压缩必须倒序枚举容量，否则同一元素会被重复使用。

## 32. 最长有效括号（困难）
**核心模式：** DP / 以位置结尾

**题意摘要：** 求最长连续合法括号子串长度。

**标准思路：** dp[i] 表示必须以 i 结尾的最长合法括号长度。只有 s[i]=")" 才可能更新，分前一位是 "(" 和 ")" 两种情况处理。

```python
class Solution:
    def longestValidParentheses(self, s: str) -> int:
        n = len(s)
        dp = [0] * n
        ans = 0
        for i in range(1, n):
            if s[i] == ')':
                if s[i - 1] == '(':
                    dp[i] = (dp[i - 2] if i >= 2 else 0) + 2
                else:
                    j = i - dp[i - 1] - 1
                    if j >= 0 and s[j] == '(':
                        dp[i] = dp[i - 1] + 2
                        if j - 1 >= 0:
                            dp[i] += dp[j - 1]
                ans = max(ans, dp[i])
        return ans
```

**复杂度：** 时间 O(n)，空间 O(n)。

**关键易错点：** 关键下标 j=i-dp[i-1]-1，表示尝试与当前右括号匹配的左括号位置。
