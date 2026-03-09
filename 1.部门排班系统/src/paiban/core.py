"""
core.py - 核心排班逻辑模块
作用：负责计算排班、导出 Excel，不负责界面
命令行和图形界面都会调用这里的函数
"""
import datetime
# 导入 datetime 模块，用于日期处理

from datetime import timedelta
# 从 datetime 导入 timedelta：表示时间间隔，如"1天"、"3小时"

import pandas as pd
# 导入 pandas，用于处理表格数据和 Excel

import chinese_calendar
# 导入 chinese_calendar 库：判断中国法定节假日、调休日


def get_all_schedule_dates(year, start_month, end_month):
    """
    找出指定年月范围内，所有需要排班的日期
    需要排班的 = 周末 + 法定节假日，但要排除调休日（周末被改成上班的那天）
    返回值：[(日期, 类型), ...]，类型如 "周末"、"法定节假日"、"周末+节假日"
    """
    # 起始日期：该年该月的 1 号
    start_date = datetime.date(year, start_month, 1)

    if end_month == 12:
        # 如果是 12 月：结束日期 = 12 月 31 日
        # 技巧：次年 1 月 1 日 - 1 天 = 12 月 31 日
        end_date = datetime.date(year + 1, 1, 1) - timedelta(days=1)
    else:
        # 非 12 月：结束日期 = 该月最后一天
        # 下月 1 日 - 1 天 = 当月最后一天
        end_date = datetime.date(year, end_month + 1, 1) - timedelta(days=1)

    # 空列表，用来存放 (日期, 类型) 的元组
    schedule_dates = []

    # pd.date_range：按天生成从 start 到 end 的日期序列，freq='D' 表示每天
    for dt in pd.date_range(start=start_date, end=end_date, freq='D'):
        # dt 是 pandas 的 Timestamp，.date() 转成 Python 的 date 对象
        d = dt.date()

        # d.weekday() 返回 0-6：0=周一，5=周六，6=周日
        # 所以 [5, 6] 表示周六和周日
        is_weekend = d.weekday() in [5, 6]

        # chinese_calendar.is_holiday：判断是否为法定节假日（如清明、国庆）
        is_holiday = chinese_calendar.is_holiday(d)

        # chinese_calendar.is_workday：判断是否工作日（含调休日）
        # 调休日 = 本来是周末，但被调成要上班
        is_workday = chinese_calendar.is_workday(d)

        # 调休日 = 本来是周末，但被改成要上班
        # 调休日不排值班，因为那天要上班
        is_makeup_workday = is_weekend and is_workday

        if is_makeup_workday:
            # continue 跳过本次循环，不把这一天加入结果
            continue

        # 只排周末或法定节假日
        if is_weekend or is_holiday:
            if is_holiday and not is_weekend:
                date_type = "法定节假日"
                # 如清明、端午在工作日时
            elif is_weekend and not is_holiday:
                date_type = "周末"
            else:
                date_type = "周末+节假日"
                # 如国庆假期里的周六，既是周末又是节假日
            # append 把 (日期, 类型) 元组加到列表末尾
            schedule_dates.append((d, date_type))

    return schedule_dates


def get_holiday_periods(schedule_dates):
    """
    把连续的排班日期分成一段段（时段）
    劳动节 5.3、国庆节 10.4 会强制拆成两段（前期、后期）
    返回值：[[(日期,类型), ...], [(日期,类型), ...], ...]
    """
    if not schedule_dates:
        # 空列表时，not schedule_dates 为 True，直接返回空列表
        return []

    holiday_periods = []
    # 当前正在处理的一段
    current_period = []

    # enumerate 同时得到下标 i 和元素，元素是 (date, date_type) 元组
    for i, (date, date_type) in enumerate(schedule_dates):
        should_split = False
        if date.month == 5 and date.day == 3:
            # 劳动节：5.1-5.2 一段，5.3-5.5 一段
            should_split = True
        elif date.month == 10 and date.day == 4:
            # 国庆节：10.1-10.3 一段，10.4-10.7 一段
            should_split = True

        if should_split and current_period:
            # 遇到断点且当前段不为空：先存当前段，再开新段
            holiday_periods.append(current_period)
            current_period = [(date, date_type)]
        elif i == 0:
            # 第一个日期直接加入当前段
            current_period.append((date, date_type))
        else:
            # 取上一个日期的 date 部分，[0] 是元组的第一个元素
            prev_date = schedule_dates[i - 1][0]
            # 两日期相减得 timedelta，.days 取天数差
            days_diff = (date - prev_date).days
            if days_diff == 1:
                # 连续（只差 1 天），加入当前段
                current_period.append((date, date_type))
            else:
                # 不连续，存当前段并开新段
                if current_period:
                    holiday_periods.append(current_period)
                current_period = [(date, date_type)]

    if current_period:
        # 循环结束后，最后一段别忘了加入
        holiday_periods.append(current_period)

    return holiday_periods


