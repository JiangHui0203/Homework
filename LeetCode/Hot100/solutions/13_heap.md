# 13 堆

> LeetCode Hot 100 个人题库 · Python 3 标准参考答案

## 215. 数组中的第 K 个最大元素（中等）
**核心模式：** 大小为 k 的最小堆

**题意摘要：** 返回数组排序后第 k 大元素，不要求返回排序结果。

**标准思路：** 维护大小最多为 k 的最小堆；遍历所有元素，超过 k 就弹出最小值。最终堆顶就是第 k 大。

```python
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []
        for x in nums:
            heappush(heap, x)
            if len(heap) > k:
                heappop(heap)
        return heap[0]
```

**复杂度：** 时间 O(n log k)，空间 O(k)。

**关键易错点：** 更优平均 O(n) 的 Quickselect 也常考；堆版最稳定易写。

## 347. 前 K 个高频元素（中等）
**核心模式：** 计数 + 最小堆

**题意摘要：** 返回出现频率最高的 k 个元素。

**标准思路：** 先 Counter 统计频率，再维护大小为 k 的 (freq, value) 最小堆。

```python
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freq = Counter(nums)
        heap = []
        for x, f in freq.items():
            heappush(heap, (f, x))
            if len(heap) > k:
                heappop(heap)
        return [x for _, x in heap]
```

**复杂度：** 设不同元素数为 m：时间 O(n + m log k)，空间 O(m+k)。

**关键易错点：** 若要求线性期望复杂度，可用桶排序；面试中堆法通常足够标准。

## 295. 数据流的中位数（困难）
**核心模式：** 双堆

**题意摘要：** 支持不断加入数字，并随时返回当前所有数字的中位数。

**标准思路：** small 为最大堆（Python 用负数）保存较小一半，large 为最小堆保存较大一半；保持 len(small) 与 len(large) 差不超过 1，且 small 可多一个。

```python
class MedianFinder:
    def __init__(self):
        self.small = []   # max-heap via negatives
        self.large = []   # min-heap

    def addNum(self, num: int) -> None:
        heappush(self.small, -num)
        heappush(self.large, -heappop(self.small))
        if len(self.large) > len(self.small):
            heappush(self.small, -heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0
```

**复杂度：** addNum O(log n)，findMedian O(1)，空间 O(n)。

**关键易错点：** 同时维护“数量平衡”和“small 中所有值 <= large 中所有值”。
