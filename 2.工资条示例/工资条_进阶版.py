"""
工资条示例 - 进阶版

在已经理解“基础版”的前提下，进一步学习：
    1. groupby 分组统计
    2. 条件筛选 + 排序
    3. 导出 Excel / CSV 文件

使用建议：
    - 如果你对基础版已经比较熟悉，再来运行这个文件。
    - 先整体运行一遍，再把每个函数拆开，单独练习。
"""

import pandas as pd


def build_salary_dataframe() -> pd.DataFrame:
    """
    和完整版示例类似，这里准备一张稍微完整一点的工资表。
    为了练 groupby，我们额外加上“部门”列。
    """
    data = {
        "姓名": ["安欣", "高启强", "李响", "孟钰", "高启盛", "小五", "程程"],
        "部门": ["刑警队", "建工集团", "刑警队", "央视记者站", "建工集团", "建工集团", "刑警队"],
        "基础工资": [12000, 30000, 13000, 15000, 22000, 8000, 9000],
        "绩效奖金": [5000, 8000, 4000, 7000, 6000, 2000, 2500],
        "扣款": [800, 3000, 500, 600, 2000, 300, 400],
    }

    df = pd.DataFrame(data)

    # 计算应发工资、实发工资（和完整版示例相同）
    df["应发工资"] = df["基础工资"] + df["绩效奖金"]
    df["实发工资"] = df["应发工资"] - df["扣款"]

    return df


def analyze_by_department(df: pd.DataFrame) -> pd.DataFrame:
    """
    按部门做统计：人数、平均实发工资、实发工资总额。

    这是 groupby + agg 的经典用法，非常值得反复练习。
    """
    grouped = (
        df.groupby("部门", as_index=False)
        .agg(
            人数=("姓名", "count"),
            平均实发工资=("实发工资", "mean"),
            实发工资总额=("实发工资", "sum"),
        )
        .sort_values("实发工资总额", ascending=False)
    )
    return grouped


def filter_high_salary(df: pd.DataFrame, threshold: int = 20000) -> pd.DataFrame:
    """
    条件筛选 + 排序练习：
        - 条件：实发工资 >= threshold
        - 排序：按实发工资从高到低
    """
    result = df[df["实发工资"] >= threshold].sort_values("实发工资", ascending=False)
    return result


def main() -> None:
    """进阶练习的完整流程演示。"""
    # 1. 构造工资表
    df_salary = build_salary_dataframe()
    print("===== 进阶版：原始工资表 =====")
    print(df_salary)
    print()

    # 2. 部门分组统计
    dept_summary = analyze_by_department(df_salary)
    print("===== 按部门统计（人数、平均实发、实发总额）=====")
    print(dept_summary)
    print()

    # 3. 高收入人员筛选
    high_salary_df = filter_high_salary(df_salary, threshold=20000)
    print("===== 实发工资 ≥ 20000 的员工 =====")
    print(high_salary_df[["姓名", "部门", "实发工资"]])
    print()

    # 4. 导出文件（和完整版类似）
    df_salary.to_excel("工资明细_狂飙人物_进阶版.xlsx", index=False)
    dept_summary.to_csv("部门工资统计_狂飙人物_进阶版.csv", index=False, encoding="utf-8-sig")
    print("已生成：'工资明细_狂飙人物_进阶版.xlsx' 和 '部门工资统计_狂飙人物_进阶版.csv'")


if __name__ == "__main__":
    main()

