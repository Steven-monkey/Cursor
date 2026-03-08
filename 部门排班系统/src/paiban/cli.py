"""
cli.py - 命令行交互模块（Command Line Interface）
作用：用 input 让用户输入、用 print 输出结果，调用 core 模块生成排班表
适合习惯敲命令的用户，或者在没有图形界面的环境使用
"""
import pandas as pd
# 导入 pandas 库，pd 是它的常用缩写
# 用于把排班结果转成 DataFrame（表格数据）做统计，比如统计每组值班天数

# 从同包的 core 模块导入三个核心函数
from .core import (
    get_all_schedule_dates,  # 获取需要排班的所有日期（周末+节假日）
    create_schedule,         # 生成排班表
    export_to_excel,         # 导出到 Excel 文件
)


def get_user_input():
    """
    获取用户输入的所有配置信息
    包括：组数、每组的组员、年份月份、是否接续上一年排班
    返回值：groups, year, start_month, end_month, start_group_index
    """
    # 打印分隔线：字符串 "=" 乘以 50 得到 50 个等号
    print("=" * 50)
    print("欢迎使用部门排班系统")
    print("=" * 50)

    # input() 会等待用户键盘输入，返回的是字符串
    # int() 把字符串转成整数；\n 表示换行
    group_count = int(input("\n请输入组数："))

    # 创建一个空列表，用来存放每组的人员名单
    # 最终格式：[['张三','李四'], ['王五','赵六'], ...]
    groups = []

    # range(n) 生成 0 到 n-1 的整数序列
    for i in range(group_count):
        # f 字符串：花括号 {i+1} 会被替换成实际数值，因为 i 从 0 开始，所以 +1 显示为"第1组"
        print(f"\n--- 第{i+1}组 ---")
        members = input(f"请输入第{i+1}组的组员名字（用逗号分隔）：")

        # 列表推导式：一行代码完成拆分和清洗
        # members.split(',')：按逗号把字符串拆成列表，如 "张三,李四" -> ['张三','李四']
        # name.strip()：去掉每个名字首尾的空格
        # [x for x in ...]：遍历并生成新列表
        member_list = [name.strip() for name in members.split(',')]
        # 把这一组的名单追加到 groups 列表末尾
        groups.append(member_list)

    print("\n--- 排班时间范围 ---")
    year = int(input("请输入年份（例如：2024）："))
    start_month = int(input("请输入起始月份（1-12）："))
    end_month = int(input("请输入结束月份（1-12）："))

    print("\n--- 排班顺序设置 ---")
    # 问用户是否接续上一年的排班顺序
    # .strip() 去掉首尾空格；.lower() 转成小写，这样用户输入 Y 或 y 都能识别
    continue_last_year = input("是否接续上一年的排班顺序？(y/n，默认n)：").strip().lower()
    # 默认从第 0 组（显示为第 1 组）开始
    start_group_index = 0

    if continue_last_year == 'y':
        # 用户选择了接续，需要知道上一年最后是哪组值班
        last_group = int(input(f"请输入上一年最后值班的组号（1-{group_count}）："))
        # 校验组号是否在有效范围内
        if 1 <= last_group <= group_count:
            # 取余运算实现"下一组"：比如 3 组时，last_group=3 则 3%3=0，下次从第 1 组开始
            start_group_index = last_group % group_count
            print(f"提示：本次排班将从第{start_group_index + 1}组开始")
        else:
            print("警告：输入的组号无效，将从第1组开始")
    else:
        print("提示：本次排班将从第1组开始")

    # return 可以一次返回多个值，外面用多个变量接收
    return groups, year, start_month, end_month, start_group_index


def main():
    """
    主流程函数：完整的排班流程
    1. 获取用户输入
    2. 计算需要排班的日期
    3. 生成排班表
    4. 导出 Excel
    5. 打印统计信息
    """
    try:
        # 用 5 个变量接收 get_user_input 返回的 5 个值
        groups, year, start_month, end_month, start_group_index = get_user_input()

        print("\n正在分析日期...")
        # 获取指定年月范围内所有需要排班的日期（周末+节假日，排除调休日）
        schedule_dates = get_all_schedule_dates(year, start_month, end_month)
        # len() 获取列表长度，即有多少个日期
        print(f"共找到 {len(schedule_dates)} 个需要排班的日期")

        print("\n正在生成排班表...")
        # 根据组、日期和起始组索引，生成完整排班表
        schedule = create_schedule(groups, schedule_dates, start_group_index)

        print("\n正在导出Excel文件...")
        # 生成文件名，如：排班表_2024年1-12月.xlsx
        filename = f"排班表_{year}年{start_month}-{end_month}月.xlsx"
        export_to_excel(schedule, groups, year, start_month, end_month, filename)

        # 打印分隔线和标题
        print("\n" + "=" * 50)
        print("排班统计信息")
        print("=" * 50)

        # 把排班表（字典列表）转成 pandas 的 DataFrame，方便做统计
        df_schedule = pd.DataFrame(schedule)
        for i in range(len(groups)):
            # df_schedule['值班组'] == f"第{i+1}组" 得到一个布尔 Series（True/False 列）
            # .sum() 会把 True 当作 1、False 当作 0 相加，得到该组值班总天数
            total_days = (df_schedule['值班组'] == f"第{i+1}组").sum()
            print(f"第{i+1}组：共值班 {total_days} 天")

        # 如果排班表不为空
        if schedule:
            # schedule[-1] 取列表最后一个元素（最后一条排班记录）
            last_schedule_item = schedule[-1]
            # 用字典的键取值
            last_group = last_schedule_item['值班组']
            # strftime 把日期对象格式化成指定格式的字符串
            last_date = last_schedule_item['日期'].strftime('%Y年%m月%d日')
            print(f"\n最后值班：{last_group}（{last_date}）")
            print("提示：下次排班时可选择接续此次排班顺序")

        print("\n排班完成！")

    except NotImplementedError as e:
        # chinesecalendar 库对某些年份没有节假日数据时会抛出这个异常
        print(f"\n程序运行出错：{e}")
        print("提示：法定节假日数据随 chinesecalendar 库更新，支持 2004-2026 年。")
        print("      每年 11 月国务院发布次年安排后，执行 pip install -U chinesecalendar 可获取最新数据。")
    except Exception as e:
        # 捕获其他所有类型的异常，避免程序崩溃
        print(f"\n程序运行出错：{e}")
        print("请检查输入是否正确，或联系管理员。")


# 直接运行 cli.py 时执行 main；被 import 时 __name__ 是 "paiban.cli"，不会执行
if __name__ == "__main__":
    main()
