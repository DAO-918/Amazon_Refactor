import configparser

def startInit():
    # 读取配置文件
    config = configparser.ConfigParser()
    config_file_path = 'C:\\AutoRPA\\Config.ini'
    with open(config_file_path, encoding='utf-8') as f:
        config.read_file(f)

    # 获取文件路径配置信息
    # file_route = config.get('File_Route', 'File_Route')
    # 全局变量的声明和赋值不能放在同一行
    # global rpa_file_path
    # global keyword_file_path
    # global kscore_file_path
    # global krank_file_path
    # global kfre_file_path
    # global kcomp_file_path
    # global history_file_path
    # global info_file_path
    # global record_file_path
    # global review_file_path
    # global arank_file_path
    # global picture_file_path
    # global ptrsc_file_path
    # global test_file_path
    rpa_file_path = config.get('Route', 'RPAFilePath')
    keyword_file_path = config.get('Route', 'KeywordFilePath')
    kscore_file_path = config.get('Route', 'KScoreFilePath')
    krank_file_path = config.get('Route', 'KRankFilePath')
    kfre_file_path = config.get('Route', 'KFrequFilePath')
    kcomp_file_path = config.get('Route', 'KCompFilePath')
    history_file_path = config.get('Route', 'HistoryFilePath')
    info_file_path = config.get('Route', 'InfoFilePath')
    record_file_path = config.get('Route', 'RecordFilePath')
    review_file_path = config.get('Route', 'ReviewFilePath')
    arank_file_path = config.get('Route', 'ARankFilePath')
    picture_file_path = config.get('Route', 'PictureFilePath')
    ptrsc_file_path = config.get('Route', 'PtrscFilePath')
    test_file_path = config.get('Route', 'TestFilePath')

    return {
        'rpa_file_path': rpa_file_path,
        'keyword_file_path': keyword_file_path,
        'kscore_file_path': kscore_file_path,
        'krank_file_path': krank_file_path,
        'kfre_file_path': kfre_file_path,
        'kcomp_file_path': kcomp_file_path,
        'history_file_path': history_file_path,
        'info_file_path': info_file_path,
        'record_file_path': record_file_path,
        'review_file_path': review_file_path,
        'arank_file_path': arank_file_path,
        'picture_file_path': picture_file_path,
        'ptrsc_file_path': ptrsc_file_path,
        'test_file_path': test_file_path,
    }