from functools import reduce
import re

import scrapy

from ..items import ParserItem


class HabrSpider(scrapy.Spider):
    name = 'habr'
    allowed_domains = ['freelance.habr.com']
    start_urls = [f'https://freelance.habr.com/tasks?page={i}' for i in range(1, 56)]

    def __init__(self):
        self.table = list()

    def parse(self, response):
        self.table.extend(
            map(
                lambda x: response.urljoin(x),
                response.css(
                    'ul.content-list_tasks li.content-list__item div.task__title a::attr("href")',
                    ).getall(),
                ),
            )

        for project_url in self.table:
            yield scrapy.Request(
                url=project_url,
                callback=self.project_parse,
                )

    def project_parse(self, response):
        data = ParserItem()
        data['link'] = response.url
        data['name'] = (
            response.css('div.task_detail h2::text').get().strip() + response
            .css('div.task_detail h2 span::text').get().strip())
        data['price'] = (response.css('div.task_detail div.task__finance::text').get().strip() + response
                         .css('div.task_detail div.task__finance span::text').get().strip())
        data['tags'] = reduce(lambda x, y: x + ' ' + y if y else x,
                              filter(lambda s: s != '', response
                                     .css('div.task_detail div.task__tags li.tags__item \
                                         a.tags__item_link::text')
                                     .getall()))
        
        [i.strip() for i in response.css(
            'div.task_detail div.task__tags li.tags__item a.tags__item_link::text').getall()]
        data['time'] = re.findall(r'\d{2}:\d{2}',
                                  response.css('div.task_detail div.task__meta::text')
                                  .get().strip())[0]
        data['date'] = re.findall(r'\d{2}\s\w{3,}\s\d{4}',
                                  response.css('div.task_detail div.task__meta::text')
                                  .get().strip())[0]
        data['views'] = response.css(
            'div.task_detail div.task__meta span.count::text').get().strip()
        data['responses'] = response.css(
            'div.task_detail div.task__meta span.count::text').getall()[-1].strip()
        data['description'] = reduce(lambda x, y: x + ' ' + y if y else x,
                                     filter(lambda s: s != '', response
                                            .css('div.task_detail div.task__description::text')
                                            .getall())).strip()
        
        if response.css('div.task_detail div.task__description a::attr("href")') is not None:
            data['description_links'] = [i.strip() for i in response.css(
                'div.task_detail div.task__description a::attr("href")').getall()]
   
        if response.css('div.task_detail dl.user-params').getall() is not None:
            data['user_files'] = [i.strip() for i in response.css(
                'div.task_detail dl.user-params ::attr("href")').getall()]
    
        return data
