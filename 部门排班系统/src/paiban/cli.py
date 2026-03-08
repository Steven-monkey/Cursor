"""
部门排班系统 - 命令行入口

【本文件在项目中的位置】
  - 位于：src/paiban/cli.py
  - 作用：提供命令行交互（input/print），收集用户输入后调用 core 做排班
  - 被谁调用：只有 run_cli.py，通过 from paiban.cli import main
  - 调用谁：from .core import ... 调用同包下的 core.py

【执行流程】
  run_cli.py 执行 main() → get_user_input() 获取输入 → get_all_schedule_dates → create_schedule → export_to_excel → 打印统计
"""

import pandas as pd  # 用于统计每组值班天数

# from .core：点号 . 表示"当前包"，即同目录下的 core.py
# 这样写的前提是 cli.py 在 paiban 包内，被 run_cli.py 以 from paiban.cli import main 方式加载
from .core import (
    get_all_schedule_dates,
    create_schedule,
    export_to_excel,
)


def get_user_input():
    """
    获取用户输入的组员信息和时间范围

    用 input() 在终端弹出一行让用户输入，用 print() 显示提示。
    返回值会传给后面的排班逻辑。

    返回值：
        groups: 如 [['张三','李四'], ['王五','赵六']]
        year, start_month, end_month: 排班时间范围
        start_group_index: 从第几组开始轮（0 表示第 1 组）
    """
    # 打印分隔线，让界面清晰
    print("=" * 50)  # 字符串 * 数字 = 重复 50 次
    print("欢迎使用部门排班系统")
    print("=" * 50)

    # input() 返回字符串，int() 转成整数
    group_count = int(input("\n请输入组数："))
    groups = []  # 空列表，用来存每组的人员

    for i in range(group_count):  # range(n) 生成 0,1,...,n-1
        print(f"\n--- 第{i+1}组 ---")  # f"..." 里 {i+1} 会替换成实际数字
        members = input(f"请输入第{i+1}组的组员名字（用逗号分隔）：")

        # split(',') 按逗号拆成列表；strip() 去掉前后空格
        # [x for x in ...] 叫列表推导式，对每个元素做相同处理
        member_list = [name.strip() for name in members.split(',')]
        groups.append(member_list)  # append 在末尾添加

    print("\n--- 排班时间范围 ---")
    year = int(input("请输入年份（例如：2024）："))
    start_month = int(input("请输入起始月份（1-12）："))
    end_month = int(input("请输入结束月份（1-12）："))

    print("\n--- 排班顺序设置 ---")
    # strip() 去首尾空格，lower() 转小写，方便只判断 'y'
    continue_last_year = input("是否接续上一年的排班顺序？(y/n，默认n)：").strip().lower()
    start_group_index = 0

    if continue_last_year == 'y':
        last_group = int(input(f"请输入上一年最后值班的组号（1-{group_count}）："))
        if 1 <= last_group <= group_count:  # 判断在有效范围内
            # 接续：从 last_group 的下一组开始
            # 例如 3 组，去年最后是第 2 组，则 (2 % 3)=2，即从第 3 组开始
            start_group_index = last_group % group_count
            print(f"提示：本次排班将从第{start_group_index + 1}组开始")
        else:
            print("警告：输入的组号无效，将从第1组开始")
    else:
        print("提示：本次排班将从第1组开始")

    # 用 return 一次返回多个值，接收时用多个变量
    return groups, year, start_month, end_month, start_group_index


def main():
    """
    主函数：程序的入口

    流程：获取输入 -> 分析日期 -> 生成排班 -> 导出 Excel -> 显示统计
    用 try-except 捕获错误，避免程序直接崩溃。
    """
    try:
        # 步骤 1：获取用户输入
        groups, year, start_month, end_month, start_group_index = get_user_input()

        # 步骤 2：获取需要排班的所有日期
        print("\n正在分析日期...")
        schedule_dates = get_all_schedule_dates(year, start_month, end_month)
        print(f"共找到 {len(schedule_dates)} 个需要排班的日期")  # len() 取列表长度

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
            # 统计"值班组"列中等于"第X组"的行数
            total_days = (df_schedule['值班组'] == f"第{i+1}组").sum()
            print(f"第{i+1}组：共值班 {total_days} 天")

        if schedule:
            last_schedule_item = schedule[-1]  # 列表[-1] 表示最后一个元素
            last_group = last_schedule_item['值班组']
            last_date = last_schedule_item['日期'].strftime('%Y年%m月%d日')
            print(f"\n最后值班：{last_group}（{last_date}）")
            print("提示：下次排班时可选择接续此次排班顺序")

        print("\n排班完成！")

    except NotImplementedError as e:
        # 节假日库不支持该年份时会抛出此异常
        print(f"\n程序运行出错：{e}")
        print("提示：法定节假日数据随 chinesecalendar 库更新，支持 2004-2026 年。")
        print("      每年 11 月国务院发布次年安排后，执行 pip install -U chinesecalendar 可获取最新数据。")
    except Exception as e:
        # 捕获其他所有异常，e 是异常对象
        print(f"\n程序运行出错：{e}")
        print("请检查输入是否正确，或联系管理员。")


# 当直接运行本文件时，__name__ 为 "__main__"
# 被其他文件 import 时，__name__ 为 "paiban.cli"
# 这样只有"直接运行"才执行 main()，import 时不会自动执行
if __name__ == "__main__":
    main()
