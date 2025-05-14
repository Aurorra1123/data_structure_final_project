# 产品管理系统

这是一个基于AVL树实现的产品管理系统，支持高效的产品信息存储、查询和范围搜索操作。

## 功能特点

- 使用AVL树作为底层数据结构，确保所有操作的时间复杂度为O(log n)
- 支持以下操作：
  - 插入产品信息（INSERT）
  - 查询产品价格（LOOKUP）
  - 删除产品信息（DELETE）
  - 价格范围搜索（RANGE_PRICE）
  - 描述模式搜索（RANGE_PATTERN）

## 系统要求

- Python 3.x
- 无需额外依赖包

## 使用方法

1. 准备输入文件（例如：test_file.txt），格式如下：
   ```
   N Q
   ID1 Price1 "Description1"
   ID2 Price2 "Description2"
   ...
   Operation1
   Operation2
   ...
   ```
   其中：
   - N：初始产品记录数量
   - Q：操作数量
   - 每个操作可以是以下格式之一：
     - `LOOKUP <ProductID>`
     - `INSERT <ProductID> <Price> "Description"`
     - `DELETE <ProductID>`
     - `RANGE_PRICE <ID1> <ID2> <Tau>`
     - `RANGE_PATTERN <ID1> <ID2> "Pattern"`

2. 运行程序：
   ```bash
   python source.py < test_file.txt
   ```

3. 查看输出：
   - 所有输出将写入 `output.txt` 文件
   - 每个操作的结果会按顺序记录在输出文件中

## 输出格式

- LOOKUP：输出产品价格（保留两位小数）或 "Product ID not found."
- RANGE_PRICE：输出符合价格条件的产品ID列表（空格分隔）或提示未找到
- RANGE_PATTERN：输出符合描述模式的产品ID列表（空格分隔）或提示未找到
- INSERT 和 DELETE 操作不产生输出

## 示例

输入示例：
```
2 3
1 99.99 "High quality laptop"
2 149.99 "Gaming mouse"
LOOKUP 1
RANGE_PRICE 1 2 100.00
RANGE_PATTERN 1 2 "laptop"
```

输出示例（output.txt）：
```
99.99
1
1
```

## 实现细节

- 使用AVL树确保树的平衡性，优化查询性能
- 范围搜索使用优化的遍历算法
- 字符串匹配使用内置的字符串查找功能（可根据需要替换为更高效的算法）

## 注意事项

- 产品ID应为整数
- 价格应为浮点数
- 描述和模式搜索字符串需要用双引号包围
- 所有ID在范围内搜索时都是闭区间 [ID1, ID2] 