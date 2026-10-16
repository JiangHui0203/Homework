# 17 技巧

> LeetCode Hot 100 个人题库 · Python 3 标准参考答案

## 136. 只出现一次的数字（简单）
**核心模式：** 位运算 XOR

**题意摘要：** 除一个元素出现一次外，其余都恰好出现两次，找出单独元素。

**标准思路：** 利用 x^x=0、x^0=x 且异或满足交换律与结合律，把所有数异或即可。

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        ans = 0
        for x in nums:
            ans ^= x
        return ans
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 这是 XOR 消对的标准题，前提是其他元素恰好出现两次。

## 169. 多数元素（简单）
**核心模式：** Boyer-Moore 投票

**题意摘要：** 找出出现次数超过 n/2 的元素，题目保证存在。

**标准思路：** 把不同元素两两抵消。维护 candidate 和 count；count 归零时换候选，相同 +1，不同 -1。最终剩下的一定是多数元素。

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        candidate = None
        count = 0
        for x in nums:
            if count == 0:
                candidate = x
            count += 1 if x == candidate else -1
        return candidate
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 若题目不保证多数元素存在，还需第二遍验证 candidate 频次。

## 75. 颜色分类（中等）
**核心模式：** 荷兰国旗 / 三指针

**题意摘要：** 原地把只含 0、1、2 的数组按颜色排序。

**标准思路：** 维护 [0,left) 全为 0，[left,i) 全为 1，(right,n) 全为 2。遇 0 与 left 换并推进；遇 2 与 right 换但 i 暂不推进，因为换来的值尚未检查。

```python
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        left, i, right = 0, 0, len(nums) - 1
        while i <= right:
            if nums[i] == 0:
                nums[left], nums[i] = nums[i], nums[left]
                left += 1
                i += 1
            elif nums[i] == 2:
                nums[i], nums[right] = nums[right], nums[i]
                right -= 1
            else:
                i += 1
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 交换 2 后不能立刻 i+=1，因为从右边换回来的元素还未分类。

## 31. 下一个排列（中等）
**核心模式：** 字典序 / 找下降拐点

**题意摘要：** 把数组原地变成字典序中的下一个更大排列；若已最大则变为最小排列。

**标准思路：** 从右找第一个 nums[i]<nums[i+1] 的拐点；再从右找第一个大于 nums[i] 的元素交换；最后反转 i+1 之后的递减后缀使其最小。

```python
class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        n = len(nums)
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1
        if i >= 0:
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]
        l, r = i + 1, n - 1
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 目标是“最小幅度地变大”：拐点尽量靠右，替换值尽量小但必须更大，后缀再变为最小。

## 287. 寻找重复数（中等）
**核心模式：** Floyd 判环映射

**题意摘要：** 长度 n+1 的数组元素均在 [1,n]，只有一个重复值（可重复多次），要求不修改数组且 O(1) 额外空间。

**标准思路：** 把下标 i 指向 nums[i] 看作链表。由于值域是 [1,n]，必然形成环；重复数就是环入口。用 Floyd 快慢指针先相遇，再从起点同步走到入口。

```python
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        slow = nums[0]
        fast = nums[nums[0]]
        while slow != fast:
            slow = nums[slow]
            fast = nums[nums[fast]]

        p = 0
        while p != slow:
            p = nums[p]
            slow = nums[slow]
        return p
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 不要把“值”与“下标”混淆：数组定义了函数 f(i)=nums[i]，重复值对应多个入边，形成环入口。
