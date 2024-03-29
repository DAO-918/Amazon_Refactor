from bs4 import BeautifulSoup

def find_full_xpath(outer_html, target):
    # 解析HTML
    soup = BeautifulSoup(outer_html, 'html.parser')
    # 找到目标标签
    target_element = soup.find(target)
    # 初始化一个列表来存储路径
    path = []
    # 开始循环，找到父标签，直到找不到为止
    while target_element is not None:
        # 将当前标签的名称添加到路径中
        path.append(target_element.name)
        # 找到当前标签的父标签
        target_element = target_element.find_parent()
    # 翻转路径列表，并用'/'来连接它们，形成完整的xpath
    full_path = '/'.join(reversed(path))
    # 返回完整的xpath
    return full_path

# 使用实际的HTML代码替换'your_html_code_here'
outer_html = '''<div class="celwidget" data-cel-widget="title_feature_div" data-csa-c-asin="B09V38ST65" data-csa-c-content-id="title" data-csa-c-id="253bro-5zma3h-awnwra-6em3lg" data-csa-c-is-in-initial-active-row="false" data-csa-c-slot-id="title_feature_div" data-csa-c-type="widget" data-feature-name="title" id="title_feature_div">
 <style type="text/css">
  .product-title-word-break {
        word-break: break-word;
    }
 </style>
 <div class="a-section a-spacing-none" id="titleSection">
  <h1 class="a-size-large a-spacing-none" id="title">
   <span class="a-size-large product-title-word-break" id="productTitle">
    PLAYBEA Dinosaur Toys - 12 7-Inch Realistic Dinosaurs Figures with Storage Box |Dino Toys for Kids 3-5 5-7 | Toddler Boy Toys
   </span>
  </h1>
  <div class="a-section a-spacing-none expand aok-hidden" id="expandTitleToggle">
  </div>
 </div>
</div>'''

# 输出outer_html中<span>标签的完整xpath
print(find_full_xpath(outer_html, '''<span class="a-size-large product-title-word-break" id="productTitle">'''))
