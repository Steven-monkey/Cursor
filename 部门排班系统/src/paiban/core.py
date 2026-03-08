"""
部门排班系统 - 核心排班逻辑

【本文件在项目中的位置】
  - 位于：src/paiban/core.py
  - 作用：排班的"最底层"逻辑，只做计算和导出，不依赖 cli、gui
  - 被谁调用：cli.py 和 gui.py 都 import 本文件的 get_all_schedule_dates、create_schedule、export_to_excel
  - 调用谁：只调用标准库和第三方库（datetime、pandas、chinese_calendar），不 import 本项目的 cli、gui

【核心逻辑流程】
  1. get_all_schedule_dates：根据年月范围，筛出需要排班的日期（周末+节假日，排除调休日）
  2. get_holiday_periods：把日期按"连续"分成多段（劳动节、国庆节强制分段）
  3. get_period_identifier：为每段打标签（如"劳动节前期"），用于连休固定同一组
  4. create_schedule：按规则分配值班组，生成排班表
  5. export_to_excel：导出到 xlsx 文件
"""

# ==================== 导入库 ====================
# import 用来引入别人写好的代码，避免重复造轮子
import datetime  # 处理日期：创建日期、计算日期间隔等
from datetime import timedelta  # 从 datetime 里单独导入 timedelta，用于表示"一段时间"（如 1 天）
import pandas as pd  # 数据分析库，这里用来生成日期序列、导出 Excel
import chinese_calendar  # 中国节假日库：判断某天是节假日、工作日还是调休日


def get_all_schedule_dates(year, start_month, end_month):
    """
    获取指定时间范围内所有需要排班的日期（周末和法定节假日）

    参数说明：
        year: 年份，如 2024
        start_month: 起始月份，1-12
        end_month: 结束月份，1-12

    返回值：
        列表，每个元素是 (日期, 类型) 元组，如 [(date(2024,1,6), "周末"), ...]
    """
    # 计算起始日期：该年该月的 1 号
    start_date = datetime.date(year, start_month, 1)

    # 计算结束日期：若是 12 月则用年末，否则用 end_month 的下月 1 号减 1 天
    # 三元表达式：条件 if 真 else 假
    if end_month == 12:
        end_date = datetime.date(year + 1, 1, 1) - timedelta(days=1)  # 12月31日
    else:
        end_date = datetime.date(year, end_month + 1, 1) - timedelta(days=1)

    # 存放需要排班的日期的列表
    schedule_dates = []

    # pd.date_range 按天生成从 start_date 到 end_date 的日期序列，freq='D' 表示每天
    for dt in pd.date_range(start=start_date, end=end_date, freq='D'):
        d = dt.date()  # pandas 的 Timestamp 转成 Python 的 date 对象

        # 判断是不是周末：weekday() 返回 0-6，5=周六，6=周日
        is_weekend = d.weekday() in [5, 6]

        # chinese_calendar 判断：是不是法定节假日（如春节、国庆）
        is_holiday = chinese_calendar.is_holiday(d)

        # 判断是不是工作日（要上班的日子，包括调休的周末）
        is_workday = chinese_calendar.is_workday(d)

        # 调休日：本来是周末，但被调成要上班，如国庆前后的周六
        # 这种日子不安排值班！
        is_makeup_workday = is_weekend and is_workday

        if is_makeup_workday:
            continue  # 跳过调休日，不加入排班

        # 只排周末和法定节假日
        if is_weekend or is_holiday:
            # 确定日期类型，方便后面在 Excel 里区分显示
            if is_holiday and not is_weekend:
                date_type = "法定节假日"  # 如清明、端午（在工作日时）
            elif is_weekend and not is_holiday:
                date_type = "周末"
            else:
                date_type = "周末+节假日"  # 既是周末又是节假日，如国庆中的周六
            # append 在列表末尾添加元素；(d, date_type) 是元组
            schedule_dates.append((d, date_type))

    return schedule_dates


