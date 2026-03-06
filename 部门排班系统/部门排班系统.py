"""
部门排班系统
功能：自动生成周末和法定节假日的排班表
特点：
  - 自动识别法定节假日和调休日
  - 调休日（周末但需要上班）不安排值班
  - 劳动节、国庆节特殊分段安排
  - 连休假期固定同一组值班
  - 避免连续值班，保证休息时间
"""

# 导入需要的库
import datetime
from datetime import timedelta
import pandas as pd
import chinese_calendar


def get_user_input():
    """
    获取用户输入的组员信息和时间范围
    
    功能说明：
        1. 获取组数和各组成员信息
        2. 获取排班的年份和月份范围
        3. 询问是否接续上一年的排班顺序
        4. 如果接续，计算起始组索引
    
    返回值：
        groups: 列表，包含所有组的成员信息，例如：[['张三', '李四'], ['王五', '赵六']]
        year: 整数，排班年份
        start_month: 整数，起始月份（1-12）
        end_month: 整数，结束月份（1-12）
        start_group_index: 整数，起始组的索引（0表示第1组，1表示第2组...）
    """
    # 打印欢迎信息，使用"="号创建分隔线，让界面更美观
    print("=" * 50)
    print("欢迎使用部门排班系统")
    print("=" * 50)
    
    # 获取组数，int()函数将用户输入的字符串转换为整数
    group_count = int(input("\n请输入组数："))
    
    # 创建一个空列表来存储所有组的信息
    # 列表是Python中用于存储多个元素的数据结构
    groups = []
    
    # 使用for循环获取每个组的成员
    # range(group_count)生成0到group_count-1的数字序列
    for i in range(group_count):
        # 打印当前是第几组（i从0开始，所以显示时要+1）
        print(f"\n--- 第{i+1}组 ---")
        
        # 输入组员名字，用逗号分隔，例如：张三,李四,王五
        members = input(f"请输入第{i+1}组的组员名字（用逗号分隔）：")
        
        # 处理输入的字符串：
        # 1. members.split(',') 将字符串按逗号分割成列表
        # 2. name.strip() 去除每个名字前后的空格
        # 3. [... for name in ...] 是列表推导式，对每个元素执行相同操作
        # 例如："张三, 李四 ,王五" -> ['张三', '李四', '王五']
        member_list = [name.strip() for name in members.split(',')]
        
        # 将这个组的成员列表添加到groups列表中
        # append()方法用于在列表末尾添加元素
        groups.append(member_list)
    
    # 获取排班的起止时间
    print("\n--- 排班时间范围 ---")
    # 获取年份，例如：2024
    year = int(input("请输入年份（例如：2024）："))
    # 获取起始月份，范围1-12
    start_month = int(input("请输入起始月份（1-12）："))
    # 获取结束月份，范围1-12
    end_month = int(input("请输入结束月份（1-12）："))
    
    # 询问是否接续上一年的排班
    # 接续功能可以让新一年的排班从上一年结束的组继续，保证公平性
    print("\n--- 排班顺序设置 ---")
    # strip()去除首尾空格，lower()转换为小写，方便比较
    continue_last_year = input("是否接续上一年的排班顺序？(y/n，默认n)：").strip().lower()
    
    # 初始化起始组索引为0（表示第1组）
    # 索引是从0开始的，所以第1组的索引是0，第2组的索引是1，以此类推
    start_group_index = 0
    
    # 如果用户选择接续上一年（输入'y'）
    if continue_last_year == 'y':
        # 询问上一年最后值班的是哪个组
        # 例如：如果上一年最后是第2组值班，输入2
        last_group = int(input(f"请输入上一年最后值班的组号（1-{group_count}）："))
        
        # 验证输入的组号是否在有效范围内（1到group_count）
        if 1 <= last_group <= group_count:
            # 计算起始组索引：
            # last_group % group_count 实现循环轮换
            # 例如：3个组，上一年最后是第2组，则 2 % 3 = 2（第3组）
            #      3个组，上一年最后是第3组，则 3 % 3 = 0（第1组）
            start_group_index = last_group % group_count
            # 显示提示信息（索引+1转换为组号）
            print(f"提示：本次排班将从第{start_group_index + 1}组开始")
        else:
            # 如果输入的组号无效，显示警告并从第1组开始
            print(f"警告：输入的组号无效，将从第1组开始")
            start_group_index = 0
    else:
        # 如果不接续，从第1组开始
        print("提示：本次排班将从第1组开始")
    
    # 返回所有输入的信息，包括起始组索引
    # Python支持返回多个值，用逗号分隔
    return groups, year, start_month, end_month, start_group_index


