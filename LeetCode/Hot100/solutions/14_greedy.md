# 14 贪心

> LeetCode Hot 100 个人题库 · Python 3 标准参考答案

## 121. 买卖股票的最佳时机（简单）
**核心模式：** 一次扫描 / 前缀最小值

**题意摘要：** 只能买一次卖一次，求最大利润。

**标准思路：** 遍历价格，维护此前最低买入价 min_price；当前价作为卖出价时利润为 price-min_price，更新答案。

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price = float('inf')
        ans = 0
        for p in prices:
            min_price = min(min_price, p)
            ans = max(ans, p - min_price)
        return ans
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 买入必须发生在卖出之前，所以维护的是“此前”最小值。

## 55. 跳跃游戏（中等）
**核心模式：** 贪心 / 最远可达位置

**题意摘要：** 每个位置给最大跳跃长度，判断能否到达最后一个下标。

**标准思路：** 扫描可达区间内的位置并持续更新 farthest=i+nums[i] 的最大值；若某个 i 已超过 farthest，则无法到达。

```python
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        farthest = 0
        for i, x in enumerate(nums):
            if i > farthest:
                return False
            farthest = max(farthest, i + x)
            if farthest >= len(nums) - 1:
                return True
        return True
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 不需要真的选择每一步怎么跳，只需维护“当前能覆盖到哪里”。

## 45. 跳跃游戏 II（中等）
**核心模式：** 贪心 / 分层覆盖

**题意摘要：** 保证能到达终点，求最少跳跃次数。

**标准思路：** 把一次跳跃能覆盖的范围看作一层。遍历当前层内所有位置更新 next_end；到达 current_end 时必须完成一次跳跃，并把边界扩到 next_end。

```python
class Solution:
    def jump(self, nums: List[int]) -> int:
        jumps = 0
        current_end = 0
        next_end = 0
        for i in range(len(nums) - 1):
            next_end = max(next_end, i + nums[i])
            if i == current_end:
                jumps += 1
                current_end = next_end
        return jumps
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 只遍历到 n-2，避免已经到终点后再多算一次跳跃。

## 763. 划分字母区间（中等）
**核心模式：** 贪心 / 最后出现位置

**题意摘要：** 把字符串尽量切成更多片段，使同一字母只出现在一个片段内。

**标准思路：** 先记录每个字符最后出现位置。扫描当前片段时不断把 end 扩到所见字符的最远末位置；当 i==end 时即可切分。

```python
class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        last = {ch: i for i, ch in enumerate(s)}
        ans = []
        start = end = 0
        for i, ch in enumerate(s):
            end = max(end, last[ch])
            if i == end:
                ans.append(end - start + 1)
                start = i + 1
        return ans
```

**复杂度：** 时间 O(n)，空间 O(字符集大小)。

**关键易错点：** 本质是把字符的覆盖区间做贪心合并，并在最早可闭合位置切段。
