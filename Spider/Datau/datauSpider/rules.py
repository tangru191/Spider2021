from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

# rules = {
#     'china': (
#         Rule(LinkExtractor(allow='article\/.*\.html', restrict_xpaths='//div[@id="left_side"]//div[@class="con_item"]'),
#              callback='parse_item'),
#         Rule(LinkExtractor(restrict_xpaths='//div[@id="pageStyle"]//a[contains(., "下一页")]'))
#     )
# }
rules = {
    'china': (
        Rule(LinkExtractor(allow='course/list\?page=\d+'), follow=True),
        Rule(LinkExtractor(allow='www.imooc.com/learn/\d+'), callback='parse_item', follow=False)

    )
}
