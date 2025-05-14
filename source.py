import time

#常量定义
OUTPUT_FILE = "output.txt"
STRING_MATCH_ALGORITHM = "BM"  # 可选: "KMP", "BM" 或 "IN"

with open(OUTPUT_FILE, "w") as f:
    pass

def write_output(data):
    """将数据追加写入到 output.txt 文件"""
    with open(OUTPUT_FILE, "a") as f:
        f.write(str(data) + "\n")

class AVLNode:
    def __init__(self, product_id, price, description):
        self.product_id = product_id
        self.price = price
        self.description = description
        self.left = None
        self.right = None
        self.height = 1  # AVL树节点需要高度信息

    def __str__(self):
        return f"ID: {self.product_id}, Price: {self.price}, Desc: {self.description}"

class AVLTree:
    def __init__(self):
        self.root = None

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _right_rotate(self, z):
        # 实现右旋操作
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _left_rotate(self, y):
        # 实现左旋操作
        x = y.right
        T2 = x.left

        x.left = y
        y.right = T2

        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x

    def insert(self, product_id, price, description):
        self.root = self._insert_node(self.root, product_id, price, description)

    def _insert_node(self, root, product_id, price, description):
        if not root:
            return AVLNode(product_id, price, description)
        elif product_id < root.product_id:
            root.left = self._insert_node(root.left, product_id, price, description)
        else:
            root.right = self._insert_node(root.right, product_id, price, description)

        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        balance = self._get_balance(root)

        # LL Case
        if balance > 1 and product_id < root.left.product_id:
            return self._right_rotate(root)
        # RR Case
        if balance < -1 and product_id > root.right.product_id:
            return self._left_rotate(root)
        # LR Case
        if balance > 1 and product_id > root.left.product_id:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)
        # RL Case
        if balance < -1 and product_id < root.right.product_id:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)

        return root


    def delete(self, product_id):
        self.root = self._delete_node(self.root, product_id)

    def _delete_node(self, root, product_id):
        # 递归辅助函数
        if not root:
            return root

        if product_id < root.product_id:
            root.left = self._delete_node(root.left, product_id)
        elif product_id > root.product_id:
            root.right = self._delete_node(root.right, product_id)
        else: # 找到了要删除的节点
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp

            # 节点有两个子节点，获取中序后继 (右子树中最小的节点)
            temp = self._get_min_value_node(root.right)
            root.product_id = temp.product_id
            root.price = temp.price
            root.description = temp.description
            root.right = self._delete_node(root.right, temp.product_id) # 删除中序后继

        if root is None: # 如果树在删除后变为空 (例如，只有一个节点时)
            return root

        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        balance = self._get_balance(root)

        # 平衡调整 (与插入类似，但有更多情况)
        # LL Case
        if balance > 1 and self._get_balance(root.left) >= 0:
            return self._right_rotate(root)
        # LR Case
        if balance > 1 and self._get_balance(root.left) < 0:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)
        # RR Case
        if balance < -1 and self._get_balance(root.right) <= 0:
            return self._left_rotate(root)
        # RL Case
        if balance < -1 and self._get_balance(root.right) > 0:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)

        return root

    def _get_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def lookup(self, product_id):
        # 实现AVL树的查找操作
        # 返回包含 (price, description) 的元组，如果未找到则返回 None
        node = self._lookup_node(self.root, product_id)
        if node:
            return node.price
        return None

    def _lookup_node(self, root, product_id):
        # 递归辅助函数
        if not root or root.product_id == product_id:
            return root
        if product_id < root.product_id:
            return self._lookup_node(root.left, product_id)
        return self._lookup_node(root.right, product_id)

    def _range_search_nodes(self, node, id1, id2, result_nodes):
        """
        辅助函数，用于递归查找在ID范围 [id1, id2] 内的节点。
        将符合条件的节点添加到 result_nodes 列表中。
        """
        if not node:
            return

        # 如果当前节点的ID小于范围的下限，则只搜索右子树
        if node.product_id < id1:
            self._range_search_nodes(node.right, id1, id2, result_nodes)
        # 如果当前节点的ID大于范围的上限，则只搜索左子树
        elif node.product_id > id2:
            self._range_search_nodes(node.left, id1, id2, result_nodes)
        # 如果当前节点的ID在范围内
        else:
            # 先搜索左子树中可能符合条件的节点
            self._range_search_nodes(node.left, id1, id2, result_nodes)
            # 将当前节点加入结果列表
            result_nodes.append(node)
            # 再搜索右子树中可能符合条件的节点
            self._range_search_nodes(node.right, id1, id2, result_nodes)


# 字符串匹配算法选择
def compute_lps(pattern):
    """
    KMP算法：计算模式串的最长公共前后缀数组
    """
    lps = [0] * len(pattern)
    length = 0
    i = 1
    
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    """
    KMP算法实现
    """
    if not pattern:
        return True
    if not text:
        return False
        
    lps = compute_lps(pattern)
    i = 0  # text的索引
    j = 0  # pattern的索引
    
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
            
        if j == len(pattern):
            return True
            
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
                
    return False

def bad_char_heuristic(pattern):
    """
    BM算法：坏字符规则预处理
    """
    bad_char = {}
    for i in range(len(pattern)):
        bad_char[pattern[i]] = i
    return bad_char

def good_suffix_heuristic(pattern):
    """
    BM算法：好后缀规则预处理
    """
    m = len(pattern)
    good_suffix = [0] * (m + 1)
    suffix = [0] * (m + 1)
    
    # 计算后缀数组
    for i in range(m):
        suffix[i] = m
    j = 0
    for i in range(m-1, -1, -1):
        if i > j and pattern[i] == pattern[m-1-j]:
            j += 1
        suffix[j] = m-1-i
    
    # 计算好后缀数组
    for i in range(m):
        good_suffix[i] = m
    j = 0
    for i in range(m-1, -1, -1):
        if suffix[i] == i + 1:
            for j in range(m-1-i):
                if good_suffix[j] == m:
                    good_suffix[j] = m-1-i
    
    for i in range(m-1):
        good_suffix[m-1-suffix[i]] = m-1-i
        
    return good_suffix

