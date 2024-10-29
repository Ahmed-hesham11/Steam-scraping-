# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst,MapCompose
from w3lib.html import remove_tags

def clean_discount_rate(discounted_rate):
        if discounted_rate:
            return discounted_rate.lstrip('-')
        return discounted_rate


def remove_html( rate):
        try:
            clean_rate = remove_tags(rate)
        except TypeError:
            clean_rate = 'NO review'
        return clean_rate

def get_platform( one_class):
        plateformm = []
        
        platform = one_class.split(" ")[-1]
        if platform == "win":
                plateformm.append("Windows")
        if platform == "mac":
                plateformm.append("Mac OS")
        if platform == "linux":
                plateformm.append("Linux")
        else:
                plateformm.append(platform)
        return plateformm

class StemItem(scrapy.Item):
    # define the fields for your item here like:
     game_name = scrapy.Field(
         output_processor=TakeFirst()
     )
     url = scrapy.Field(
         output_processor=TakeFirst()
     )
     img_url = scrapy.Field(
         output_processor=TakeFirst()
     )
     date = scrapy.Field(
         input_processor=MapCompose(str.strip),  # Removes leading and trailing spaces
        output_processor=TakeFirst()
     )
     platform = scrapy.Field(
         input_processor=MapCompose(get_platform),
     )
     rate = scrapy.Field(
         input_processor=MapCompose(remove_html),
          output_processor=TakeFirst()
         
     )
     orginal_price = scrapy.Field(
         output_processor=TakeFirst()
     )
     discounted_price = scrapy.Field(
         output_processor=TakeFirst()
     )
     discounted_rate = scrapy.Field(
         input_processor=MapCompose(clean_discount_rate),
          output_processor=TakeFirst())
     
    
