from bs4 import BeautifulSoup
import yaml

def get_full_xpath(soup, target_element):
    '''xpath = ''
    for parent in target_element.parents:
        # get index of tag among its siblings
        index = 1 + sum(1 for previous_sibling in parent.find_previous_siblings(parent.name))
        xpath = '/' + parent.name + '[' + str(index) + ']' + xpath
    # add the tag itself
    xpath = '/' + target_element.name + '[1]' + xpath
    return xpath'''
    # 解析HTML
    soup = BeautifulSoup(soup, 'html.parser')
    # 使用BeautifulSoup解析target标签和它的属性
    target_soup = BeautifulSoup(target_element, 'html.parser')
    target_tag = target_soup.contents[0].name
    target_attrs = target_soup.contents[0].attrs
    # 找到目标标签
    target_element = soup.find(target_tag, attrs=target_attrs)
    # 初始化一个列表来存储路径
    path = []
    # 开始循环，找到父标签，直到找不到为止
    while target_element is not None:
        # 获取当前元素在其同级元素中的位置
        sibling_count = len(list(target_element.find_previous_siblings(target_element.name)))
        # 将当前标签的名称添加到路径中
        path.append(f"{target_element.name}[{sibling_count+1}]")        # 找到当前标签的父标签
        target_element = target_element.find_parent()
    # 翻转路径列表，并用'/'来连接它们，形成完整的xpath
    full_path = '/'.join(reversed(path))
    # 返回完整的xpath
    return full_path

def update_yaml_file(config_name):
    config_file = f'yaml/features_result_{config_name}.yml'
    with open(config_file) as f:
        config = yaml.safe_load(f)
        
    for section in config:
        # 匹配特征值
        print (section)
        outerHTML = config[section]['Div_feature']
        outerHTML = config[section]['Div_outerHTML']
        exists = True
        key_flag = 1
        while key_flag > 0:
            # section中有几个需要获取的data，后缀就到几
            key_name = f'data_{key_flag}'
            # 匹配失败，即section的需要获取值已经到尾部，跳出循环
            if key_name not in config[section]:
                key_flag = -1
                continue
            # 匹配成功后，获取键值
            key_value = config[section][key_name]
            data_html = key_value[0]
            data_xpath = key_value[1]
            data_method = key_value[2]
            data_type = key_value[3]
            data_name = key_value[4]
            if data_html != 'outerHTML' and data_xpath == './':
                fullxpath = get_full_xpath(outerHTML, data_html)
                fullxpath = fullxpath.replace('[document][1]/div[1]','.')
                config[section][key_name][1] = fullxpath
            key_flag += 1
                #config[section][key_name] = [data_html, fullxpath, data_method, data_type, data_name]
    with open(config_file, 'w') as f:
        yaml.dump(config, f)

update_yaml_file('asin')