def get_all_schedule_dates(year, start_month, end_month):
    """
    获取指定时间范围内所有需要排班的日期（周末和法定节假日）
    使用 pandas 的 date_range 生成日期序列，代码更简洁。
    """
    start_date = datetime.date(year, start_month, 1)
    end_date = datetime.date(year + 1, 1, 1) - timedelta(days=1) if end_month == 12 else datetime.date(year, end_month + 1, 1) - timedelta(days=1)

    schedule_dates = []
    # pd.date_range 生成每天一个日期的序列，比 while 循环更简洁
    for dt in pd.date_range(start=start_date, end=end_date, freq='D'):
        d = dt.date()
        is_weekend = d.weekday() in [5, 6]
        is_holiday = chinese_calendar.is_holiday(d)
        is_workday = chinese_calendar.is_workday(d)
        is_makeup_workday = is_weekend and is_workday

        if is_makeup_workday:
            continue

        if is_weekend or is_holiday:
            if is_holiday and not is_weekend:
                date_type = "法定节假日"
            elif is_weekend and not is_holiday:
                date_type = "周末"
            else:
                date_type = "周末+节假日"
            schedule_dates.append((d, date_type))

    return schedule_dates


def get_holiday_periods(schedule_dates):
    """
    识别所有连续的假期时段（包括周末+节假日连休）
    
    功能说明：
        1. 将连续的日期（间隔1天）归为一个时段
        2. 特别处理劳动节和国庆节，强制分成两段
           - 劳动节：5月1-2日一段，5月3-5日另一段
           - 国庆节：10月1-3日一段，10月4-7日另一段
        3. 返回所有识别出的时段列表
    
    参数：
        schedule_dates: 列表，需要排班的日期列表，每个元素是(日期, 类型)元组
    
    返回值：
        列表，每个元素是一个时段（时段也是列表，包含多个日期元组）
        例如：[[(date1, type1), (date2, type2)], [(date3, type3)]]
    """
    # 如果没有日期，返回空列表
    # not运算符：如果列表为空，not []返回True
    if not schedule_dates:
        return []
    
    # 存储所有假期时段的列表
    # 每个时段本身也是一个列表，包含连续的日期
    holiday_periods = []
    
    # 当前正在处理的时段
    # 用于临时存储连续的日期，当遇到不连续的日期时保存到holiday_periods
    current_period = []
    
    # 遍历所有日期
    # enumerate()函数返回索引和元素，i是索引，(date, date_type)是元素
    for i, (date, date_type) in enumerate(schedule_dates):
        # 检查是否需要强制分段（劳动节5月3日、国庆节10月4日）
        # 这是为了满足特殊排班规则：劳动节和国庆节要分成两段
        should_split = False
        
        if date.month == 5 and date.day == 3:
            # 劳动节：5月3日开始新时段
            # 将5月1-2日作为一段，5月3-5日作为另一段
            should_split = True
        elif date.month == 10 and date.day == 4:
            # 国庆节：10月4日开始新时段
            # 将10月1-3日作为一段，10月4-7日作为另一段
            should_split = True
        
        # 如果需要强制分段，且当前时段不为空
        if should_split and current_period:
            # 保存当前时段到结果列表
            holiday_periods.append(current_period)
            # 开始新时段，将当前日期作为新时段的第一天
            current_period = [(date, date_type)]
        # 如果是第一个日期（索引为0），直接加入当前时段
        elif i == 0:
            current_period.append((date, date_type))
        else:
            # 获取上一个日期（索引i-1）
            # schedule_dates[i-1][0]表示上一个元组的第一个元素（日期对象）
            prev_date = schedule_dates[i-1][0]
            
            # 计算与上一个日期的间隔天数
            # 日期对象相减得到timedelta对象，.days获取天数
            # 例如：2024-01-02 - 2024-01-01 = 1天
            days_diff = (date - prev_date).days
            
            # 如果是连续的日期（间隔1天），加入当前时段
            if days_diff == 1:
                current_period.append((date, date_type))
            else:
                # 如果不连续（间隔超过1天），说明遇到了新的时段
                # 保存当前时段（如果不为空）
                if current_period:
                    holiday_periods.append(current_period)
                # 开始新时段，将当前日期作为新时段的第一天
                current_period = [(date, date_type)]
    
    # 循环结束后，添加最后一个时段
    # 因为循环中只在遇到不连续日期时保存时段，最后一个时段需要单独保存
    if current_period:
        holiday_periods.append(current_period)
    
    # 返回所有识别出的假期时段
    return holiday_periods


