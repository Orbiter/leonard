"""
name: news
description: "Get last news from Google News or Yandex News"
priority: 250
"""
import json

import feedparser

import requests
import leonard
import leonard.utils
import leonard.utils.ru

# See comments for weather plugin
NEWS_RU_WORDS = leonard.utils.keywords_from_words(
    leonard.utils.ru.vowel_ends('новост'))


def get_news_data(rss_url, n=5):
    feed = feedparser.parse(rss_url)
    news = []
    for entry in feed['entries']:
        news.append({'title': entry['title'], 'url': entry['link']})
    return news[:n]


@leonard.hooks.keywords(NEWS_RU_WORDS + [['news']])
def news_message(message, bot):
    news_data = get_news_data(message.locale.rss_url)
    news = []
    for post in news_data:
        news.append('{title} - {url}\n'.format(title=post['title'],
                                               url=post['url']))
    answer = leonard.OutgoingMessage(
        recipient=message.sender,
        text=message.locale.news_report.format('\n'.join(news)),
        variables={"telegram_hide_preview": True}
    )
    bot.send_message(answer)


class EnglishLocale(leonard.locale.EnglishLocale):
    language_code = 'en'

    rss_url = 'https://news.google.com/news?cf=all&hl=en&ned=us&output=rss'

    news_report = 'Last news:\n\n{}'


class RussianLocale(leonard.locale.RussianLocale):
    language_code = 'ru'

    rss_url = 'https://news.yandex.ru/index.rss'

    news_report = 'Последние новости:\n\n{}'
