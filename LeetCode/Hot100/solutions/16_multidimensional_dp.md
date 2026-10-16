# 16 多维动态规划

> LeetCode Hot 100 个人题库 · Python 3 标准参考答案

## 62. 不同路径（中等）
**核心模式：** 二维 DP / 网格计数

**题意摘要：** 机器人只能向右或向下，从左上到右下，求路径数量。

**标准思路：** 到达 (i,j) 的路径来自上方和左方，因此 dp[j] 可用一维数组滚动：dp[j]=dp[j]+dp[j-1]。

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [1] * n
        for _ in range(1, m):
            for j in range(1, n):
                dp[j] += dp[j - 1]
        return dp[-1]
```

**复杂度：** 时间 O(mn)，空间 O(n)。

**关键易错点：** 第一行和第一列路径数都为 1，因此可直接用全 1 初始化。

## 64. 最小路径和（中等）
**核心模式：** 二维 DP / 网格最优值

**题意摘要：** 从左上到右下只能向右或向下，求路径数字之和最小值。

**标准思路：** dp[j] 表示当前行到该列的最小路径和；从上方 dp[j] 和左方 dp[j-1] 取较小者，再加当前格。

```python
class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dp = [float('inf')] * n
        dp[0] = 0
        for i in range(m):
            for j in range(n):
                if j == 0:
                    dp[j] = dp[j] + grid[i][j]
                else:
                    dp[j] = min(dp[j], dp[j - 1]) + grid[i][j]
        return dp[-1]
```

**复杂度：** 时间 O(mn)，空间 O(n)。

**关键易错点：** 一维压缩时 dp[j] 在更新前代表“上方”，dp[j-1] 已代表“左方”。

## 5. 最长回文子串（中等）
**核心模式：** 中心扩展

**题意摘要：** 返回字符串中的最长回文连续子串。

**标准思路：** 每个回文都有一个中心。分别以单字符和相邻两字符作为中心向两侧扩展，记录最长区间。

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s:
            return ''
        best_l = best_r = 0

        def expand(l, r):
            nonlocal best_l, best_r
            while l >= 0 and r < len(s) and s[l] == s[r]:
                if r - l > best_r - best_l:
                    best_l, best_r = l, r
                l -= 1
                r += 1

        for i in range(len(s)):
            expand(i, i)
            expand(i, i + 1)
        return s[best_l:best_r + 1]
```

**复杂度：** 时间 O(n²)，空间 O(1)。

**关键易错点：** 虽然被放在多维 DP 专题，中心扩展通常是更简洁的标准面试解法。

## 1143. 最长公共子序列（中等）
**核心模式：** 二维 DP

**题意摘要：** 求两个字符串最长公共子序列长度，子序列不要求连续。

**标准思路：** dp[i][j] 表示 text1 前 i 个字符与 text2 前 j 个字符的 LCS 长度。字符相等则 +1，否则取舍弃其中一个末字符的最大值。用一维滚动压缩。

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        if len(text1) < len(text2):
            text1, text2 = text2, text1
        dp = [0] * (len(text2) + 1)
        for c1 in text1:
            prev = 0
            for j, c2 in enumerate(text2, 1):
                old = dp[j]
                if c1 == c2:
                    dp[j] = prev + 1
                else:
                    dp[j] = max(dp[j], dp[j - 1])
                prev = old
        return dp[-1]
```

**复杂度：** 时间 O(mn)，空间 O(min(m,n))。

**关键易错点：** 一维压缩中 prev 保存二维表的左上角 dp[i-1][j-1]。

## 72. 编辑距离（中等）
**核心模式：** 二维 DP / 字符串编辑

**题意摘要：** 把 word1 转换成 word2，允许插入、删除、替换，每次代价 1，求最少操作数。

**标准思路：** dp[i][j] 表示 word1[:i] 到 word2[:j] 的最少操作。末字符相同则继承左上；否则 1+min(删除、插入、替换)。

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        prev = list(range(n + 1))
        for i in range(1, m + 1):
            cur = [i] + [0] * n
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    cur[j] = prev[j - 1]
                else:
                    cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])
            prev = cur
        return prev[n]
```

**复杂度：** 时间 O(mn)，空间 O(n)。

**关键易错点：** 三项分别对应：删 word1 当前字符、插入匹配 word2 当前字符、替换。
