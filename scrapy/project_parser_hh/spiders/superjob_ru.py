import scrapy
from scrapy.http import HtmlResponse
from project_parser_hh.items import ProjectParserSuperJobItem


class SuperjobRuSpider(scrapy.Spider):
    name = 'superjob_ru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4&page=1']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@rel='next']/@href").get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

        urls_vacancies = response.xpath("//span[@class='_2KHVB _3l13l _3l6qV _3PTah _3xCPT rygxv _17lam _2Ovds']//@href").getall()
        for url_vacancy in urls_vacancies:
            url_vacancy = "https://www.superjob.ru" + url_vacancy
            yield response.follow(url_vacancy, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):

        vacancy_name = response.xpath("//h1/text()").get()
        vacancy_salary = response.xpath("//span[@class = '_2eYAG _3xCPT rygxv _3GtUQ']//text()").getall()
        vacancy_url = response.url

        if len(vacancy_salary) == 1:
            vacancy_salary_from = vacancy_salary[0]
            vacancy_salary_to = vacancy_salary[0]
        else:
            if len(vacancy_salary) == 3 and vacancy_salary[0] == 'от':
                vacancy_salary_from = vacancy_salary[2].replace('\xa0', '').replace('₽', '')
                vacancy_salary_to = ''

            if len(vacancy_salary) == 3 and vacancy_salary[0] == 'до':
                vacancy_salary_from = ''
                vacancy_salary_to = vacancy_salary[2].replace('\xa0', '').replace('₽', '')

            if len(vacancy_salary) == 7:
                vacancy_salary_from = vacancy_salary[0].replace('\xa0', '')
                vacancy_salary_to = vacancy_salary[4].replace('\xa0', '')


        yield ProjectParserSuperJobItem(
            name=vacancy_name,
            url=vacancy_url,
            salary_min=vacancy_salary_from,
            salary_max=vacancy_salary_to
        )