def get_holiday_periods(schedule_dates):
    """
    识别所有连续的假期时段（包括周末+节假日连休）

    把一串日期按"连续"分成多段，如 1.6-1.7 是一段，5.1-5.5 劳动节是一段。
    劳动节、国庆节会强制分成两段（前期/后期），满足排班规则。

    参数：
        schedule_dates: [(date, type), ...] 需要排班的日期列表

    返回值：
        列表的列表，如 [[(d1,t1),(d2,t2)], [(d3,t3)], ...]，每个内层列表是一段连续假期
    """
    if not schedule_dates:
        return []  # 空列表的布尔值为 False，not [] 为 True

    holiday_periods = []  # 所有时段
    current_period = []   # 当前正在处理的一段

    # enumerate 同时得到索引 i 和元素 (date, date_type)
    for i, (date, date_type) in enumerate(schedule_dates):
        # 劳动节 5 月 3 日、国庆 10 月 4 日需要强制分段，保证同组不连值太多天
        should_split = False
        if date.month == 5 and date.day == 3:
            should_split = True   # 5.1-5.2 一段，5.3-5.5 一段
        elif date.month == 10 and date.day == 4:
            should_split = True   # 10.1-10.3 一段，10.4-10.7 一段

        if should_split and current_period:
            # 先保存当前时段，再开新段
            holiday_periods.append(current_period)
            current_period = [(date, date_type)]
        elif i == 0:
            # 第一个日期直接加入
            current_period.append((date, date_type))
        else:
            # 看和上一个日期是否连续（相差 1 天）
            prev_date = schedule_dates[i - 1][0]  # [0] 取元组的第一个元素（日期）
            days_diff = (date - prev_date).days   # 日期相减得到 timedelta，.days 取天数

            if days_diff == 1:
                current_period.append((date, date_type))
            else:
                # 不连续，当前时段结束，开新段
                if current_period:
                    holiday_periods.append(current_period)
                current_period = [(date, date_type)]

    # 最后一段别漏掉
    if current_period:
        holiday_periods.append(current_period)

    return holiday_periods


def get_period_identifier(period):
    """
    为假期时段生成唯一标识符，用于"连休假期固定同一组值班"

    劳动节、国庆节分前期/后期；其他多天连休（如清明、端午）用"连休_年月日"。
    普通周末返回 None，表示可以正常轮流排班。

    参数：
        period: 一段假期，如 [(date,t),(date,t),...]

    返回值：
        字符串如 "劳动节前期"，或 None
    """
    first_date = period[0][0]  # period[0] 是第一个 (date,type)，[0] 取 date

    # any()：只要有一个为 True 就返回 True
    # for date, _ in period：遍历每个元组，_ 表示忽略第二个元素
    has_holiday = any(chinese_calendar.is_holiday(date) for date, _ in period)

    # 列表推导式：取出所有日期
    period_dates = [date for date, _ in period]

    # 定义劳动节、国庆节的前期、后期日期
    labor_day_early = [datetime.date(first_date.year, 5, 1), datetime.date(first_date.year, 5, 2)]
    labor_day_late = [datetime.date(first_date.year, 5, 3), datetime.date(first_date.year, 5, 4), datetime.date(first_date.year, 5, 5)]
    national_day_early = [datetime.date(first_date.year, 10, 1), datetime.date(first_date.year, 10, 2), datetime.date(first_date.year, 10, 3)]
    national_day_late = [datetime.date(first_date.year, 10, 4), datetime.date(first_date.year, 10, 5), datetime.date(first_date.year, 10, 6), datetime.date(first_date.year, 10, 7)]

    # 检查这段假期落在哪个区间，返回对应标识
    if any(date in labor_day_early for date in period_dates):
        return "劳动节前期"
    elif any(date in labor_day_late for date in period_dates):
        return "劳动节后期"
    elif any(date in national_day_early for date in period_dates):
        return "国庆节前期"
    elif any(date in national_day_late for date in period_dates):
        return "国庆节后期"
    elif has_holiday and len(period) > 1:
        # 其他多天连休（清明、端午等）
        return f"连休_{first_date.strftime('%Y%m%d')}"  # 如 连休_20240404
    else:
        return None  # 普通周末，不需要固定组


def create_schedule(groups, schedule_dates, start_group_index=0):
    """
    创建排班表（核心函数）

    【逻辑流程】
        1. get_holiday_periods：把 schedule_dates 按连续日期分成多段
        2. 遍历每段：get_period_identifier 判断是"劳动节前期"等特殊段还是普通周末
        3. 特殊段：用 find_available_group_for_period 选一组承担整段，记到 period_assigned
        4. 普通段：每天用 find_available_group 轮流选组
        5. 每个日期：更新 group_month_count、last_schedule_date，拼成一行排班记录

    参数：
        groups: 如 [['张三','李四'], ['王五','赵六']]，每组的人员列表
        schedule_dates: 需要排班的日期列表
        start_group_index: 从哪一组开始轮（0 表示第 1 组），用于接续上一年

    返回值：
        列表，每个元素是字典：{'日期','星期','类型','值班组','值班人员'}
    """
    schedule = []  # 排班结果

    # 记录每组每月已排几天，键 (组索引, 年, 月)，值 天数
    group_month_count = {}

    # 记录每组最后一次值班的日期，避免连续值班
    last_schedule_date = {}

    current_group_index = start_group_index  # 当前轮到哪一组
    period_assigned = {}  # 某段假期已分配给哪组，键 时段标识，值 组索引

    # 第一步：把日期按"连续"分时段，如 [[1.6,1.7], [5.1,5.2,5.3,5.4,5.5], ...]
    holiday_periods = get_holiday_periods(schedule_dates)

    for period in holiday_periods:
        period_id = get_period_identifier(period)  # "劳动节前期" / "连休_20240404" / None（普通周末）

        # 第二步：若是特殊段且未分配，选一组承担整段
        if period_id and period_id not in period_assigned:
            assigned_group = find_available_group_for_period(
                groups, current_group_index, period,
                group_month_count, last_schedule_date
            )
            period_assigned[period_id] = assigned_group
            # 下一段从下一组开始轮
            current_group_index = (assigned_group + 1) % len(groups)  # 下一段从下一组开始轮

        # 第三步：遍历时段内每一天，确定值班组
        for date, date_type in period:
            if period_id and period_id in period_assigned:
                assigned_group = period_assigned[period_id]
            else:
                assigned_group = find_available_group(
                    groups, current_group_index, date,
                    group_month_count, last_schedule_date
                )
                current_group_index = (assigned_group + 1) % len(groups)

            # 更新统计
            month_key = (assigned_group, date.year, date.month)
            # get(key, 0)：没有则返回 0
            group_month_count[month_key] = group_month_count.get(month_key, 0) + 1
            last_schedule_date[assigned_group] = date

            weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            weekday = weekday_names[date.weekday()]
            members_str = '、'.join(groups[assigned_group])  # 用顿号连接成员名

            schedule.append({
                '日期': date,
                '星期': weekday,
                '类型': date_type,
                '值班组': f"第{assigned_group + 1}组",  # 索引从 0 开始，显示用 1 开始
                '值班人员': members_str
            })

    return schedule


