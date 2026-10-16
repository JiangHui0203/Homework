# 07 链表

> LeetCode Hot 100 个人题库 · Python 3 标准参考答案

## 160. 相交链表（简单）
**核心模式：** 双指针 / 路径长度对齐

**题意摘要：** 返回两个单链表的第一个相交节点；若不相交返回 None。

**标准思路：** 指针 A 走完链表 A 后转到 B，指针 B 走完 B 后转到 A；两者总路程相同，最终在交点或 None 相遇。

```python
class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        a, b = headA, headB
        while a is not b:
            a = a.next if a else headB
            b = b.next if b else headA
        return a
```

**复杂度：** 时间 O(m+n)，空间 O(1)。

**关键易错点：** 比较的是节点身份 is，而不是节点值。

## 206. 反转链表（简单）
**核心模式：** 三指针迭代

**题意摘要：** 原地反转单链表并返回新头结点。

**标准思路：** 遍历时先保存 next，再把当前节点 next 指向 prev，最后整体向前推进。

```python
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev, cur = None, head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        return prev
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 必须先保存 nxt，再改 cur.next，否则会丢失剩余链表。

## 234. 回文链表（简单）
**核心模式：** 快慢指针 + 反转后半段

**题意摘要：** 判断链表节点值序列是否为回文。

**标准思路：** 快慢指针找中点；反转后半段；从头和后半段起点同步比较。

```python
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        prev = None
        cur = slow
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt

        p1, p2 = head, prev
        while p2:
            if p1.val != p2.val:
                return False
            p1 = p1.next
            p2 = p2.next
        return True
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 若工程代码需要保持输入不变，可比较后再把后半段反转恢复。

## 141. 环形链表（简单）
**核心模式：** Floyd 快慢指针

**题意摘要：** 判断链表中是否存在环。

**标准思路：** 慢指针每次走一步，快指针每次两步；有环时必然相遇，无环时快指针会到达 None。

```python
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 循环条件必须同时检查 fast 和 fast.next。

## 142. 环形链表 II（中等）
**核心模式：** Floyd 判环 + 环入口数学关系

**题意摘要：** 若链表有环，返回环的入口节点。

**标准思路：** 快慢指针先在环内相遇。随后一个指针回到 head，两个都每次走一步，再次相遇的位置就是环入口。

```python
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                p = head
                while p is not slow:
                    p = p.next
                    slow = slow.next
                return p
        return None
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 先确认相遇再做第二阶段；无环直接返回 None。

## 21. 合并两个有序链表（简单）
**核心模式：** 哑节点 + 双指针

**题意摘要：** 合并两个升序链表并保持升序。

**标准思路：** 用 dummy 统一处理头结点，每次连接两条链表中较小的当前节点，最后接上未遍历完的一条。

```python
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        tail = dummy
        while list1 and list2:
            if list1.val <= list2.val:
                tail.next, list1 = list1, list1.next
            else:
                tail.next, list2 = list2, list2.next
            tail = tail.next
        tail.next = list1 or list2
        return dummy.next
```

**复杂度：** 时间 O(m+n)，空间 O(1)。

**关键易错点：** dummy 可以消除“第一个节点单独处理”的分支。

## 2. 两数相加（中等）
**核心模式：** 链表模拟加法 / 进位

**题意摘要：** 两个链表按低位到高位存储非负整数，返回它们的和。

**标准思路：** 同步遍历两链表，缺失位按 0 处理，并维护 carry；循环条件要包含 carry。

```python
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        tail = dummy
        carry = 0
        while l1 or l2 or carry:
            x = l1.val if l1 else 0
            y = l2.val if l2 else 0
            total = x + y + carry
            carry, digit = divmod(total, 10)
            tail.next = ListNode(digit)
            tail = tail.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        return dummy.next
```

**复杂度：** 时间 O(max(m,n))，空间 O(max(m,n))（输出链表）。

**关键易错点：** 最后一位可能产生新的进位，因此 while 条件中要有 carry。

## 19. 删除链表的倒数第 N 个结点（中等）
**核心模式：** 快慢指针 + dummy

**题意摘要：** 删除倒数第 n 个节点并返回头结点。

**标准思路：** dummy 指向 head。fast 先走 n 步，再让 fast/slow 同步走到 fast.next 为空；此时 slow.next 正是待删节点。

```python
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        fast = slow = dummy
        for _ in range(n):
            fast = fast.next
        while fast.next:
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next
        return dummy.next
```

**复杂度：** 时间 O(L)，空间 O(1)。

**关键易错点：** 从 dummy 出发更容易统一“删除头结点”的情况。

## 24. 两两交换链表中的节点（中等）
**核心模式：** dummy + 局部指针重连

**题意摘要：** 每两个相邻节点交换一次，不能只交换值。

