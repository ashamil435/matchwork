import scrapy


class ParserItem(scrapy.Item):
    link: str = scrapy.Field()  # ССылка на проект
    name: str = scrapy.Field()  # Название проекта
    price: str = scrapy.Field(max_length=15)  # Стоимость проекта
    tags: str = scrapy.Field(null=True)  # Теги проекта (если есть)
    time: str = scrapy.Field(max_length=5)  # Время публикации проекта
    date: str = scrapy.Field(max_length=25)  # Дата публикации проекта
    views: int = scrapy.Field(max_length=3)  # Сколько просмотров
    responses: int = scrapy.Field(max_length=3)  # Количество откликов
    description: str = scrapy.Field()  # Описание проекта
    description_links: list[str] = scrapy.Field(null=True)  # Ссылки которые есть в проекте
    user_files: list[str] = scrapy.Field(null=True)  # Приложенные файлы


'''
В дальнейшем сделаем так чтобы количество
просмотров/откликов/и тд обновлялось ежеминутно
'''
