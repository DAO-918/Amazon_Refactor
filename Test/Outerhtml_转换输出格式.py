# 首先确保已经安装了beautifulsoup4这个库，如果还没有安装，可以通过命令"pip install beautifulsoup4"进行安装

import bs4 as bs

def print_html_nicely(html_code):
    # 使用BeautifulSoup进行解析
    soup = bs.BeautifulSoup(html_code, 'html.parser')
    
    # 使用prettify()函数将HTML代码美化
    pretty_html = soup.prettify()
    
    # 打印美化后的HTML代码，每行打印一次
    for line in pretty_html.split('\n'):
        print(line)

# 测试代码
if __name__ == '__main__':
# 调用上面定义的函数，输入你的HTML代码即可
    your_html_code = '<div class="a-section a-spacing-none a-spacing-top-micro"><div class="a-row a-size-small"><span aria-label="3.8 out of 5 stars"><span class="a-declarative" data-version-id="v36g8q2u37vpji29sg9uhoxaczm" data-render-id="r2wl2si5pfnx952haerwa39igbr" data-action="a-popover" data-csa-c-type="widget" data-csa-c-func-deps="aui-da-a-popover" data-a-popover="{&quot;position&quot;:&quot;triggerBottom&quot;,&quot;popoverLabel&quot;:&quot;&quot;,&quot;url&quot;:&quot;/review/widgets/average-customer-review/popover/ref=acr_search__popover?ie=UTF8&amp;asin=B09PVKBP61&amp;ref_=acr_search__popover&amp;contextId=search&quot;,&quot;closeButton&quot;:false,&quot;closeButtonLabel&quot;:&quot;&quot;}" data-csa-c-id="yphyli-ybbsxe-5zowk9-flsb5i"><a href="javascript:void(0)" role="button" class="a-popover-trigger a-declarative"><i class="a-icon a-icon-star-small a-star-small-4 aok-align-bottom"><span class="a-icon-alt">3.8 out of 5 stars</span></i><i class="a-icon a-icon-popover"></i></a></span> </span><span data-component-type="s-client-side-analytics" class="rush-component" data-version-id="v36g8q2u37vpji29sg9uhoxaczm" data-render-id="r2wl2si5pfnx952haerwa39igbr" data-component-id="59"><div style="display: inline-block" class="s-csa-instrumentation-wrapper alf-search-csa-instrumentation-wrapper" data-csa-c-type="alf-af-component" data-csa-c-content-id="alf-customer-ratings-count-component" data-csa-c-slot-id="alf-reviews" data-csa-op-log-render="" data-csa-c-layout="GRID" data-csa-c-asin="B09PVKBP61" data-csa-c-id="hfakx5-jo1cap-azwcao-azu450"><span aria-label="13,221"><a class="a-link-normal s-underline-text s-underline-link-text s-link-style" href="/TEMI-Dinosaur-Tyrannosaurus-Transport-Activity/dp/B09PVKBP61/ref=sr_1_1?crid=1348F1WA6OH7W&amp;dib=eyJ2IjoiMSJ9.bxuiv5XF5oX2Dy3hx-IyeTZ75mr4sn3L6g9vNoKBfLbLDd44_9TacnQGtAIN7R93ct32mn128Fv55oyVH6h5ICskcLZTL3XU6ygozLqcYCPOptPunfTikEbLgpAhp-IKMmLa39GvDsh0GH92bOp6vVuMKeaAJRbm74aEd_JtERKqhQIOC7ZmfeTL9wJkczMQwOh5OP2fsaHQiKk0CtU9Fqv0_POxpr2sgkQ3qWvZCxIPdqIYf-moT999AOiXBDlFa1p88Zi3ZIV3TdCc55TIP17Yo9vf-w-pHf5yUwA7aNI.ZDWfkpFwN1M-ObJfypzXVVwVwW3sgurvzUDDW_RXLcE&amp;dib_tag=se&amp;keywords=dinosaur+toys&amp;qid=1709710835&amp;sprefix=%2Caps%2C2499&amp;sr=8-1#customerReviews"><span class="a-size-base s-underline-text">13,221</span> </a> </span></div></span></div><div class="a-row a-size-base"><span class="a-size-base a-color-secondary">8K+ bought in past month</span></div></div>'
    print_html_nicely(your_html_code)