def get_period_identifier(period):
    """
    为假期时段生成唯一标识符
    
    功能说明：
        1. 判断时段是否为特殊节假日（劳动节、国庆节）
        2. 判断时段是否为其他连休假期（清明、端午、中秋等）
        3. 返回时段的唯一标识符，用于确保同一时段由同一组值班
    
    参数：
        period: 列表，假期时段，包含多个(日期, 类型)元组
    
    返回值：
        字符串，时段标识符，如"劳动节前期"、"连休_20240404"等
        如果是普通周末，返回None（不需要固定组）
    """
    # 获取时段的第一天和最后一天
    # period[0][0]表示第一个元组的第一个元素（日期对象）
    # period[-1][0]表示最后一个元组的第一个元素（日期对象）
    first_date = period[0][0]
    last_date = period[-1][0]
    
    # 检查时段是否包含法定节假日
    # any()函数：只要有一个元素为True，就返回True
    # for date, _ in period：遍历时段中的每个元组，_表示忽略第二个元素（类型）
    # 生成器表达式：(... for ... in ...)，比列表推导式更节省内存
    has_holiday = any(chinese_calendar.is_holiday(date) for date, _ in period)
    
    # 提取时段内所有日期对象，用于后续判断
    # 列表推导式：[date for date, _ in period]
    period_dates = [date for date, _ in period]
    
    # 定义特殊节假日的日期范围
    # 劳动节前期：5月1-2日
    # datetime.date(年, 月, 日)创建日期对象
    labor_day_early = [datetime.date(first_date.year, 5, 1), datetime.date(first_date.year, 5, 2)]
    
    # 劳动节后期：5月3-5日
    labor_day_late = [datetime.date(first_date.year, 5, 3), datetime.date(first_date.year, 5, 4), datetime.date(first_date.year, 5, 5)]
    
    # 国庆节前期：10月1-3日
    national_day_early = [datetime.date(first_date.year, 10, 1), datetime.date(first_date.year, 10, 2), datetime.date(first_date.year, 10, 3)]
    
    # 国庆节后期：10月4-7日
    national_day_late = [datetime.date(first_date.year, 10, 4), datetime.date(first_date.year, 10, 5), datetime.date(first_date.year, 10, 6), datetime.date(first_date.year, 10, 7)]
    
    # 检查时段是否与特殊节假日有交集
    # any(date in labor_day_early for date in period_dates)：
    # 检查period_dates中是否有任何日期在labor_day_early中
    if any(date in labor_day_early for date in period_dates):
        # 时段包含5月1-2日，标识为劳动节前期
        return "劳动节前期"
    elif any(date in labor_day_late for date in period_dates):
        # 时段包含5月3-5日，标识为劳动节后期
        return "劳动节后期"
    elif any(date in national_day_early for date in period_dates):
        # 时段包含10月1-3日，标识为国庆节前期
        return "国庆节前期"
    elif any(date in national_day_late for date in period_dates):
        # 时段包含10月4-7日，标识为国庆节后期
        return "国庆节后期"
    # 如果是包含法定节假日的连休（如清明、端午、中秋等）
    # 条件：包含节假日 且 时段长度大于1天
    elif has_holiday and len(period) > 1:
        # 生成唯一标识符，格式：连休_年月日
        # strftime('%Y%m%d')将日期格式化为字符串，如20240404
        # f-string：f"..."可以在字符串中嵌入变量
        return f"连休_{first_date.strftime('%Y%m%d')}"
    # 普通周末（不包含节假日，或只有1天）
    else:
        # 返回None，表示不需要固定组，可以正常轮换
        return None


