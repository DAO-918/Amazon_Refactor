import re

s = '11.3*12.5*5.5'
#s = '11.3/12.5/5.5'
#s = '11.3/12.5'
s = '23*30*8'


# 使用正则表达式找出所有的数字和非数字字符
numbers = re.findall('\d+', s)  # 这将找出所有的数字
operators = re.findall('\D', s)  # 这将找出所有的非数字字符
print('数字：', numbers)
print('运算符：', operators)

# 使用正则表达式找出所有的数字和非数字字符
# 首先查找一个或多个连续的数字（\d+），然后查找小数点后的数字（.5）。但这样的话，会将小数当做两个独立的部分来处理
numbers = re.findall('(\d+(\.\d+)?)', s)
# 在使用正则表达式匹配浮点数或整数时，括号会创建捕获组/子组。在你的情况下，re.findall返回了每个匹配的元组而不是字符串。
# 因此，当你调用sort方法时，你实际上是在元组上调用它的，而不是单独的数字字符串。这就是为什么代码没有正确排序数字的原因。
operators = re.findall('[^\d.]+', s)  # 这将找出所有的非数字字符
print('数字：', [num for num in numbers])
print('运算符：', operators)

# 使用正则表达式找出所有的数字和非数字字符
# 先查找一个或多个连续的数字（\d+），然后查找可能存在的小数点（.?），最后查找小数点后可能存在的数字（\d*）
numbers = re.findall(r'\d+\.?\d*', s)  # 这将找出所有的数字（包括带小数的）
numbers = [float(match) for match in numbers]
numbers.sort(reverse=True)
operators = re.findall('[^\d.]+', s)  # 这将找出所有的非数字字符
print('数字：', [num for num in numbers])
print('运算符：', operators)

# 通过将列表转换为集合，再转换回列表，可去除列表中的重复项
operators_unique = list(set(operators))
print('运算符：', operators_unique)