def get_period_identifier(period):
    """
    给这段假期打标签，用于特殊规则（劳动节/国庆节分前后期）
    返回值如 "劳动节前期"、"国庆节后期"、"连休_20240501" 或 None（普通周末）
    """
    # period[0] 是第一个 (date, date_type)，[0] 取日期
    first_date = period[0][0]

    # any(可迭代对象)：只要有一个 True 就返回 True
    # for date, _ in period：遍历，_ 表示忽略第二项（date_type）
    has_holiday = any(chinese_calendar.is_holiday(date) for date, _ in period)

    # 列表推导：取出这段里所有日期
    period_dates = [date for date, _ in period]

    # 劳动节、国庆节的日期范围，用于判断这段属于哪部分
    labor_day_early = [datetime.date(first_date.year, 5, 1), datetime.date(first_date.year, 5, 2)]
    labor_day_late = [datetime.date(first_date.year, 5, 3), datetime.date(first_date.year, 5, 4), datetime.date(first_date.year, 5, 5)]
    national_day_early = [datetime.date(first_date.year, 10, 1), datetime.date(first_date.year, 10, 2), datetime.date(first_date.year, 10, 3)]
    national_day_late = [datetime.date(first_date.year, 10, 4), datetime.date(first_date.year, 10, 5), datetime.date(first_date.year, 10, 6), datetime.date(first_date.year, 10, 7)]

    # 按优先级判断这段属于哪种类型
    if any(date in labor_day_early for date in period_dates):
        return "劳动节前期"
    elif any(date in labor_day_late for date in period_dates):
        return "劳动节后期"
    elif any(date in national_day_early for date in period_dates):
        return "国庆节前期"
    elif any(date in national_day_late for date in period_dates):
        return "国庆节后期"
    elif has_holiday and len(period) > 1:
        # 有节假日且是多天连休，用日期做标签
        return f"连休_{first_date.strftime('%Y%m%d')}"
    else:
        # 普通周末，不需要固定组
        return None


def create_schedule(groups, schedule_dates, start_group_index=0):
    """
    生成完整排班表
    流程：分时段 -> 对特殊时段分配固定组 -> 逐日分配 -> 拼结果
    返回值：列表，每个元素是 {'日期','星期','类型','值班组','值班人员'} 的字典
    """
    schedule = []

    # 记录每个组每月已排天数：键 (组索引, 年, 月)，值 天数
    group_month_count = {}
    # 记录每个组上次值班日期：键 组索引，值 日期
    last_schedule_date = {}
    # 当前轮到哪一组（0 表示第 1 组）
    current_group_index = start_group_index
    # 特殊时段（劳动节/国庆节等）已分配给哪组：键 时段标签，值 组索引
    period_assigned = {}

    # 先按连续日期分成时段
    holiday_periods = get_holiday_periods(schedule_dates)

    for period in holiday_periods:
        period_id = get_period_identifier(period)

        # 如果是特殊时段且还没分配，选一组承担整段
        if period_id and period_id not in period_assigned:
            assigned_group = find_available_group_for_period(
                groups, current_group_index, period,
                group_month_count, last_schedule_date
            )
            period_assigned[period_id] = assigned_group
            # 下一组：取余实现循环，如 3 组时 (2+1)%3=0
            current_group_index = (assigned_group + 1) % len(groups)

        # 遍历这段里的每一天
        for date, date_type in period:
            if period_id and period_id in period_assigned:
                # 特殊段用已分配的固定组
                assigned_group = period_assigned[period_id]
            else:
                # 普通日子按规则找可用组
                assigned_group = find_available_group(
                    groups, current_group_index, date,
                    group_month_count, last_schedule_date
                )
                current_group_index = (assigned_group + 1) % len(groups)

            # 更新该组本月已排天数
            month_key = (assigned_group, date.year, date.month)
            # .get(键, 0)：没有则返回 0，再 +1
            group_month_count[month_key] = group_month_count.get(month_key, 0) + 1
            last_schedule_date[assigned_group] = date

            # 星期名称列表，date.weekday() 返回 0-6
            weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            weekday = weekday_names[date.weekday()]
            # 用顿号连接该组所有成员
            members_str = '、'.join(groups[assigned_group])

            schedule.append({
                '日期': date,
                '星期': weekday,
                '类型': date_type,
                '值班组': f"第{assigned_group + 1}组",
                '值班人员': members_str
            })

    return schedule