def create_schedule(groups, schedule_dates, start_group_index=0):
    """
    创建排班表（核心函数）
    
    功能说明：
        1. 识别所有连续假期时段
        2. 为特殊时段（劳动节、国庆节、连休）分配固定组
        3. 为普通周末轮流分配组
        4. 确保每组每月值班不超过4天
        5. 避免连续值班
    
    参数：
        groups: 列表，所有组的成员信息
        schedule_dates: 列表，需要排班的日期列表
        start_group_index: 整数，起始组索引（默认0），用于接续上一年的排班
    
    返回值：
        列表，每个元素是一个字典，包含：日期、星期、类型、值班组、值班人员
    """
    # 存储排班结果的列表
    # 每个元素是一个字典，包含一天的排班信息
    schedule = []
    
    # 记录每个组每月的值班天数
    # 字典格式：{(组索引, 年, 月): 天数}
    # 例如：{(0, 2024, 1): 3} 表示第1组在2024年1月值班3天
    group_month_count = {}
    
    # 记录每个组最后一次值班的日期
    # 字典格式：{组索引: 日期对象}
    # 用于避免连续值班（两次值班之间至少间隔1天）
    last_schedule_date = {}
    
    # 当前轮到哪个组值班（轮流制）
    # 从指定的起始组开始（用于接续上一年的排班）
    current_group_index = start_group_index
    
    # 记录假期时段已分配的组
    # 字典格式：{时段标识: 组索引}
    # 例如：{"劳动节前期": 0} 表示劳动节前期由第1组值班
    period_assigned = {}
    
    # 第一步：识别所有连续假期时段
    # 调用get_holiday_periods函数，将连续的日期归为一个时段
    holiday_periods = get_holiday_periods(schedule_dates)
    
    # 第二步：为每个时段分配值班组
    # 遍历所有识别出的假期时段
    for period in holiday_periods:
        # 获取时段标识符（如"劳动节前期"、"连休_20240404"等）
        period_id = get_period_identifier(period)
        
        # 如果这个时段需要固定一个组（特殊节假日或连休）
        # period_id不为None表示需要固定组
        if period_id:
            # 检查这个时段是否已经分配过组
            # 避免重复分配（虽然正常情况下不会重复）
            if period_id not in period_assigned:
                # 选择一个合适的组
                # 计算这个时段需要的天数
                period_days = len(period)
                # 获取时段的第一天
                first_date = period[0][0]
                
                # 找到一个可用的组（考虑月度限制和避免连续值班）
                # 调用find_available_group_for_period函数
                assigned_group = find_available_group_for_period(
                    groups, current_group_index, period,
                    group_month_count, last_schedule_date
                )
                
                # 记录这个时段分配的组
                # 后续这个时段的所有日期都使用这个组
                period_assigned[period_id] = assigned_group
                
                # 更新当前组索引，下一个时段从下一组开始
                # %运算符实现循环：(2+1)%3=0，即第3组的下一组是第1组
                current_group_index = (assigned_group + 1) % len(groups)
        
        # 第三步：为时段内的每一天安排值班
        # 遍历时段内的每个日期
        for date, date_type in period:
            # 如果时段有固定组（特殊节假日或连休），使用固定组
            if period_id and period_id in period_assigned:
                assigned_group = period_assigned[period_id]
            else:
                # 普通周末，按轮流顺序分配
                # 调用find_available_group函数找到可用的组
                assigned_group = find_available_group(
                    groups, current_group_index, date, 
                    group_month_count, last_schedule_date
                )
                # 更新当前组索引，下一天从下一组开始
                current_group_index = (assigned_group + 1) % len(groups)
            
            # 更新该组本月的值班天数
            # 月度键：(组索引, 年, 月)
            month_key = (assigned_group, date.year, date.month)
            # get(key, default)：如果key不存在，返回default值（0）
            # 然后加1，表示本月值班天数+1
            group_month_count[month_key] = group_month_count.get(month_key, 0) + 1
            
            # 更新该组最后一次值班日期
            # 用于下次判断是否连续值班
            last_schedule_date[assigned_group] = date
            
            # 获取星期几的中文名称
            # 定义一个列表，索引对应weekday()的返回值
            weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            # date.weekday()返回0-6，用作列表索引获取中文名称
            weekday = weekday_names[date.weekday()]
            
            # 获取值班组的成员名单
            # groups[assigned_group]获取该组的成员列表
            group_members = groups[assigned_group]
            # join()方法用顿号连接所有成员名字
            # 例如：['张三', '李四', '王五'] -> '张三、李四、王五'
            members_str = '、'.join(group_members)
            
            # 将排班信息添加到结果列表
            # 创建一个字典存储一天的排班信息
            schedule.append({
                '日期': date,  # 日期对象
                '星期': weekday,  # 星期几的中文名称
                '类型': date_type,  # 日期类型（周末、法定节假日等）
                '值班组': f"第{assigned_group + 1}组",  # 值班组名称（索引+1转为组号）
                '值班人员': members_str  # 值班人员名单
            })
    
    # 返回完整的排班表
    return schedule


