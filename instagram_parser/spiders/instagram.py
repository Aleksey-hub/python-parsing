import json
import re
from copy import deepcopy
from urllib.parse import urlencode

import scrapy
from scrapy.http import HtmlResponse

from instagram_parser.items import InstagramParserItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com', 'i.instagram.com']
    start_urls = ['https://www.instagram.com/']

    login_link = 'https://www.instagram.com/accounts/login/ajax/'
    # считываем данные для авторизации из json файла
    with open('../authorization.json') as f:
        authorization = json.load(f)
        user_name = authorization['username']
        password = authorization['enc_password']
    csrf_token = None

    graphql_url = 'https://www.instagram.com/graphql/query/?'
    query_hash = 'd4d88dc1500312af6f937f7b804c68c3'

    def __init__(self, users):
        super(InstagramSpider, self).__init__()
        self.users = users

    def parse(self, response: HtmlResponse):
        yield scrapy.FormRequest(self.login_link,
                                 method='POST',
                                 callback=self.is_login,
                                 formdata={'username': f'{self.user_name}', 'enc_password': f'{self.password}'},
                                 headers={'x-csrftoken': f'{self.get_csrf_token(response)}'})

    def is_login(self, response: HtmlResponse):
        # Проверка успешности аутентификации
        json_data = response.json()
        if json_data['authenticated']:
            for user in self.users:
                yield response.follow(f'/{user}', callback=self.followers_parse, cb_kwargs={'user_name': user})
                yield response.follow(f'/{user}', callback=self.following_parse, cb_kwargs={'user_name': user},
                                      dont_filter=True)

    def followers_parse(self, response: HtmlResponse, user_name):
        user_id = self.get_user_id(response.text, user_name)
        variables = {'count': 12,
                     'search_surface': 'follow_list_page'}
        url_api = self.formation_followers_url(user_id, variables)
        yield response.follow(url_api, callback=self.user_data_parse, cb_kwargs={'user_name': user_name,
                                                                                 'user_id': user_id,
                                                                                 'variables': deepcopy(variables),
                                                                                 'is_follower': True})

    def following_parse(self, response: HtmlResponse, user_name):
        user_id = self.get_user_id(response.text, user_name)
        variables = {'count': 12}
        url_api = self.formation_following_url(user_id, variables)
        yield response.follow(url_api, callback=self.user_data_parse, cb_kwargs={'user_name': user_name,
                                                                                 'user_id': user_id,
                                                                                 'variables': deepcopy(variables),
                                                                                 'is_following': True})

    def user_data_parse(self, response: HtmlResponse, user_name, user_id, variables, is_follower=None,
                        is_following=None):
        json_data = response.json()

        if json_data.get('next_max_id') and is_follower:
            url_api = self.formation_followers_url(user_id, variables, json_data['next_max_id'])
            yield response.follow(url_api, callback=self.user_data_parse, cb_kwargs={'user_name': user_name,
                                                                                     'user_id': user_id,
                                                                                     'variables': deepcopy(variables),
                                                                                     'is_follower': is_follower})
        elif json_data.get('next_max_id') and is_following:
            url_api = self.formation_following_url(user_id, variables, json_data['next_max_id'])
            yield response.follow(url_api, callback=self.user_data_parse, cb_kwargs={'user_name': user_name,
                                                                                     'user_id': user_id,
                                                                                     'variables': deepcopy(variables),
                                                                                     'is_following': is_following})

        if is_follower:
            for user_foll in json_data['users']:
                item = InstagramParserItem(user_name=user_name,
                                           user_id_foll=user_foll['pk'],
                                           user_name_foll=user_foll['username'],
                                           user_pic_link_foll=user_foll['profile_pic_url'],
                                           is_follower=is_follower)
                yield item
        elif is_following:
            for user_foll in json_data['users']:
                item = InstagramParserItem(user_name=user_name,
                                           user_id_foll=user_foll['pk'],
                                           user_name_foll=user_foll['username'],
                                           user_pic_link_foll=user_foll['profile_pic_url'],
                                           is_following=is_following)
                yield item

    def formation_followers_url(self, user_id, variables, max_id=None):
        # Формирование url для получения списка подписчиков
        if max_id:
            variables['max_id'] = max_id
        return f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?{urlencode(variables)}'

    def formation_following_url(self, user_id, variables, max_id=None):
        # Формирование url для получения списка подписок
        if max_id:
            variables['max_id'] = max_id
        return f'https://i.instagram.com/api/v1/friendships/{user_id}/following/?{urlencode(variables)}'

    def get_csrf_token(self, response: HtmlResponse):
        # Получение csrf_token'а
        csrf_token = re.search(r'"csrf_token":"(.*?)",', response.text).group(1)
        return csrf_token

    def get_user_id(self, text, user_name):
        # Получение id пользователя
        user_id = re.search(fr'"id":"(\d+)","username":"{user_name}"', text).group(1)
        return user_id
