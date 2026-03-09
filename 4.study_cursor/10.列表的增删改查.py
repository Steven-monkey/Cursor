# ============ 列表的增删改查 ============

# 创建一个员工列表，列表中可以有重复的元素
employees = ["达康书记", "高启盛", "王伟伟", "赵四", "赵三", "赵六", "赵四", "赵四", "赵四"]

# ------------ 一、增（添加元素）------------

# append(元素)：在列表末尾追加一个元素，原列表会被修改
employees.append("新员工")
print("append后:", employees)

# insert(索引, 元素)：在指定索引位置插入元素，该位置及后面的元素都会往后挪一位
# 索引0表示最前面，所以"老大"会插到第一位
employees.insert(0, "老大")
print("insert后:", employees)

# 用 + 号可以把两个列表合并成一个新列表，原列表不变
# new_list 是新的列表，employees 本身没有改变
new_list = employees + ["临时工A", "临时工B"]
print("合并后 new_list:", new_list)

# ------------ 二、查（查找/获取）------------

# 通过索引获取元素：列表[索引]，索引从0开始
# 索引0是第一个，-1 是最后一个（倒数第一个）
first = employees[0]    # 获取第一个元素
last = employees[-1]    # 获取最后一个元素
third = employees[2]    # 获取第三个元素（索引为2）
print("第一个:", first, "最后一个:", last, "第三个:", third)

# index(元素)：查找元素在列表中第一次出现的位置，返回索引值
# 如果元素不存在会报错
pos = employees.index("高启盛")
print("高启盛的索引:", pos)

# count(元素)：统计该元素在列表中出现了多少次
num = employees.count("赵四")
print("赵四出现次数:", num)

# in 关键字：判断元素是否在列表中，返回 True 或 False
if "达康书记" in employees:
    print("达康书记在名单里")

# ------------ 三、改（修改元素）------------

# 通过 列表[索引] = 新值 来修改指定位置的元素
employees[0] = "达康书记升级版"   # 把第一个元素改成新值
employees[-1] = "最后一个"        # 把最后一个元素改成"最后一个"
print("修改后:", employees)

# ------------ 四、删（删除元素）------------

# remove(元素)：按值删除，只删除第一个匹配的元素
# 如果元素不存在会报错
employees.remove("王伟伟")
print("remove王伟伟后:", employees)

# pop(索引)：按位置删除，删除指定索引的元素并返回该元素
# 不写索引时默认删除最后一个
removed = employees.pop(2)       # 删除索引2的元素，返回值赋给 removed
print("pop(2)删除的是:", removed)

# del 列表[索引]：按索引删除元素，不返回值
del employees[0]
print("del后:", employees)

# clear()：清空列表，删除所有元素，列表变成空列表 []
employees.clear()
print("clear后:", employees)
