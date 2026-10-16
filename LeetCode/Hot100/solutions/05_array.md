# 05 普通数组

> LeetCode Hot 100 个人题库 · Python 3 标准参考答案

## 53. 最大子数组和（中等）
**核心模式：** Kadane 动态规划

**题意摘要：** 求和最大的非空连续子数组。

**标准思路：** cur 表示“必须以当前位置结尾”的最大和：要么从当前元素重新开始，要么接在之前最优后面。

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        cur = ans = nums[0]
        for x in nums[1:]:
            cur = max(x, cur + x)
            ans = max(ans, cur)
        return ans
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 不能把初始答案设为 0，否则全负数组会出错。

## 56. 合并区间（中等）
**核心模式：** 排序 + 区间扫描

**题意摘要：** 合并所有有重叠的闭区间。

**标准思路：** 按左端点排序。若当前区间起点大于结果最后区间终点，则开新区间；否则扩展最后区间的右端点。

```python
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda x: x[0])
        ans = []
        for l, r in intervals:
            if not ans or l > ans[-1][1]:
                ans.append([l, r])
            else:
                ans[-1][1] = max(ans[-1][1], r)
        return ans
```

**复杂度：** 时间 O(n log n)，空间 O(n)（输出不计时额外可视为 O(log n) 排序栈）。

**关键易错点：** 闭区间 [1,4] 与 [4,5] 视为重叠，条件应是 l > last_r 才分开。

## 189. 轮转数组（中等）
**核心模式：** 三次反转

**题意摘要：** 将数组向右轮转 k 个位置，要求原地。

**标准思路：** k 先对 n 取模。整体反转，再反转前 k 个，再反转剩余部分。

```python
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k %= n

        def rev(l: int, r: int) -> None:
            while l < r:
                nums[l], nums[r] = nums[r], nums[l]
                l += 1
                r -= 1

        rev(0, n - 1)
        rev(0, k - 1)
        rev(k, n - 1)
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 先 k %= n；k=0 时 rev(0,-1) 会自然跳过。

## 238. 除了自身以外数组的乘积（中等）
**核心模式：** 前缀积 + 后缀积

**题意摘要：** 不使用除法，为每个位置返回其余元素的乘积。

**标准思路：** ans 先存每个位置左侧元素乘积，再从右向左用变量 suffix 累乘右侧乘积并写回。

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans = [1] * n
        prefix = 1
        for i in range(n):
            ans[i] = prefix
            prefix *= nums[i]
        suffix = 1
        for i in range(n - 1, -1, -1):
            ans[i] *= suffix
            suffix *= nums[i]
        return ans
```

**复杂度：** 时间 O(n)，除输出数组外额外空间 O(1)。

**关键易错点：** 这种写法天然处理一个或多个 0，无需特判。

## 41. 缺失的第一个正数（困难）
**核心模式：** 原地哈希 / 下标归位

**题意摘要：** 在 O(n) 时间、O(1) 额外空间内找未出现的最小正整数。

**标准思路：** 长度 n 的答案只可能在 [1,n+1]。把值 x 尽量交换到下标 x-1；归位后第一个 nums[i] != i+1 的位置就是答案。

```python
class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        for i in range(n):
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                j = nums[i] - 1
                nums[i], nums[j] = nums[j], nums[i]
        for i, x in enumerate(nums):
            if x != i + 1:
                return i + 1
        return n + 1
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** while 条件必须防止重复值导致死循环。
