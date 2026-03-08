"""
core.py - 核心排班逻辑

这个文件做什么？
  只负责"算排班"和"导出Excel"，不负责弹窗口、不负责打印提示。
  cli 和 gui 都会调用这里的函数。

谁用这个文件？
  cli.py 和 gui.py 会写 from .core import xxx 来用这里的函数。

流程简要：
  1. 找出要排班的日子（周末、节假日，排除调休）
  2. 把连续的日子分成一段段（比如 5.1-5.5 劳动节是一段）
  3. 给每段分配值班组
  4. 导出 Excel
"""

# ==================== 导入库 ====================
# import = 把别人写好的代码拿进来用
import datetime  # 算日期的
from datetime import timedelta  # 表示"几天"这种时间长度
import pandas as pd  # 生成日期、写 Excel 用
import chinese_calendar  # 判断某天是不是节假日、调休日


def get_all_schedule_dates(year, start_month, end_month):
    """
    找出需要排班的所有日期（周末 + 节假日，排除调休日）

    传入：年份、起始月、结束月
    返回：一个列表，每个元素是 (日期, "周末"或"法定节假日"等)
    """
    # 从哪一天开始：比如 2024年1月1日
    start_date = datetime.date(year, start_month, 1)

    # 到哪一天结束：比如 2024年12月31日
    if end_month == 12:
        end_date = datetime.date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime.date(year, end_month + 1, 1) - timedelta(days=1)

    schedule_dates = []  # 空列表，后面把要排班的日期一个个加进去

    # 从 start_date 到 end_date，一天一天遍历
    for dt in pd.date_range(start=start_date, end=end_date, freq='D'):
        d = dt.date()  # 转成普通的日期格式

        # 是不是周末？Python 里 5=周六 6=周日
        is_weekend = d.weekday() in [5, 6]

        # 是不是法定节假日（春节、国庆等）？
        is_holiday = chinese_calendar.is_holiday(d)

        # 是不是要上班的日子？（调休日也算上班）
        is_workday = chinese_calendar.is_workday(d)

        # 调休日 = 本来是周末 + 但被改成要上班（如国庆前补班的周六）
        # 调休日不排值班！
        is_makeup_workday = is_weekend and is_workday

        if is_makeup_workday:
            continue  # 跳过，不加入

        # 只排：周末 或 法定节假日
        if is_weekend or is_holiday:
            if is_holiday and not is_weekend:
                date_type = "法定节假日"
            elif is_weekend and not is_holiday:
                date_type = "周末"
            else:
                date_type = "周末+节假日"  # 如国庆里的周六
            schedule_dates.append((d, date_type))  # append = 加到列表末尾

    return schedule_dates


def get_holiday_periods(schedule_dates):
    """
    把日期按"连续"分成一段段。
    比如 1.6、1.7 连续 → 一段；5.1-5.5 劳动节 → 一段。
    劳动节、国庆节会强制拆成两段（前期/后期）。

    传入：日期列表
    返回：列表的列表，每小段是一串连续的日期
    """
    if not schedule_dates:
        return []  # 空的话直接返回空列表

    holiday_periods = []  # 存所有段
    current_period = []   # 当前这一段

    for i, (date, date_type) in enumerate(schedule_dates):  # enumerate = 同时拿到序号 i 和内容
        # 劳动节 5.3、国庆 10.4 要强制断开，不让同一组值太多天
        should_split = False
        if date.month == 5 and date.day == 3:
            should_split = True   # 5.1-5.2 一段，5.3-5.5 一段
        elif date.month == 10 and date.day == 4:
            should_split = True   # 10.1-10.3 一段，10.4-10.7 一段

        if should_split and current_period:
            holiday_periods.append(current_period)  # 先存好当前这段
            current_period = [(date, date_type)]   # 开新段
        elif i == 0:
            current_period.append((date, date_type))  # 第一个直接加
        else:
            prev_date = schedule_dates[i - 1][0]  # 上一个日期
            days_diff = (date - prev_date).days   # 隔了几天

            if days_diff == 1:  # 连续（隔1天）
                current_period.append((date, date_type))
            else:
                # 不连续了，存好当前段，开新段
                if current_period:
                    holiday_periods.append(current_period)
                current_period = [(date, date_type)]

    # 别忘了最后一段
    if current_period:
        holiday_periods.append(current_period)

    return holiday_periods


def get_period_identifier(period):
    """
    给这一段假期打个"标签"。
    劳动节、国庆节有"前期""后期"；清明端午等用"连休_年月日"。
    普通周末返回 None，表示可以轮流排，不用固定一组。

    传入：一段日期
    返回："劳动节前期" 或 None 等
    """
    first_date = period[0][0]  # 这段的第一天

    # 这段里有没有法定节假日？
    has_holiday = any(chinese_calendar.is_holiday(date) for date, _ in period)

    period_dates = [date for date, _ in period]  # 把这段的日期都拿出来

    # 劳动节、国庆节各分前后两段
    labor_day_early = [datetime.date(first_date.year, 5, 1), datetime.date(first_date.year, 5, 2)]
    labor_day_late = [datetime.date(first_date.year, 5, 3), datetime.date(first_date.year, 5, 4), datetime.date(first_date.year, 5, 5)]
    national_day_early = [datetime.date(first_date.year, 10, 1), datetime.date(first_date.year, 10, 2), datetime.date(first_date.year, 10, 3)]
    national_day_late = [datetime.date(first_date.year, 10, 4), datetime.date(first_date.year, 10, 5), datetime.date(first_date.year, 10, 6), datetime.date(first_date.year, 10, 7)]

    # 看这段属于哪个，返回对应标签
    if any(date in labor_day_early for date in period_dates):
        return "劳动节前期"
    elif any(date in labor_day_late for date in period_dates):
        return "劳动节后期"
    elif any(date in national_day_early for date in period_dates):
        return "国庆节前期"
    elif any(date in national_day_late for date in period_dates):
        return "国庆节后期"
    elif has_holiday and len(period) > 1:
        return f"连休_{first_date.strftime('%Y%m%d')}"  # 如 连休_20240404
    else:
        return None  # 普通周末


