# 04 子串

> LeetCode Hot 100 个人题库 · Python 3 标准参考答案

## 560. 和为 K 的子数组（中等）
**核心模式：** 前缀和 + 哈希计数

**题意摘要：** 统计和等于 k 的连续子数组数量。

**标准思路：** 若当前前缀和为 pre，需要之前出现过 pre-k。哈希表记录每种前缀和值出现次数；初始化 {0:1} 处理从下标 0 开始的子数组。

```python
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = defaultdict(int)
        count[0] = 1
        pre = 0
        ans = 0
        for x in nums:
            pre += x
            ans += count[pre - k]
            count[pre] += 1
        return ans
```

**复杂度：** 时间 O(n)，空间 O(n)。

**关键易错点：** 数组可含负数，所以一般不能用普通滑动窗口。

## 239. 滑动窗口最大值（困难）
**核心模式：** 单调队列 / deque

**题意摘要：** 对每个长度为 k 的滑动窗口，返回窗口最大值。

**标准思路：** 双端队列保存“下标”，且对应值单调递减。新元素入队前弹出所有不大于它的尾部元素；队首若已出窗口则移除。

```python
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        q = deque()
        ans = []
        for i, x in enumerate(nums):
            while q and nums[q[-1]] <= x:
                q.pop()
            q.append(i)
            if q[0] <= i - k:
                q.popleft()
            if i >= k - 1:
                ans.append(nums[q[0]])
        return ans
```

**复杂度：** 时间 O(n)，空间 O(k)。

**关键易错点：** 队列存下标而不是值，才能判断元素是否已经离开窗口。

## 76. 最小覆盖子串（困难）
**核心模式：** 可变长滑动窗口 / 满足计数后收缩

**题意摘要：** 在 s 中找包含 t 所有字符及其次数的最短子串。

**标准思路：** 右端扩张直到窗口满足需求；满足后不断收缩左端并更新最优答案。用 formed 记录已有多少种字符达到所需次数。

```python
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not t or not s:
            return ''
        need = Counter(t)
        window = defaultdict(int)
        required = len(need)
        formed = 0
        left = 0
        best_len = float('inf')
        best_l = 0

        for right, ch in enumerate(s):
            window[ch] += 1
            if ch in need and window[ch] == need[ch]:
                formed += 1

            while formed == required:
                if right - left + 1 < best_len:
                    best_len = right - left + 1
                    best_l = left
                c = s[left]
                window[c] -= 1
                if c in need and window[c] < need[c]:
                    formed -= 1
                left += 1

        return '' if best_len == float('inf') else s[best_l:best_l + best_len]
```

**复杂度：** 时间 O(|s|+|t|)，空间 O(字符集大小)。

**关键易错点：** formed 统计“达标的字符种类数”，不是窗口中字符总数。
