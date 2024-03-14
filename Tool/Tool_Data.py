class DataType:
    def remove_duplicates(nums):
        # 使用集合的特性,将数组转换为集合,重复元素会被自动去除
        nums_set = set(nums)
        # 将集合转换回列表
        return list(nums_set)