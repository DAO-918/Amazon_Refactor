from bs4 import BeautifulSoup

def find_full_xpath(soup, target):
    # 获取目标元素的标签名
    tag_name = target.name
    # 获取目标元素的class属性
    class_attr = target.get('class')
    # 将目标元素的标签名初始化为完整的xpath
    full_xpath = f'//{tag_name}'
    # 如果目标元素有class属性，将其添加到xpath中
    if class_attr:
        full_xpath += f'[@class="{"".join(class_attr)}"]'
    # 获取目标元素的父元素
    parent = target.find_parent()
    # 当目标元素有父元素时
    while parent is not None:
        # 将父元素的标签名添加到xpath中
        full_xpath = f'/{parent.name}{full_xpath}'
        # 如果父元素有class属性，将其添加到xpath中
        if parent.get('class'):
            full_xpath = f'[{"".join(parent.get("class"))}]'+full_xpath
        # 获取父元素的父元素
        parent = parent.find_parent()
    # 返回完整的xpath
    return full_xpath

#TODO:如li或者div的class相同的情况出现，匹配可以有多个时，就不会准确，如何结合feature进行匹配

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


outer_html = '''<div class="celwidget" data-cel-widget="tellAmazon_feature_div" data-csa-c-asin="B09V38ST65" data-csa-c-content-id="tellAmazon" data-csa-c-id="ohv926-t58216-mev1vg-g73bw8" data-csa-c-is-in-initial-active-row="false" data-csa-c-slot-id="tellAmazon_feature_div" data-csa-c-type="widget" data-feature-name="tellAmazon" id="tellAmazon_feature_div">
 <div cel_widget_id="tell-amazon-desktop_DetailPage_2" class="celwidget c-f" data-cel-widget="tell-amazon-desktop_DetailPage_2" data-csa-c-content-id="DsUnknown" data-csa-c-id="pef1b5-hahm81-89h6d-aic3bd" data-csa-c-painter="tell-amazon-desktop-cards" data-csa-c-slot-id="DsUnknown-3" data-csa-c-type="widget" data-csa-op-log-render="">
  <!--CardsClient-->
  <div data-acp-tracking="{}" data-card-metrics-id="tell-amazon-desktop_DetailPage_2" data-mix-claimed="true" id="CardInstanceWSaRJZFMfOiGx57-pZHeSw">
   <div class="_tell-amazon-desktop_style_tell_amazon_div__1YDZk" data-asin="B09V38ST65" data-logged-in="false" data-marketplace="ATVPDKIKX0DER">
    <a class="_tell-amazon-desktop_style_tell_amazon_link__1KW5z" data-mix-operations="openTellAmazonModal">
     <i aria-label="Report an issue with this product or seller" class="a-icon a-icon-share-sms a-icon-mini" role="img">
     </i>
     Report an issue with this product or seller
    </a>
   </div>
   <span class="a-popover-preload" id="a-popover-tellAmazon-modal-1">
    <div class="_tell-amazon-desktop_style_tell_amazon_modal_root__1q10s" data-a-modal-id="tellAmazon-modal-1">
     <div class="_tell-amazon-desktop_style_tell_amazon_modal_end__30n3x">
      <div class="_tell-amazon-desktop_style_tell_amazon_modal_spinner__3bz5K">
       <span class="a-spinner a-spinner-medium">
       </span>
      </div>
     </div>
    </div>
   </span>
  </div>
 </div>
</div>'''
print(find_full_xpath(outer_html, '''<div class="_tell-amazon-desktop_style_tell_amazon_modal_root__1q10s" data-a-modal-id="tellAmazon-modal-1">'''))


outer_html = '''<div class="celwidget" data-cel-widget="featurebullets_feature_div" data-csa-c-asin="B09V38ST65" data-csa-c-content-id="featurebullets" data-csa-c-id="nedm1-2rm20i-jtuq94-muueo7" data-csa-c-is-in-initial-active-row="false" data-csa-c-slot-id="featurebullets_feature_div" data-csa-c-type="widget" data-feature-name="featurebullets" id="featurebullets_feature_div">
 <div class="a-section a-spacing-medium a-spacing-top-small" id="feature-bullets">
  <ul class="a-unordered-list a-vertical a-spacing-mini">
   <li class="a-spacing-mini">
    <span class="a-list-item">
     INCLUDES: 12 realistic, colorful dinosaur figures that are durable and made from high-quality material, Metal Storage box
    </span>
   </li>
   <li class="a-spacing-mini">
    <span class="a-list-item">
     12 DINOSAUR FIGURES: features Diplodocus, Gallimimus, Allosaurus, Triceratops Prorsus, Tyrannosaurus, Stygimoloch, Brontosaurus, Ankylosaurus, Stegosaurus, Parasaurolophus, Spinosaurus, Triceratops
    </span>
   </li>
   <li class="a-spacing-mini">
    <span class="a-list-item">
     METAL STORAGE BOX: Our metal storage box is durable metal with beautifully designed dinosaur images which makes playing more exciting &amp; fun
    </span>
   </li>
   <li class="a-spacing-mini">
    <span class="a-list-item">
     NON-TOXIC &amp; BPA FREE: The dinosaurs are made of non-toxic and high-quality PVC material, which will make them more durable and safe. Allowing your kids to play safely for a long time.
    </span>
   </li>
   <li class="a-spacing-mini">
    <span class="a-list-item">
     REAT GIFT: The dinosaur figures are packaged beautifully which makes it a perfect gift for kids, Great educational toy to help kids learn about different dinosaurs.
    </span>
   </li>
  </ul>
  <!-- Loading EDP related metadata -->
 </div>
</div>'''
print(find_full_xpath(outer_html, '''<li class="a-spacing-mini">'''))