def boyer_moore_search(text, pattern):
    """
    Boyer-Moore算法实现
    """
    if not pattern:
        return True
    if not text:
        return False
        
    m = len(pattern)
    n = len(text)
    
    # 预处理
    bad_char = bad_char_heuristic(pattern)
    good_suffix = good_suffix_heuristic(pattern)
    
    # 搜索
    s = 0  # 模式串相对于文本串的偏移量
    while s <= n - m:
        j = m - 1
        
        # 从右向左匹配
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
            
        if j < 0:  # 找到匹配
            return True
        else:
            # 使用坏字符规则和好后缀规则中的较大值
            bc_shift = j - bad_char.get(text[s + j], -1)
            gs_shift = good_suffix[j]
            s += max(bc_shift, gs_shift)
            
    return False

def builtin_search(text, pattern):
    """
    Python内置的in操作符实现
    """
    return pattern in text

def string_contains(text, pattern):
    algorithms = {
        "KMP": kmp_search,
        "BM": boyer_moore_search,
        "IN": builtin_search
    }
    return algorithms.get(STRING_MATCH_ALGORITHM, builtin_search)(text, pattern)

class ProductSystem:
    def __init__(self):
        self.avl_tree = AVLTree()

    def process_lookup(self, product_id):
        price = self.avl_tree.lookup(product_id)
        if price is not None:
            write_output(f"{price:.2f}")
        else:
            write_output("Product ID not found.")

    def process_insert(self, product_id, price, description):

        self.avl_tree.insert(product_id, price, description)
        # 根据文档，INSERT 操作后通常没有立即的输出要求到 output.txt

    def process_delete(self, product_id):
        # 删除操作通常也没有显式输出到文件的要求
        # 文档中 DELETE 操作没有指定输出格式
        self.avl_tree.delete(product_id)
        # 根据文档，DELETE 操作后通常没有立即的输出要求到 output.txt

    def process_range_price(self, id1, id2, tau):
        result_nodes = []
        self.avl_tree._range_search_nodes(self.avl_tree.root, id1, id2, result_nodes)

        matching_ids = []
        for node in result_nodes:
            if node.price <= tau:
                matching_ids.append(node.product_id)

        matching_ids.sort() # 确保升序

        if matching_ids:
            write_output(" ".join(map(str, matching_ids)))
        else:
            write_output("No products found in the given range with the specified price.")

    def process_range_pattern(self, id1, id2, pattern):
        result_nodes = []
        self.avl_tree._range_search_nodes(self.avl_tree.root, id1, id2, result_nodes)

        matching_ids = []
        for node in result_nodes:
            if string_contains(node.description, pattern):
                matching_ids.append(node.product_id)

        matching_ids.sort() # 确保升序

        if matching_ids:
            write_output(" ".join(map(str, matching_ids)))
        else:
            write_output("No products found in the given range with the specified pattern.")


# 主程序逻辑

if __name__ == "__main__":
    # 记录开始时间
    start_time = time.time()
    
    system = ProductSystem()

    # 1. 读取 N 和 Q (在同一行)
    line_N_Q = input().split()
    N = int(line_N_Q[0])
    Q = int(line_N_Q[1])

    # 2. 读取 N 条初始产品记录
    for _ in range(N):
        # ProductID Price "Description"
        # maxsplit=2 会将行分割成三部分：ID, Price, 和带引号的Description
        line_parts = input().split(maxsplit=2)
        product_id = int(line_parts[0])
        price = float(line_parts[1])
        description = line_parts[2].strip('"') # 移除描述两边的引号
        system.process_insert(product_id, price, description) # 初始记录插入

    # 3. 读取并执行 Q 条操作
    for _ in range(Q):
        # 读取整行操作指令，然后根据第一个词判断操作类型
        operation_line_raw = input()
        parts = operation_line_raw.split() # 先初步分割
        op_type = parts[0]

        if op_type == "LOOKUP":
            product_id = int(parts[1])
            system.process_lookup(product_id)
        elif op_type == "INSERT":

            parsed_insert = operation_line_raw.split(maxsplit=3)
            product_id = int(parsed_insert[1])
            price = float(parsed_insert[2])
            description = parsed_insert[3].strip('"')
            system.process_insert(product_id, price, description)
        elif op_type == "DELETE":
            product_id = int(parts[1])
            system.process_delete(product_id)
        elif op_type == "RANGE_PRICE":
            # RANGE_PRICE <ID1> <ID2> <Tau>
            id1 = int(parts[1])
            id2 = int(parts[2])
            tau = float(parts[3])
            system.process_range_price(id1, id2, tau)
        elif op_type == "RANGE_PATTERN":
            # RANGE_PATTERN <ID1> <ID2> <Pattern>
            # op_type id1 id2 "pattern with spaces"
            # split(maxsplit=3) 会分成4部分: op, id1, id2, "pattern"
            parsed_range_pattern = operation_line_raw.split(maxsplit=3)
            id1 = int(parsed_range_pattern[1])
            id2 = int(parsed_range_pattern[2])
            pattern = parsed_range_pattern[3].strip('"') # 移除模式两边的引号
            system.process_range_pattern(id1, id2, pattern)
    
    # 记录结束时间并计算总执行时间
    end_time = time.time()
    execution_time = end_time - start_time
    
    # 将执行时间输出到终端
    print(f"程序总执行时间: {execution_time:.4f} 秒")