def find_available_group_for_period(groups, start_index, period, group_month_count, last_schedule_date):
    """
    为整段假期找一组：满足"每月不超 4 天"、"离上次值班至少 2 天"
    返回值：组索引
    """
    group_count = len(groups)
    first_date = period[0][0]

    for i in range(group_count):
        # 从 start_index 开始轮流试
        group_index = (start_index + i) % group_count
        can_assign = True
        # 统计这段假期在各月占几天（可能跨月，如 4.30-5.2）
        month_days = {}

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

        # 检查离上次值班是否至少 2 天
        if group_index in last_schedule_date:
            last_date = last_schedule_date[group_index]
            days_diff = (first_date - last_date).days
            if days_diff < 2:
                continue

        return group_index

    # 找不到满足条件的组，兜底返回起始组
    return start_index


def find_available_group(groups, start_index, date, group_month_count, last_schedule_date):
    """
    为单天找一组：本月未满 4 天，离上次值班至少 2 天
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
    把排班结果写成 Excel 文件
    schedule：排班列表；groups：组员；year, start_month, end_month：时间范围
    """
    title = f"{year}年{start_month}月-{end_month}月值班排班表"
    # 表头：第一行标题，后面 4 个空单元格
    header_rows = [[title, "", "", "", ""]]
    for i, group in enumerate(groups):
        header_rows.append([f"第{i+1}组：{'、'.join(group)}", "", "", "", ""])
    header_rows.append(["", "", "", "", ""])
    header_rows.append(["日期", "星期", "类型", "值班组", "值班人员"])

    # 把排班数据转成 DataFrame（pandas 的表格结构）
    df_data = pd.DataFrame(schedule)
    # 把日期列格式化为 "2024-01-06" 字符串
    # apply：对每一行执行 lambda 函数；lambda x: x.strftime(...) 匿名函数
    df_data["日期"] = df_data["日期"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df_data = df_data[["日期", "星期", "类型", "值班组", "值班人员"]]

    df_header = pd.DataFrame(header_rows)
    # concat 拼接两个表格；ignore_index=True 重新编号行索引
    df_full = pd.concat([df_header, df_data], ignore_index=True)

    # with 语句：自动在结束时关闭文件，即使发生异常也会关闭
    # engine="xlsxwriter" 指定用 xlsxwriter 写 xlsx 格式
    with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
        # to_excel：写入 Excel；index=False 不写行号；header=False 因为表头已在数据里
        df_full.to_excel(writer, sheet_name=f"{year}年排班表", index=False, header=False)
        ws = writer.sheets[f"{year}年排班表"]
        # 设置列宽，让显示更美观
        ws.set_column("A:A", 15)
        ws.set_column("B:B", 10)
        ws.set_column("C:C", 15)
        ws.set_column("D:D", 12)
        ws.set_column("E:E", 30)

    print(f"\n排班表已成功导出到：{filename}")