def find_available_group_for_period(groups, start_index, period, group_month_count, last_schedule_date):
    """
    为整个假期时段找到一个可用的组
    
    功能说明：
        1. 从起始索引开始，轮流尝试每个组
        2. 检查该组是否能承担整个时段的值班（考虑跨月情况）
        3. 确保不超过每月4天的限制
        4. 确保与上次值班间隔至少2天
    
    参数：
        groups: 列表，所有组的列表
        start_index: 整数，开始查找的组索引
        period: 列表，假期时段（包含多个日期元组）
        group_month_count: 字典，各组每月值班天数统计
        last_schedule_date: 字典，各组最后值班日期
    
    返回值：
        整数，可用的组索引
    """
    # 获取组的总数
    # len()函数返回列表的长度
    group_count = len(groups)
    
    # 获取时段的第一天
    # period[0][0]表示第一个元组的第一个元素（日期对象）
    first_date = period[0][0]
    
    # 从start_index开始，尝试每一个组
    # range(group_count)生成0到group_count-1的序列
    for i in range(group_count):
        # 计算当前检查的组索引（轮流）
        # %运算符实现循环轮换
        group_index = (start_index + i) % group_count
        
        # 检查该组是否能承担整个时段的值班
        # 初始假设可以分配，如果发现问题则设为False
        can_assign = True
        
        # 统计时段内每个月需要的天数
        # 因为时段可能跨月，需要分别统计每个月的天数
        # 字典格式：{(年, 月): 天数}
        month_days = {}
        
        # 遍历时段内的每个日期
        for date, _ in period:
            # 月度键：(年, 月)
            month_key = (date.year, date.month)
            # 统计该月的天数，get(key, 0)如果key不存在返回0
            month_days[month_key] = month_days.get(month_key, 0) + 1
        
        # 检查每个月的值班天数是否会超限
        # items()方法返回字典的键值对
        for month_key, days_needed in month_days.items():
            # 解包月度键，获取年和月
            year, month = month_key
            # 获取该组在该月已有的值班天数
            current_count = group_month_count.get((group_index, year, month), 0)
            
            # 如果加上这个时段的天数会超过4天，不能分配
            # 这是为了确保每组每月值班不超过4天
            if current_count + days_needed > 4:
                can_assign = False
                # break语句跳出循环，不再检查其他月份
                break
        
        # 如果月度天数检查不通过，跳过这个组
        # not运算符：如果can_assign为False，not can_assign为True
        if not can_assign:
            # continue语句跳过本次循环，继续下一个组
            continue
        
        # 检查是否会造成连续值班
        # in运算符：检查key是否在字典中
        if group_index in last_schedule_date:
            # 获取该组最后一次值班的日期
            last_date = last_schedule_date[group_index]
            
            # 计算与上次值班的天数差
            # 日期相减得到timedelta对象，.days获取天数
            days_diff = (first_date - last_date).days
            
            # 如果间隔小于2天（即连续或隔一天），跳过这个组
            # 这是为了避免连续值班，保证休息时间
            if days_diff < 2:
                continue
        
        # 找到合适的组，返回其索引
        # 这个组满足所有条件：月度天数未超限、不会连续值班
        return group_index
    
    # 如果所有组都不满足条件，返回起始索引（兜底方案）
    # 这种情况很少发生，通常是因为约束条件太严格
    return start_index


