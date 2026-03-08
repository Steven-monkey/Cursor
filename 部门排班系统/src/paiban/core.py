"""
core.py - 核心排班逻辑
负责算排班和导出 Excel，不负责界面。
"""
import datetime  # 日期处理
from datetime import timedelta  # 表示时间间隔，如"1天"
import pandas as pd  # 表格、Excel，pd 是别名
import chinese_calendar  # 判断中国节假日、调休日


def get_all_schedule_dates(year, start_month, end_month):
    """找出需要排班的所有日期（周末+节假日，排除调休）"""
    # 起始日期：该年该月 1 号
    start_date = datetime.date(year, start_month, 1)

    if end_month == 12:
        # 12 月：结束日期 = 次年 1 月 1 日 - 1 天 = 12 月 31 日
        end_date = datetime.date(year + 1, 1, 1) - timedelta(days=1)
    else:
        # 非 12 月：结束日期 = 下月 1 日 - 1 天
        end_date = datetime.date(year, end_month + 1, 1) - timedelta(days=1)

    schedule_dates = []  # 空列表，存 (日期, 类型) 元组

    for dt in pd.date_range(start=start_date, end=end_date, freq='D'):
        # pd.date_range 按天生成日期；freq='D' 表示每天；dt 是 pandas 的日期
        d = dt.date()  # 转成 Python 的 date 对象

        is_weekend = d.weekday() in [5, 6]
        # weekday() 返回 0-6，5=周六 6=周日；in 判断是否在列表里

        is_holiday = chinese_calendar.is_holiday(d)  # 是否法定节假日

        is_workday = chinese_calendar.is_workday(d)  # 是否工作日（含调休）

        is_makeup_workday = is_weekend and is_workday
        # 调休日 = 周末但被改成要上班；调休日不排值班

        if is_makeup_workday:
            continue  # 跳过调休日，不加入结果

        if is_weekend or is_holiday:
            # 只排周末或法定节假日
            if is_holiday and not is_weekend:
                date_type = "法定节假日"  # 如清明、端午在工作日时
            elif is_weekend and not is_holiday:
                date_type = "周末"
            else:
                date_type = "周末+节假日"  # 如国庆里的周六
            schedule_dates.append((d, date_type))  # append 加到列表末尾；(d, date_type) 是元组

    return schedule_dates  # 返回日期列表


def get_holiday_periods(schedule_dates):
    """把日期按"连续"分成一段段；劳动节、国庆节强制拆两段"""
    if not schedule_dates:
        return []  # 空列表时直接返回

    holiday_periods = []  # 存所有段，每段是一个列表
    current_period = []   # 当前正在处理的一段

    for i, (date, date_type) in enumerate(schedule_dates):
        # enumerate 同时得到下标 i 和元素；元素是 (date, date_type) 元组
        should_split = False  # 是否要强制断开
        if date.month == 5 and date.day == 3:
            should_split = True   # 劳动节 5.3 断开：5.1-5.2 一段，5.3-5.5 一段
        elif date.month == 10 and date.day == 4:
            should_split = True   # 国庆 10.4 断开：10.1-10.3 一段，10.4-10.7 一段

        if should_split and current_period:
            holiday_periods.append(current_period)  # 先存当前段
            current_period = [(date, date_type)]   # 开新段，当前日期作为第一天
        elif i == 0:
            current_period.append((date, date_type))  # 第一个日期直接加
        else:
            prev_date = schedule_dates[i - 1][0]  # 上一个日期的 date；[0] 取元组第一个元素
            days_diff = (date - prev_date).days   # 两日期相减得 timedelta，.days 取天数
            if days_diff == 1:
                current_period.append((date, date_type))  # 连续则加入当前段
            else:
                if current_period:
                    holiday_periods.append(current_period)  # 不连续则存当前段
                current_period = [(date, date_type)]  # 开新段

    if current_period:
        holiday_periods.append(current_period)  # 最后一段别忘了

    return holiday_periods


def get_period_identifier(period):
    """给这段假期打标签：劳动节前期/国庆节后期/连休_日期/None"""
    first_date = period[0][0]  # period[0] 第一个元组，[0] 取日期

    has_holiday = any(chinese_calendar.is_holiday(date) for date, _ in period)
    # any：任一为 True 则 True；for date, _ in period 遍历，_ 忽略第二项

    period_dates = [date for date, _ in period]  # 列表推导：取出所有日期

    labor_day_early = [datetime.date(first_date.year, 5, 1), datetime.date(first_date.year, 5, 2)]
    labor_day_late = [datetime.date(first_date.year, 5, 3), datetime.date(first_date.year, 5, 4), datetime.date(first_date.year, 5, 5)]
    national_day_early = [datetime.date(first_date.year, 10, 1), datetime.date(first_date.year, 10, 2), datetime.date(first_date.year, 10, 3)]
    national_day_late = [datetime.date(first_date.year, 10, 4), datetime.date(first_date.year, 10, 5), datetime.date(first_date.year, 10, 6), datetime.date(first_date.year, 10, 7)]

    if any(date in labor_day_early for date in period_dates):
        return "劳动节前期"
    elif any(date in labor_day_late for date in period_dates):
        return "劳动节后期"
    elif any(date in national_day_early for date in period_dates):
        return "国庆节前期"
    elif any(date in national_day_late for date in period_dates):
        return "国庆节后期"
    elif has_holiday and len(period) > 1:
        return f"连休_{first_date.strftime('%Y%m%d')}"  # strftime 格式化日期
    else:
        return None  # 普通周末，不需要固定组


