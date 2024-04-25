import re

s = '11.3*12.5*5.5'
#s = '11.3/12.5/5.5'

# 使用正则表达式找出所有的数字和非数字字符
numbers = re.findall('\d+', s)  # 这将找出所有的数字
operators = re.findall('\D', s)  # 这将找出所有的非数字字符

print('数字：', numbers)
print('运算符：', operators)

# 使用正则表达式找出所有的数字和非数字字符
numbers = re.findall('(\d+(\.\d+)?)', s)  # 这将找出所有的数字（包括带小数的）
operators = re.findall('[^\d.]+', s)  # 这将找出所有的非数字字符

print('数字：', [num[0] for num in numbers])
print('运算符：', operators)

# 通过将列表转换为集合，再转换回列表，可去除列表中的重复项
operators_unique = list(set(operators))
print('运算符：', operators_unique)

