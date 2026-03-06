numbers=[1,2,3,4,5,6,7,8,9,10]
#用i循环访问numbers列表中的元素

# for i in range(len(numbers)): #len()函数返回列表的长度
    # print(numbers[i])
    # print(len(numbers))
for i in range(len(numbers)):
    if i==1:
        print(f"索引{i}的值是{numbers[i]}")