def create_schedule(groups, schedule_dates, start_group_index=0):
    """生成排班表：分时段、分配组、拼结果"""
    schedule = []  # 最终排班结果

    group_month_count = {}   # 键 (组索引, 年, 月)，值：该组该月已排天数
    last_schedule_date = {}  # 键 组索引，值：该组上次值班日期
    current_group_index = start_group_index  # 当前轮到第几组（从 0 开始）
    period_assigned = {}     # 键 时段标签，值：已分配的组索引

    holiday_periods = get_holiday_periods(schedule_dates)  # 先分时段

    for period in holiday_periods:
        period_id = get_period_identifier(period)  # 这段的标签

        if period_id and period_id not in period_assigned:
            # 特殊段且未分配：选一组承担整段
            assigned_group = find_available_group_for_period(
                groups, current_group_index, period,
                group_month_count, last_schedule_date
            )
            period_assigned[period_id] = assigned_group  # 记下来
            current_group_index = (assigned_group + 1) % len(groups)
            # % 取余：3 组时 (2+1)%3=0，实现循环

        for date, date_type in period:
            # 遍历这段里每一天
            if period_id and period_id in period_assigned:
                assigned_group = period_assigned[period_id]  # 特殊段用固定组
            else:
                assigned_group = find_available_group(
                    groups, current_group_index, date,
                    group_month_count, last_schedule_date
                )
                current_group_index = (assigned_group + 1) % len(groups)

            month_key = (assigned_group, date.year, date.month)  # 月度键
            group_month_count[month_key] = group_month_count.get(month_key, 0) + 1
            # get(键, 0)：没有则返回 0，再 +1
            last_schedule_date[assigned_group] = date  # 更新该组上次值班日

            weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            weekday = weekday_names[date.weekday()]  # weekday() 返回 0-6
            members_str = '、'.join(groups[assigned_group])  # 用顿号连接名单

            schedule.append({
                '日期': date,
                '星期': weekday,
                '类型': date_type,
                '值班组': f"第{assigned_group + 1}组",  # 显示用 1 开始
                '值班人员': members_str
            })

    return schedule


def find_available_group_for_period(groups, start_index, period, group_month_count, last_schedule_date):
    """给整段找一组：每月不超 4 天，离上次值班至少 2 天"""
    group_count = len(groups)  # 组数
    first_date = period[0][0]  # 这段第一天

    for i in range(group_count):
        group_index = (start_index + i) % group_count  # 轮流试各组
        can_assign = True  # 假设可分配
        month_days = {}    # 这段在各月占几天（可能跨月）

        for date, _ in period:
            month_key = (date.year, date.month)
            month_days[month_key] = month_days.get(month_key, 0) + 1

        for month_key, days_needed in month_days.items():
            # items() 返回 (键, 值) 对
            year, month = month_key
            current_count = group_month_count.get((group_index, year, month), 0)
            if current_count + days_needed > 4:
                can_assign = False
                break  # 超了 4 天，换下一组

        if not can_assign:
            continue

        if group_index in last_schedule_date:
            last_date = last_schedule_date[group_index]
            days_diff = (first_date - last_date).days
            if days_diff < 2:
                continue  # 间隔不足 2 天

        return group_index  # 找到可用组

    return start_index  # 找不到就兜底返回


def find_available_group(groups, start_index, date, group_month_count, last_schedule_date):
    """给单天找一组：本月未满 4 天，离上次至少 2 天"""
    group_count = len(groups)

    for i in range(group_count):
        group_index = (start_index + i) % group_count
        month_key = (group_index, date.year, date.month)
        current_count = group_month_count.get(month_key, 0)

        if current_count >= 4:
            continue  # 本月已满

        if group_index in last_schedule_date:
            last_date = last_schedule_date[group_index]
            days_diff = (date - last_date).days
            if days_diff < 2:
                continue

        return group_index

    return start_index


def export_to_excel(schedule, groups, year, start_month, end_month, filename="排班表.xlsx"):
    """把排班结果写成 Excel 文件"""
    title = f"{year}年{start_month}月-{end_month}月值班排班表"  # 标题
    header_rows = [[title, "", "", "", ""]]  # 第一行：标题，后面 4 空
    for i, group in enumerate(groups):
        header_rows.append([f"第{i+1}组：{'、'.join(group)}", "", "", "", ""])
    header_rows.append(["", "", "", "", ""])  # 空行
    header_rows.append(["日期", "星期", "类型", "值班组", "值班人员"])  # 表头

    df_data = pd.DataFrame(schedule)  # 排班数据转成 DataFrame（表格）
    df_data["日期"] = df_data["日期"].apply(lambda x: x.strftime("%Y-%m-%d"))
    # apply 对每行执行；lambda x: ... 匿名函数；strftime 格式化为 "2024-01-06"
    df_data = df_data[["日期", "星期", "类型", "值班组", "值班人员"]]  # 选这 5 列

    df_header = pd.DataFrame(header_rows)  # 表头转成表格
    df_full = pd.concat([df_header, df_data], ignore_index=True)
    # concat 拼接；ignore_index=True 重新编号行号

    with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
        # with 自动关文件；engine 指定用 xlsxwriter 写 xlsx
        df_full.to_excel(writer, sheet_name=f"{year}年排班表", index=False, header=False)
        # 写入；index=False 不写行号；header=False 不把第一行当表头（已包含在数据里）
        ws = writer.sheets[f"{year}年排班表"]  # 拿到工作表对象
        ws.set_column("A:A", 15)  # A 列宽 15
        ws.set_column("B:B", 10)
        ws.set_column("C:C", 15)
        ws.set_column("D:D", 12)
        ws.set_column("E:E", 30)

    print(f"\n排班表已成功导出到：{filename}")  # 打印提示