def create_schedule(groups, schedule_dates, start_group_index=0):
    """
    生成排班表（核心函数）

    流程：1. 分时段 2. 特殊段固定一组 3. 普通段轮流 4. 拼成排班记录

    传入：groups=各组人员, schedule_dates=要排的日期, start_group_index=从第几组开始轮
    返回：排班表，每行是 日期、星期、类型、值班组、值班人员
    """
    schedule = []  # 排班结果，最后返回这个

    group_month_count = {}   # 每组每月排了几天（不能超过4天）
    last_schedule_date = {}  # 每组上次值班是哪天（避免连续值）
    current_group_index = start_group_index  # 当前轮到第几组
    period_assigned = {}     # 某段假期已经分给哪组了

    # 先把日期按"连续"分成一段段
    holiday_periods = get_holiday_periods(schedule_dates)

    for period in holiday_periods:
        period_id = get_period_identifier(period)  # 这段的标签，可能是 None（普通周末）

        # 特殊段（劳动节、国庆等）要整段分给同一组
        if period_id and period_id not in period_assigned:
            assigned_group = find_available_group_for_period(
                groups, current_group_index, period,
                group_month_count, last_schedule_date
            )
            period_assigned[period_id] = assigned_group
            current_group_index = (assigned_group + 1) % len(groups)  # % 取余，让组号循环

        # 遍历这段里的每一天，确定谁值班
        for date, date_type in period:
            if period_id and period_id in period_assigned:
                assigned_group = period_assigned[period_id]
            else:
                assigned_group = find_available_group(
                    groups, current_group_index, date,
                    group_month_count, last_schedule_date
                )
                current_group_index = (assigned_group + 1) % len(groups)

            # 记一下：这组这月多值了一天，这组上次值班是这天
            month_key = (assigned_group, date.year, date.month)
            group_month_count[month_key] = group_month_count.get(month_key, 0) + 1  # get(键, 默认值)
            last_schedule_date[assigned_group] = date

            weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            weekday = weekday_names[date.weekday()]  # weekday() 返回 0-6
            members_str = '、'.join(groups[assigned_group])  # 把名单用顿号连起来

            schedule.append({  # 字典：键值对，像 {"日期": xxx, "值班组": "第1组"}
                '日期': date,
                '星期': weekday,
                '类型': date_type,
                '值班组': f"第{assigned_group + 1}组",  # 组号从1开始显示
                '值班人员': members_str
            })

    return schedule


def find_available_group_for_period(groups, start_index, period, group_month_count, last_schedule_date):
    """
    给整段假期找一组来值。要求：这组值完这段后，每月不超过4天，且离上次值班至少隔2天。
    """
    group_count = len(groups)
    first_date = period[0][0]

    for i in range(group_count):
        group_index = (start_index + i) % group_count  # 轮流试每一组
        can_assign = True
        month_days = {}  # 这段假期在每个月占几天（可能跨月）

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

        # 这组上次值班离这段第一天够不够2天？
        if group_index in last_schedule_date:
            last_date = last_schedule_date[group_index]
            days_diff = (first_date - last_date).days
            if days_diff < 2:  # 间隔至少 2 天
                continue

        return group_index

    return start_index  # 实在找不到就用 start_index


def find_available_group(groups, start_index, date, group_month_count, last_schedule_date):
    """
    给单天找一组值（普通周末用）。要求：这组这月没满4天，且离上次值班至少2天。
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
    把排班结果写成 Excel 文件。

    传入：schedule=排班表, groups=组信息, 年份月份, 文件名
    """
    title = f"{year}年{start_month}月-{end_month}月值班排班表"
    header_rows = [[title, "", "", "", ""]]
    for i, group in enumerate(groups):
        header_rows.append([f"第{i+1}组：{'、'.join(group)}", "", "", "", ""])
    header_rows.append(["", "", "", "", ""])
    header_rows.append(["日期", "星期", "类型", "值班组", "值班人员"])

    df_data = pd.DataFrame(schedule)  # DataFrame = 表格
    df_data["日期"] = df_data["日期"].apply(lambda x: x.strftime("%Y-%m-%d"))  # 日期转成 "2024-01-06" 这种
    df_data = df_data[["日期", "星期", "类型", "值班组", "值班人员"]]

    df_header = pd.DataFrame(header_rows)  # 表头
    df_full = pd.concat([df_header, df_data], ignore_index=True)  # 表头+数据接在一起

    with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
        df_full.to_excel(writer, sheet_name=f"{year}年排班表", index=False, header=False)
        ws = writer.sheets[f"{year}年排班表"]
        ws.set_column("A:A", 15)
        ws.set_column("B:B", 10)
        ws.set_column("C:C", 15)
        ws.set_column("D:D", 12)
        ws.set_column("E:E", 30)

    print(f"\n排班表已成功导出到：{filename}")