def find_available_group(groups, start_index, date, group_month_count, last_schedule_date):
    """
    找到一个可用的组进行排班（单天）
    
    功能说明：
        1. 从起始索引开始，轮流尝试每个组
        2. 检查该组本月值班是否已达到4天上限
        3. 检查是否会造成连续值班（间隔小于2天）
        4. 返回第一个满足条件的组
    
    参数：
        groups: 列表，所有组的列表
        start_index: 整数，开始查找的组索引
        date: 日期对象，当前要排班的日期
        group_month_count: 字典，各组每月值班天数统计
        last_schedule_date: 字典，各组最后值班日期
    
    返回值：
        整数，可用的组索引
    """
    # 获取组的总数
    # len()函数返回列表的长度
    group_count = len(groups)
    
    # 从start_index开始，尝试每一个组
    # range(group_count)生成0到group_count-1的序列
    for i in range(group_count):
        # 计算当前检查的组索引（轮流）
        # %运算符实现循环：(2+1)%3=0，即第3组的下一组是第1组
        group_index = (start_index + i) % group_count
        
        # 检查该组本月值班天数
        # 月度键：(组索引, 年, 月)
        month_key = (group_index, date.year, date.month)
        # get(key, 0)：如果key不存在，返回0
        current_count = group_month_count.get(month_key, 0)
        
        # 如果本月值班已达到4天，跳过这个组
        # 这是为了确保每组每月值班不超过4天
        if current_count >= 4:
            # continue语句跳过本次循环，继续下一次循环
            continue
        
        # 检查是否会造成连续值班
        # in运算符：检查key是否在字典中
        if group_index in last_schedule_date:
            # 获取该组最后一次值班的日期
            last_date = last_schedule_date[group_index]
            
            # 计算与上次值班的天数差
            # 日期相减得到timedelta对象，.days获取天数
            days_diff = (date - last_date).days
            
            # 如果间隔小于2天（即连续或隔一天），跳过这个组
            # 这是为了避免连续值班，保证休息时间
            if days_diff < 2:
                continue
        
        # 找到合适的组，返回其索引
        # 这个组满足所有条件：月度天数未超限、不会连续值班
        return group_index
    
    # 如果所有组都不满足条件，返回起始索引（兜底方案）
    # 这种情况很少发生，通常是因为约束条件太严格
    return start_index


def export_to_excel(schedule, groups, year, start_month, end_month, filename="排班表.xlsx"):
    """
    纯 pandas 导出到 Excel，无需 openpyxl。
    用 pandas + xlsxwriter 引擎完成全部写入。
    """
    title = f"{year}年{start_month}月-{end_month}月值班排班表"
    header_rows = [[title, "", "", "", ""]]
    for i, group in enumerate(groups):
        header_rows.append([f"第{i+1}组：{'、'.join(group)}", "", "", "", ""])
    header_rows.append(["", "", "", "", ""])
    header_rows.append(["日期", "星期", "类型", "值班组", "值班人员"])

    df_data = pd.DataFrame(schedule)
    df_data["日期"] = df_data["日期"].apply(lambda x: x.strftime("%Y-%m-%d"))
    df_data = df_data[["日期", "星期", "类型", "值班组", "值班人员"]]

    df_header = pd.DataFrame(header_rows)
    df_full = pd.concat([df_header, df_data], ignore_index=True)

    with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
        df_full.to_excel(writer, sheet_name=f"{year}年排班表", index=False, header=False)
        ws = writer.sheets[f"{year}年排班表"]
        ws.set_column("A:A", 15)
        ws.set_column("B:B", 10)
        ws.set_column("C:C", 15)
        ws.set_column("D:D", 12)
        ws.set_column("E:E", 30)

    print(f"\n排班表已成功导出到：{filename}")


