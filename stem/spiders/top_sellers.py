import scrapy
from ..items import StemItem
from scrapy.loader import ItemLoader

class TopSellersSpider(scrapy.Spider):
    name = "top_sellers"
    allowed_domains = ["store.steampowered.com"]
    start_urls = ["https://store.steampowered.com/search/?sort_by=_ASC&filter=topsellers&supportedlang=english&start=0"]

    # Starting index for pagination
    start = 0
    step = 50  # Increment for each page; adjust based on observed pagination behavior

    def parse(self, response):
        games = response.xpath('//div[@id="search_resultsRows"]/a')
        if not games:
            return  # Stop if no games are found (end of pages)

        for game in games:
            lodaer=ItemLoader(item=StemItem(),selector=game,response=response)
            
            lodaer.add_xpath("url",".//@href")
            lodaer.add_xpath("img_url",".//div[@class='col search_capsule']/img/@src")
            lodaer.add_xpath("game_name",'.//div[@class="responsive_search_name_combined"]/div/span[@class="title"]/text()')
            lodaer.add_xpath("date",'.//div[@class="responsive_search_name_combined"]/div[@class="col search_released responsive_secondrow"]/text()')
            lodaer.add_xpath("platform",'.//span[contains(@class, "platform_img") or @class="vr_supported"]/@class')
            lodaer.add_xpath("rate",".//span[contains(@class, 'search_review_summary')]/@data-tooltip-html")
            lodaer.add_xpath("orginal_price",'.//div[@class="discount_prices"]/div[@class="discount_final_price"]/text()')
            lodaer.add_xpath("discounted_price",'.//div[@class="discount_prices"]/div[@class="discount_original_price"]/text()')
            lodaer.add_xpath("discounted_rate",".//div[@class='discount_pct']/text()")
            yield lodaer.load_item()

        # Pagination logic
        self.start += self.step
        next_page_url = f"https://store.steampowered.com/search/?sort_by=_ASC&filter=topsellers&supportedlang=english&start={self.start}"
        
        # Request the next page if more pages are expected
        yield scrapy.Request(url=next_page_url, callback=self.parse)
