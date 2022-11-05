import scrapy


class ArticleSpider(scrapy.Spider):
    name = "news"
    start_urls = [
        'https://www.bbc.com/news/world/europe',
    ]
    
    def parse(self, response):
        for quote in response.css("article"):
            try:
                text = quote.css("p::text").getall()
                
                yield{
                    "text": " ".join(text)
                }
            except:
                yield{
                    "text": "wtf am i doing"
                }

        feed = response.css('ol')
        links = feed.css('a')
        
        for link in links:          
            yield response.follow(link.attrib['href'], callback=self.parse)

