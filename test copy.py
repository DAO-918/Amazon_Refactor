def flatten(data, level=0):
    result = ''
    indent = '    ' * level
    # 判断数据是否是列表
    if isinstance(data, list):
        for i in data:
            # 如果元素还是一个列表，我们再次调用flatten函数，并将缩进级别加1
            if isinstance(i, list):
                result += '\n' + flatten(i, level + 1)
            else:
                # 将元素转化为字符串，并在最后加上逗号
                result += '\n' + indent + '\"' + str(i) + '\",'
    else:
        result += '\n' + indent + '\"' + str(data) + '\",'
    # 返回结果
    return result

data = ['div', 0, 0, 'a-section a-spacing-none a-spacing-top-small s-title-instructions-style', 
        [['h2', 1, 1, 'a-size-mini a-spacing-none a-color-base s-line-clamp-4', [['a', 2, 1, 
        'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal', 
        [['span', 3, 1, 'a-size-base-plus a-color-base a-text-normal', []]]]]]]]

print(flatten(data, 0)) 