def main():
    """
    主函数：程序的入口
    
    功能说明：
        1. 获取用户输入（组员信息、时间范围、是否接续）
        2. 分析日期（识别周末和节假日，排除调休日）
        3. 生成排班表（分配值班组）
        4. 导出Excel文件
        5. 显示统计信息
        6. 处理异常错误
    
    参数：
        无
    
    返回值：
        无
    """
    # try-except语句用于捕获和处理异常
    # 如果try块中的代码出错，会跳转到except块
    try:
        # 步骤1：获取用户输入（包括起始组索引）
        # 调用get_user_input函数，返回5个值
        groups, year, start_month, end_month, start_group_index = get_user_input()
        
        # 步骤2：获取所有需要排班的日期
        # 显示进度信息，让用户知道程序在运行
        print("\n正在分析日期...")
        # 调用get_all_schedule_dates函数，获取需要排班的日期列表
        schedule_dates = get_all_schedule_dates(year, start_month, end_month)
        # f-string：在字符串中嵌入变量，len()获取列表长度
        print(f"共找到 {len(schedule_dates)} 个需要排班的日期")
        
        # 步骤3：创建排班表（传入起始组索引）
        print("\n正在生成排班表...")
        # 调用create_schedule函数，生成排班表
        # 传入起始组索引，用于接续上一年的排班
        schedule = create_schedule(groups, schedule_dates, start_group_index)
        
        # 步骤4：导出到Excel
        print("\n正在导出Excel文件...")
        # 生成文件名，格式：排班表_2024年1-12月.xlsx
        # f-string：在字符串中嵌入变量
        filename = f"排班表_{year}年{start_month}-{end_month}月.xlsx"
        # 调用export_to_excel函数，将排班表导出为Excel文件
        export_to_excel(schedule, groups, year, start_month, end_month, filename)
        
        # 步骤5：显示统计信息
        # 打印分隔线和标题
        print("\n" + "=" * 50)
        print("排班统计信息")
        print("=" * 50)
        
        # 用 pandas 统计每组值班天数：转为 DataFrame 后按 值班组 计数
        df_schedule = pd.DataFrame(schedule)
        for i in range(len(groups)):
            total_days = (df_schedule['值班组'] == f"第{i+1}组").sum()
            print(f"第{i+1}组：共值班 {total_days} 天")
        
        # 显示最后值班的组（用于下次接续）
        # 如果排班表不为空（有排班数据）
        if schedule:
            # 获取排班表的最后一项
            # schedule[-1]表示列表的最后一个元素
            last_schedule_item = schedule[-1]
            # 获取最后值班的组
            last_group = last_schedule_item['值班组']
            # 获取最后值班的日期，并格式化为字符串
            # strftime()方法将日期对象格式化为指定格式的字符串
            last_date = last_schedule_item['日期'].strftime('%Y年%m月%d日')
            # 显示最后值班信息
            print(f"\n最后值班：{last_group}（{last_date}）")
            print("提示：下次排班时可选择接续此次排班顺序")
        
        # 显示完成信息
        print("\n排班完成！")
        
    except NotImplementedError as e:
        # 节假日库不支持该年份（如 2027 年及以后）
        print(f"\n程序运行出错：{e}")
        print("提示：法定节假日数据随 chinesecalendar 库更新，支持 2004-2026 年。")
        print("      每年 11 月国务院发布次年安排后，执行 pip install -U chinesecalendar 可获取最新数据。")
    except Exception as e:
        print(f"\n程序运行出错：{e}")
        print("请检查输入是否正确，或联系管理员。")


# 程序入口：当直接运行此文件时执行main函数
# __name__是Python的特殊变量
# 当直接运行此文件时，__name__的值为"__main__"
# 当此文件被其他文件导入时，__name__的值为文件名
# 这个判断确保只有直接运行此文件时才执行main函数
if __name__ == "__main__":
    main()  # 调用主函数，开始执行程序