def find_available_group_for_period(groups, start_index, period, group_month_count, last_schedule_date):
    """
    为整个假期时段找一个可用的组

    要求：该组承担这段假期后，每月不超过 4 天，且与上次值班至少间隔 2 天。

    参数：
        groups: 所有组
        start_index: 从哪组开始试
        period: 这段假期
        group_month_count: 各组每月已排天数
        last_schedule_date: 各组上次值班日期

    返回值：
        可用的组索引（0,1,2,...）
    """
    group_count = len(groups)
    first_date = period[0][0]

    for i in range(group_count):
        # 轮流尝试每一组
        group_index = (start_index + i) % group_count
        can_assign = True
        month_days = {}  # 这段假期在各月的天数

        for date, _ in period:
            month_key = (date.year, date.month)
            month_days[month_key] = month_days.get(month_key, 0) + 1

        for month_key, days_needed in month_days.items():
            year, month = month_key
            current_count = group_month_count.get((group_index, year, month), 0)
            if current_count + days_needed > 4:
                can_assign = False
                break

        if not can_assign:
            continue

        # 检查会不会造成连续值班
        if group_index in last_schedule_date:
            last_date = last_schedule_date[group_index]
            days_diff = (first_date - last_date).days
            if days_diff < 2:  # 间隔至少 2 天
                continue

        return group_index

    return start_index  # 都找不到时兜底


def find_available_group(groups, start_index, date, group_month_count, last_schedule_date):
    """
    为单天找一个可用的组（普通周末用）

    要求：该组本月未满 4 天，且与上次值班至少间隔 2 天。
    """
    group_count = len(groups)

    for i in range(group_count):
        group_index = (start_index + i) % group_count
        month_key = (group_index, date.year, date.month)
        current_count = group_month_count.get(month_key, 0)

        if current_count >= 4:
            continue

        if group_index in last_schedule_date:
            last_date = last_schedule_date[group_index]
            days_diff = (date - last_date).days
            if days_diff < 2:
                continue

        return group_index

    return start_index


def export_to_excel(schedule, groups, year, start_month, end_month, filename="排班表.xlsx"):
    """
    把排班结果导出到 Excel 文件

    参数：
        schedule: 排班结果列表
        groups: 组信息
        year, start_month, end_month: 时间范围
        filename: 保存的文件名
    """
    title = f"{year}年{start_month}月-{end_month}月值班排班表"
    header_rows = [[title, "", "", "", ""]]
    for i, group in enumerate(groups):
        header_rows.append([f"第{i+1}组：{'、'.join(group)}", "", "", "", ""])
    header_rows.append(["", "", "", "", ""])
    header_rows.append(["日期", "星期", "类型", "值班组", "值班人员"])

    # DataFrame 是 pandas 的表格结构
    df_data = pd.DataFrame(schedule)
    df_data["日期"] = df_data["日期"].apply(lambda x: x.strftime("%Y-%m-%d"))  # 日期格式化为字符串
    df_data = df_data[["日期", "星期", "类型", "值班组", "值班人员"]]

    df_header = pd.DataFrame(header_rows)
    df_full = pd.concat([df_header, df_data], ignore_index=True)  # 表头+数据拼在一起

    with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
        df_full.to_excel(writer, sheet_name=f"{year}年排班表", index=False, header=False)
        ws = writer.sheets[f"{year}年排班表"]
        ws.set_column("A:A", 15)
        ws.set_column("B:B", 10)
        ws.set_column("C:C", 15)
        ws.set_column("D:D", 12)
        ws.set_column("E:E", 30)

    print(f"\n排班表已成功导出到：{filename}")