**标准思路：** 让 prev 始终指向待交换两节点之前的位置，保存 a、b 后按 prev→b→a→next 的顺序重连。

```python
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        prev = dummy
        while prev.next and prev.next.next:
            a = prev.next
            b = a.next
            a.next = b.next
            b.next = a
            prev.next = b
            prev = a
        return dummy.next
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 交换后 prev 应移动到原来的第一个节点 a。

## 25. K 个一组翻转链表（困难）
**核心模式：** 分组定位 + 区间反转

**题意摘要：** 每 k 个节点作为一组翻转；不足 k 个保持原顺序。

**标准思路：** 用 group_prev 指向每组前驱，先找到第 k 个节点；若不足则结束。保存 group_next，再反转 [group_prev.next, group_next) 并重新连接。

```python
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        group_prev = dummy

        while True:
            kth = group_prev
            for _ in range(k):
                kth = kth.next
                if not kth:
                    return dummy.next
            group_next = kth.next

            prev, cur = group_next, group_prev.next
            while cur is not group_next:
                nxt = cur.next
                cur.next = prev
                prev = cur
                cur = nxt

            old_head = group_prev.next
            group_prev.next = kth
            group_prev = old_head
```

**复杂度：** 时间 O(n)，空间 O(1)。

**关键易错点：** 反转区间的 prev 初值应设为 group_next，便于翻转后自然接回后续链表。

## 138. 随机链表的复制（中等）
**核心模式：** 哈希映射 / 两遍复制

**题意摘要：** 深拷贝带 next 和 random 指针的链表。

**标准思路：** 第一遍为每个原节点创建副本并建立 old→new 映射；第二遍利用映射连接副本的 next/random。

```python
class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        if not head:
            return None
        mp = {None: None}
        cur = head
        while cur:
            mp[cur] = Node(cur.val)
            cur = cur.next
        cur = head
        while cur:
            mp[cur].next = mp[cur.next]
            mp[cur].random = mp[cur.random]
            cur = cur.next
        return mp[head]
```

**复杂度：** 时间 O(n)，空间 O(n)。

**关键易错点：** 可进一步用“原节点后插副本节点”做到 O(1) 额外空间，但哈希版更清晰稳妥。

## 148. 排序链表（中等）
**核心模式：** 归并排序 / 快慢指针

**题意摘要：** 在 O(n log n) 时间内对链表排序。

**标准思路：** 链表适合归并排序：快慢指针从中间断开，递归排序两半，再用合并有序链表模板合并。

```python
class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head

        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        mid = slow.next
        slow.next = None

        left = self.sortList(head)
        right = self.sortList(mid)

        dummy = ListNode(0)
        tail = dummy
        while left and right:
            if left.val <= right.val:
                tail.next, left = left, left.next
            else:
                tail.next, right = right, right.next
            tail = tail.next
        tail.next = left or right
        return dummy.next
```

**复杂度：** 时间 O(n log n)，递归栈空间 O(log n)。

**关键易错点：** 切分时必须 slow.next = None，否则递归不会缩小。

## 23. 合并 K 个升序链表（困难）
**核心模式：** 最小堆

**题意摘要：** 合并 k 条升序链表。

**标准思路：** 把每条非空链表头压入最小堆；每次弹出最小节点接到结果，并把该节点的 next 入堆。为避免节点不可比较，堆元素加入唯一序号。

```python
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        heap = []
        uid = 0
        for node in lists:
            if node:
                heappush(heap, (node.val, uid, node))
                uid += 1

        dummy = ListNode(0)
        tail = dummy
        while heap:
            _, _, node = heappop(heap)
            tail.next = node
            tail = tail.next
            if node.next:
                heappush(heap, (node.next.val, uid, node.next))
                uid += 1
        return dummy.next
```

**复杂度：** 设总节点数 N：时间 O(N log k)，空间 O(k)。

**关键易错点：** Python 堆在前两个字段相同时会继续比较第三字段；加入 uid 可避免比较 ListNode。

## 146. LRU 缓存（中等）
**核心模式：** 哈希表 + 双向链表（Python OrderedDict）

**题意摘要：** 实现固定容量的最近最少使用缓存，get/put 平均 O(1)。

**标准思路：** Python 标准库 OrderedDict 已封装哈希表+双向链表语义：访问后 move_to_end；超容量时 popitem(last=False) 淘汰最久未使用项。

```python
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.data = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.data:
            return -1
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key: int, value: int) -> None:
        if key in self.data:
            self.data.move_to_end(key)
        self.data[key] = value
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)
```

**复杂度：** get/put 均摊 O(1)，空间 O(capacity)。

**关键易错点：** 面试若禁止 OrderedDict，需要手写“哈希表 + 双向链表”；原理必须会解释。
