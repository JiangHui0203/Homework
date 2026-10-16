# 10 回溯

> LeetCode Hot 100 个人题库 · Python 3 标准参考答案

## 46. 全排列（中等）
**核心模式：** 回溯 / used 数组

**题意摘要：** 返回无重复数组的所有排列。

**标准思路：** path 表示当前排列，used 标记哪些元素已被选择；当 path 长度等于 n 时加入答案。

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        ans = []
        path = []
        used = [False] * len(nums)

        def dfs():
            if len(path) == len(nums):
                ans.append(path.copy())
                return
            for i, x in enumerate(nums):
                if used[i]:
                    continue
                used[i] = True
                path.append(x)
                dfs()
                path.pop()
                used[i] = False

        dfs()
        return ans
```

**复杂度：** 时间 O(n·n!)，空间 O(n)（不计输出）。

**关键易错点：** 加入答案时必须 path.copy()，否则后续回溯会修改已保存结果。

## 78. 子集（中等）
**核心模式：** 回溯 / 选与不选

**题意摘要：** 返回无重复数组的所有子集。

**标准思路：** 每到一个状态就把当前 path 作为一个合法子集加入答案；再从 start 开始依次选择后续元素。

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        ans = []
        path = []

        def dfs(start):
            ans.append(path.copy())
            for i in range(start, len(nums)):
                path.append(nums[i])
                dfs(i + 1)
                path.pop()

        dfs(0)
        return ans
```

**复杂度：** 时间 O(n·2^n)，空间 O(n)（不计输出）。

**关键易错点：** 组合/子集类通常带 start；排列类通常用 used。

## 17. 电话号码的字母组合（中等）
**核心模式：** 回溯 / 多叉选择树

**题意摘要：** 把数字 2-9 映射到电话按键字母，返回所有可能字符串。

**标准思路：** 每一位数字对应一组可选字母；递归到第 i 位时枚举该组字母并进入下一层。

```python
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
        mp = {
            '2':'abc', '3':'def', '4':'ghi', '5':'jkl',
            '6':'mno', '7':'pqrs', '8':'tuv', '9':'wxyz'
        }
        ans = []
        path = []

        def dfs(i):
            if i == len(digits):
                ans.append(''.join(path))
                return
            for ch in mp[digits[i]]:
                path.append(ch)
                dfs(i + 1)
                path.pop()

        dfs(0)
        return ans
```

**复杂度：** 时间与输出规模同阶，最坏约 O(4^n·n)。

**关键易错点：** 空输入按题意返回 []，而不是 [""]。

## 39. 组合总和（中等）
**核心模式：** 回溯 / 可重复选择

**题意摘要：** 候选正整数可无限次使用，找所有和为 target 的组合。

**标准思路：** 先排序便于剪枝。dfs(start, remain) 中从 start 起枚举，因此组合不考虑顺序；递归仍传 i，使同一元素可再次使用。

```python
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        ans = []
        path = []

        def dfs(start, remain):
            if remain == 0:
                ans.append(path.copy())
                return
            for i in range(start, len(candidates)):
                x = candidates[i]
                if x > remain:
                    break
                path.append(x)
                dfs(i, remain - x)
                path.pop()

        dfs(0, target)
        return ans
```

**复杂度：** 复杂度与解空间相关，最坏指数级；递归深度最多约 target/min(candidates)。

**关键易错点：** “可重复选择”对应递归传 i；若不可重复通常传 i+1。

## 22. 括号生成（中等）
**核心模式：** 回溯 / 合法性剪枝

**题意摘要：** 生成 n 对括号的所有合法组合。

**标准思路：** 记录已用左括号 open、右括号 close。只要 open<n 就能加左括号；只有 close<open 才能加右括号。

```python
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        ans = []
        path = []

        def dfs(opened, closed):
            if len(path) == 2 * n:
                ans.append(''.join(path))
                return
            if opened < n:
                path.append('(')
                dfs(opened + 1, closed)
                path.pop()
            if closed < opened:
                path.append(')')
                dfs(opened, closed + 1)
                path.pop()

        dfs(0, 0)
        return ans
```

**复杂度：** 输出规模为第 n 个卡特兰数，时间与输出规模同阶。

**关键易错点：** 核心剪枝是任意前缀中右括号数不能超过左括号数。

## 79. 单词搜索（中等）
**核心模式：** 网格 DFS + 回溯

**题意摘要：** 判断给定单词能否由网格中上下左右相邻单元格依次组成，同一格不能重复使用。

**标准思路：** 从每个可能起点 DFS。当前字符匹配后暂时把该格标记为已访问，探索四邻域，回溯时恢复。

```python
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m, n = len(board), len(board[0])

        def dfs(i, j, k):
            if k == len(word):
                return True
            if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != word[k]:
                return False
            ch = board[i][j]
            board[i][j] = '#'
            found = (dfs(i + 1, j, k + 1) or dfs(i - 1, j, k + 1) or
                     dfs(i, j + 1, k + 1) or dfs(i, j - 1, k + 1))
            board[i][j] = ch
            return found

        for i in range(m):
            for j in range(n):
                if dfs(i, j, 0):
                    return True
        return False
```

**复杂度：** 最坏时间 O(mn·4^L)，递归空间 O(L)。

**关键易错点：** 无论成功失败，都应恢复 board；这里先保存 found 再恢复，避免短路返回漏恢复。

## 131. 分割回文串（中等）
**核心模式：** 回溯 + 回文判断

**题意摘要：** 把字符串分割成若干子串，使每段都是回文，返回所有方案。

**标准思路：** 从 start 枚举结束位置 end，若 s[start:end+1] 是回文就加入 path 并递归处理剩余后缀。

```python
class Solution:
    def partition(self, s: str) -> List[List[str]]:
        ans = []
        path = []

        def is_pal(l, r):
            while l < r:
                if s[l] != s[r]:
                    return False
                l += 1
                r -= 1
            return True

        def dfs(start):
            if start == len(s):
                ans.append(path.copy())
                return
            for end in range(start, len(s)):
                if is_pal(start, end):
                    path.append(s[start:end + 1])
                    dfs(end + 1)
                    path.pop()

        dfs(0)
        return ans
```

**复杂度：** 最坏时间 O(n²·2^n)（含回文判断），空间 O(n)（不计输出）。

**关键易错点：** 可用 DP 预处理 isPalindrome 将回文判断降为 O(1)。

## 51. N 皇后（困难）
**核心模式：** 回溯 + 列/对角线集合剪枝

**题意摘要：** 在 n×n 棋盘放置 n 个皇后，使任意两个不在同一列或对角线。

**标准思路：** 逐行放皇后。用 cols、diag1(row-col)、diag2(row+col) 三个集合 O(1) 判断冲突。

```python
class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        ans = []
        cols, diag1, diag2 = set(), set(), set()
        pos = [-1] * n

        def dfs(r):
            if r == n:
                board = []
                for c in pos:
                    board.append('.' * c + 'Q' + '.' * (n - c - 1))
                ans.append(board)
                return
            for c in range(n):
                if c in cols or r - c in diag1 or r + c in diag2:
                    continue
                pos[r] = c
                cols.add(c); diag1.add(r - c); diag2.add(r + c)
                dfs(r + 1)
                cols.remove(c); diag1.remove(r - c); diag2.remove(r + c)

        dfs(0)
        return ans
```

**复杂度：** 最坏约 O(n!)，递归空间 O(n)。

**关键易错点：** 两条对角线可分别用 row-col 与 row+col 唯一标识。
