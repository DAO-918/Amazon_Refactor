import os

def get_files_by_extension(folder_path,file_extension):
    # 获取目标文件夹下所有文件
    file_list = os.listdir(folder_path)

    files = []

    # 遍历文件,找出后缀为 .xlsx 的文件
    for file in file_list:
        # 获取文件的后缀名
        file_suffix = os.path.splitext(file)[1]
        
        # 如果是 .xlsx 文件,就获取其完整路径并添加到 xlsx_files列表
        if file_suffix == file_extension:
            file_path = os.path.join(folder_path, file)
            files.append(file_path)
    return files

def get_files_by_name(folder_path,file_name):
    # sourcery skip: list-comprehension
    try:
        file_list = os.listdir(folder_path)
        files = []
        for file in file_list:
            if file_name in file:
                file_path = os.path.join(folder_path, file)
                files.append(file_path)
        '''
        for filename in file_list:
            if '1500' in filename:
                files.append(filename)
        '''
        return files
    except Exception:
        return None
            
# 测试代码
if __name__ == '__main__':
    # \\AutoRPA\\产品信息\\新品竞品'是相同的
    # Python 中,字符串可以以反斜杠\ 或正斜杠/作为路径分隔符，为了风格统一，不建议同时使用两者
    # Windows 下使用反斜杠\作为路径分隔符,Linux/macOS 下使用正斜杠/
    folder_path='D:\\AutoRPA\\产品信息\\新品竞品\\'
    file_extension='.xlsx'
    files = get_files_by_extension(folder_path, file_extension)
    print(files)