"""
cli.py - 命令行入口
用 input/print 交互，调用 core 生成排班。
"""
import pandas as pd  # 用于把 schedule 转 DataFrame 做统计

from .core import (
    get_all_schedule_dates,  # 获取要排班的日期
    create_schedule,         # 生成排班
    export_to_excel,         # 导出 Excel
)


def get_user_input():
    """让用户输入组数、组员、年份月份、是否接续"""
    print("=" * 50)  # 字符串乘数字 = 重复 50 次
    print("欢迎使用部门排班系统")
    print("=" * 50)

    group_count = int(input("\n请输入组数："))
    # input 返回字符串，int() 转成整数；\n 换行

    groups = []  # 空列表，存每组人员

    for i in range(group_count):
        # range(n) 生成 0,1,...,n-1
        print(f"\n--- 第{i+1}组 ---")  # f 字符串：{i+1} 替换成值
        members = input(f"请输入第{i+1}组的组员名字（用逗号分隔）：")

        member_list = [name.strip() for name in members.split(',')]
        # split(',') 按逗号拆成列表；strip() 去首尾空格；整体是列表推导式
        groups.append(member_list)  # 加到 groups

    print("\n--- 排班时间范围 ---")
    year = int(input("请输入年份（例如：2024）："))
    start_month = int(input("请输入起始月份（1-12）："))
    end_month = int(input("请输入结束月份（1-12）："))

    print("\n--- 排班顺序设置 ---")
    continue_last_year = input("是否接续上一年的排班顺序？(y/n，默认n)：").strip().lower()
    # strip() 去空格；lower() 转小写
    start_group_index = 0  # 默认从第 1 组开始

    if continue_last_year == 'y':
        last_group = int(input(f"请输入上一年最后值班的组号（1-{group_count}）："))
        if 1 <= last_group <= group_count:
            start_group_index = last_group % group_count  # 取余实现"下一组"
            print(f"提示：本次排班将从第{start_group_index + 1}组开始")
        else:
            print("警告：输入的组号无效，将从第1组开始")
    else:
        print("提示：本次排班将从第1组开始")

    return groups, year, start_month, end_month, start_group_index
    # return 可以一次返回多个值


def main():
    """主流程：输入 -> 算日期 -> 生成排班 -> 导出 -> 统计"""
    try:
        groups, year, start_month, end_month, start_group_index = get_user_input()
        # 接收 5 个返回值

        print("\n正在分析日期...")
        schedule_dates = get_all_schedule_dates(year, start_month, end_month)
        print(f"共找到 {len(schedule_dates)} 个需要排班的日期")
        # len() 取列表长度

        print("\n正在生成排班表...")
        schedule = create_schedule(groups, schedule_dates, start_group_index)

        print("\n正在导出Excel文件...")
        filename = f"排班表_{year}年{start_month}-{end_month}月.xlsx"
        export_to_excel(schedule, groups, year, start_month, end_month, filename)

        print("\n" + "=" * 50)
        print("排班统计信息")
        print("=" * 50)

        df_schedule = pd.DataFrame(schedule)  # 转成 DataFrame 方便统计
        for i in range(len(groups)):
            total_days = (df_schedule['值班组'] == f"第{i+1}组").sum()
            # 比较得到布尔 Series，.sum() 把 True 当 1 加起来
            print(f"第{i+1}组：共值班 {total_days} 天")

        if schedule:
            # 列表非空时
            last_schedule_item = schedule[-1]  # [-1] 最后一个元素
            last_group = last_schedule_item['值班组']  # 字典取值
            last_date = last_schedule_item['日期'].strftime('%Y年%m月%d日')
            print(f"\n最后值班：{last_group}（{last_date}）")
            print("提示：下次排班时可选择接续此次排班顺序")

        print("\n排班完成！")

    except NotImplementedError as e:
        # 年份超出节假日库范围
        print(f"\n程序运行出错：{e}")
        print("提示：法定节假日数据随 chinesecalendar 库更新，支持 2004-2026 年。")
        print("      每年 11 月国务院发布次年安排后，执行 pip install -U chinesecalendar 可获取最新数据。")
    except Exception as e:
        # 捕获其他所有错误
        print(f"\n程序运行出错：{e}")
        print("请检查输入是否正确，或联系管理员。")


if __name__ == "__main__":
    # 直接运行本文件时执行；被 import 时 __name__ 是 "paiban.cli"
    main()
