# 09 图论

> LeetCode Hot 100 个人题库 · Python 3 标准参考答案

## 200. 岛屿数量（中等）
**核心模式：** DFS/BFS 连通块

**题意摘要：** 0/1 网格中，按上下左右相邻统计由 1 组成的岛屿数量。

**标准思路：** 遍历网格，每遇到一个未访问陆地就把答案加 1，并 DFS/BFS 把这一整块陆地全部标记为已访问。

```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        m, n = len(grid), len(grid[0])

        def dfs(i, j):
            if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] != '1':
                return
            grid[i][j] = '0'
            dfs(i + 1, j)
            dfs(i - 1, j)
            dfs(i, j + 1)
            dfs(i, j - 1)

        ans = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '1':
                    ans += 1
                    dfs(i, j)
        return ans
```

**复杂度：** 时间 O(mn)，最坏递归栈 O(mn)。

**关键易错点：** 这里直接修改 grid 作为 visited；若输入不可修改则单独建 visited。

## 994. 腐烂的橘子（中等）
**核心模式：** 多源 BFS

**题意摘要：** 腐烂橘子每分钟感染上下左右的新鲜橘子，求全部腐烂所需最短时间；无法完成返回 -1。

**标准思路：** 把所有初始腐烂橘子同时入队作为 BFS 第 0 层，并统计 fresh 数量；逐层扩散，每发生一层有效感染时间加 1。

```python
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        q = deque()
        fresh = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2:
                    q.append((i, j))
                elif grid[i][j] == 1:
                    fresh += 1

        minutes = 0
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        while q and fresh:
            for _ in range(len(q)):
                i, j = q.popleft()
                for di, dj in dirs:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                        grid[ni][nj] = 2
                        fresh -= 1
                        q.append((ni, nj))
            minutes += 1
        return minutes if fresh == 0 else -1
```

**复杂度：** 时间 O(mn)，空间 O(mn)。

**关键易错点：** 这是典型多源 BFS：所有起点必须一开始同时入队。

## 207. 课程表（中等）
**核心模式：** 拓扑排序 / 入度

**题意摘要：** 根据先修关系判断是否能完成所有课程，本质是判断有向图是否无环。

**标准思路：** 构建邻接表和入度。把所有入度为 0 的节点入队，逐个删除其出边；若最终处理节点数等于课程数，则无环。

```python
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = [[] for _ in range(numCourses)]
        indeg = [0] * numCourses
        for course, pre in prerequisites:
            graph[pre].append(course)
            indeg[course] += 1

        q = deque(i for i in range(numCourses) if indeg[i] == 0)
        taken = 0
        while q:
            u = q.popleft()
            taken += 1
            for v in graph[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return taken == numCourses
```

**复杂度：** 时间 O(V+E)，空间 O(V+E)。

**关键易错点：** 边方向应是 prerequisite → course。

## 208. 实现 Trie (前缀树)（中等）
**核心模式：** Trie

**题意摘要：** 支持插入单词、精确搜索单词、判断是否存在给定前缀。

**标准思路：** 每个节点保存 children 映射和 is_end 标记。insert 沿字符路径创建节点；search 走完整路径后还要检查 is_end；startsWith 只需路径存在。

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
```

**复杂度：** 单次操作时间 O(L)，空间与所有插入字符总数同阶。

**关键易错点：** search 与 startsWith 的唯一区别是是否要求终点 is_end=True。
