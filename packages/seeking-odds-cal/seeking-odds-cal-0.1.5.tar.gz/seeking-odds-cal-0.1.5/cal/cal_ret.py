import math
import pandas as pd

#区间收益率
def cal_range_return(first_value, last_value):
    return (last_value - first_value) / first_value

# 年化收益率
def cal_year_yield(range_return, n):
    return pow(float(1 + range_return), 1/n) - 1

# 月和年标准差
def cal_std(return_list):
    s1 = pd.Series(return_list)
    STD_Monthly = s1.std(ddof=1)
    STD_Yearly = STD_Monthly * math.sqrt(12)
    return STD_Monthly, STD_Yearly