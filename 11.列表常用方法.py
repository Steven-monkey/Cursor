# ============ 列表常用方法 ============

# 1. append(元素) - 在末尾添加一个元素
# 原列表会被修改，在最后追加新元素
lst = [1, 2, 3]
# lst.append(4)
# print("append:", lst)  # [1, 2, 3, 4]

# 2. extend(列表) - 把另一个列表中的元素逐个添加到当前列表末尾
# 注意：和 append 不同，extend 会把传入列表的每个元素单独加入，而不是把整个列表当成一个元素
# lst.extend([5, 6])
# print("extend:", lst)  # [1, 2, 3, 4, 5, 6]

# 3. insert(索引, 元素) - 在指定索引位置插入元素
# 该位置及后面的元素都会往后挪一位，索引0表示最前面
# lst.insert(0, 5)
# print("insert:", lst)  # [0, 1, 2, 3, 4, 5, 6]

# 4. remove(元素) - 按值删除，只删除第一个匹配的元素
# 如果元素不存在会报 ValueError 错误
# lst.remove(2)
# print("remove:", lst)  # [0, 1, 2, 4, 5, 6]

# 5. pop(索引) - 按位置删除，删除指定索引的元素并返回该元素
# 不写索引时默认删除最后一个元素
# x = lst.pop()  # 删除最后一个(6)，并返回6
# print("pop():", x, lst)  # 6 [0, 1, 2, 4, 5]

# 6. clear() - 清空列表，删除所有元素，列表变成空列表 []
# lst2 = [1, 2, 3]
# lst2.clear()
# print("clear:", lst2)  # []

# 7. index(元素) - 查找元素第一次出现的索引位置
# 如果元素不存在会报 ValueError 错误
# lst3 = ["a", "b", "c", "b"]
# i = lst3.index("c")  # "b"第一次出现在索引1
# print("index:", i)  # 1

# 8. count(元素) - 统计该元素在列表中出现的次数
# n = lst3.count("b")  # "b"出现了2次
# print("count:", n)  # 2

# 9. sort() - 原地排序，默认从小到大（升序）
# 会直接修改原列表，不返回新列表
nums = [3, 1, 4, 1, 5]
# nums.sort()
# print("sort:", nums)  # [1, 1, 3, 4, 5]

# 10. sort(reverse=True) - 从大到小排序（降序）
# nums.sort(reverse=True)
# print("sort逆序:", nums)  # [5, 4, 3, 1, 1]

# 11. reverse() - 反转列表顺序，第一个变最后一个，最后一个变第一个
# 原地修改，不返回新列表
# lst4 = [1, 2, 3,6,7,89,3,4]
# lst4.reverse()
# print("reverse:", lst4)  # [3, 2, 1]

# # 12. copy() - 复制一份新列表（浅拷贝）
# # 修改复制后的列表不会影响原列表
# # 注意：lst6 = lst5 只是让两个变量指向同一个列表，不是复制
# lst5 = [1, 2, 3]
# lst6 = lst5.copy()
# lst6.append(4)  # 只修改 lst6，lst5 不变
# print("原列表:", lst5, "复制的:", lst6)  # [1, 2, 3] [1, 2, 3, 4]

# # 13. len(列表) - 获取列表长度，即元素个数
# # 这是 Python 内置函数，不是列表的方法，写法是 len(列表) 而不是 列表.len()
# lst4 = [1, 2, 3,6,7,89,3,4]
# long =len(lst4)
# print("长度:", long)  # 5

# =========面试题========
str = "hello,world, i from china"
# lst=list(str)
x = '|'.join(reversed(str))
print(x)

s = "hello world"
x = s[::-1]  # 切片翻转：起点到终点，步长为-1表示倒着取
print(x)     # dlrow olleh