"""
cli.py - 命令行入口

这个文件做什么？
  用 input() 让用户输入，用 print() 显示提示，然后调用 core 里的函数生成排班。

谁调用它？
  run_cli.py 会写 from paiban.cli import main，然后执行 main()。

它调用谁？
  调用同文件夹下的 core.py（from .core import xxx，点号表示"当前这个包"）。
"""

import pandas as pd  # 后面统计每组值班几天用

from .core import (  # . 表示和 cli 同一个包里的 core
    get_all_schedule_dates,
    create_schedule,
    export_to_excel,
)


def get_user_input():
    """
    让用户在终端里输入：组数、每组人员、年份月份、是否接续。
    返回这些信息给 main() 用。
    """
    print("=" * 50)  # "=" * 50 表示 50 个等号
    print("欢迎使用部门排班系统")
    print("=" * 50)

    # input() 返回字符串，int() 转成整数
    group_count = int(input("\n请输入组数："))  # input 得到的是字符串，int() 转成数字
    groups = []  # 空列表

    for i in range(group_count):
        print(f"\n--- 第{i+1}组 ---")  # f"..." 里的 {i+1} 会替换成真实数字
        members = input(f"请输入第{i+1}组的组员名字（用逗号分隔）：")

        member_list = [name.strip() for name in members.split(',')]  # 按逗号拆开，再去掉空格
        groups.append(member_list)  # 加到 groups 里

    print("\n--- 排班时间范围 ---")
    year = int(input("请输入年份（例如：2024）："))
    start_month = int(input("请输入起始月份（1-12）："))
    end_month = int(input("请输入结束月份（1-12）："))

    print("\n--- 排班顺序设置 ---")
    continue_last_year = input("是否接续上一年的排班顺序？(y/n，默认n)：").strip().lower()  # 去空格、转小写
    start_group_index = 0

    if continue_last_year == 'y':
        last_group = int(input(f"请输入上一年最后值班的组号（1-{group_count}）："))
        if 1 <= last_group <= group_count:
            start_group_index = last_group % group_count  # % 取余，实现"下一组"的循环
            print(f"提示：本次排班将从第{start_group_index + 1}组开始")
        else:
            print("警告：输入的组号无效，将从第1组开始")
    else:
        print("提示：本次排班将从第1组开始")

    return groups, year, start_month, end_month, start_group_index  # 可以一次返回多个值


def main():
    """
    主函数。流程：要输入 -> 算日期 -> 生成排班 -> 导出Excel -> 打印统计。
    try-except 用来抓错误，出错时不会直接闪退。
    """
    try:
        # 步骤 1：获取用户输入
        groups, year, start_month, end_month, start_group_index = get_user_input()

        # 步骤 2：获取需要排班的所有日期
        print("\n正在分析日期...")
        schedule_dates = get_all_schedule_dates(year, start_month, end_month)
        print(f"共找到 {len(schedule_dates)} 个需要排班的日期")

        # 步骤 3：生成排班表
        print("\n正在生成排班表...")
        schedule = create_schedule(groups, schedule_dates, start_group_index)

        # 步骤 4：导出到 Excel
        print("\n正在导出Excel文件...")
        filename = f"排班表_{year}年{start_month}-{end_month}月.xlsx"
        export_to_excel(schedule, groups, year, start_month, end_month, filename)

        # 步骤 5：显示统计信息
        print("\n" + "=" * 50)
        print("排班统计信息")
        print("=" * 50)

        df_schedule = pd.DataFrame(schedule)
        for i in range(len(groups)):
            total_days = (df_schedule['值班组'] == f"第{i+1}组").sum()  # 数这组值了多少天
            print(f"第{i+1}组：共值班 {total_days} 天")

        if schedule:
            last_schedule_item = schedule[-1]  # [-1] 表示最后一个
            last_group = last_schedule_item['值班组']
            last_date = last_schedule_item['日期'].strftime('%Y年%m月%d日')
            print(f"\n最后值班：{last_group}（{last_date}）")
            print("提示：下次排班时可选择接续此次排班顺序")

        print("\n排班完成！")

    except NotImplementedError as e:
        # 年份超出节假日库支持范围
        print(f"\n程序运行出错：{e}")
        print("提示：法定节假日数据随 chinesecalendar 库更新，支持 2004-2026 年。")
        print("      每年 11 月国务院发布次年安排后，执行 pip install -U chinesecalendar 可获取最新数据。")
    except Exception as e:
        # 其他错误
        print(f"\n程序运行出错：{e}")
        print("请检查输入是否正确，或联系管理员。")


# 只有"直接运行这个文件"时才会执行 main；被 import 时不会执行
if __name__ == "__main__":
    main()
