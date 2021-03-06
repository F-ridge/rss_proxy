# -*- coding: utf-8 -*-

import os
import json
import yaml
import requests
import urllib
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone


def main():
    config = load_config()
    target_url = config['target_url']
    webhook_url = config['webhook_url']
    proxy = proxy_auth(config)
    post_to_slack(target_url, proxy, webhook_url, yesterday())


def load_config(path=None):
    if path is None:
        path = os.path.join(os.getcwd(), 'config.yml')
    with open(path, 'r', encoding='UTF-8') as yml:
        config = yaml.load(yml, Loader=yaml.FullLoader)
    return config


def proxy_auth(config):
    username = config['username']
    password = config['password']
    server = config['server']
    port = config['port']
    proxies = {"http": f"http://{username}:{password}@{server}:{port}"}
    proxy = urllib.request.ProxyHandler(proxies)
    return proxy


def post_to_slack(target_url, proxy, webhook_url, target_date):
    attachments = feed_of_the_day(target_url, proxy, target_date)
    if attachments == []:
        text = f'【{target_date}に掲示された記事はありません】'
    else:
        text = f'【{target_date}に掲示された記事一覧】'
    requests.post(
        webhook_url,
        data=json.dumps({
            'text': text,
            'attachments': attachments,
            'link_names': 1}))


def feed_of_the_day(target_url, proxy, target_date):
    feed = feedparser.parse(target_url, handlers=[proxy])
    opener = urllib.request.build_opener(proxy)
    urllib.request.install_opener(opener)
    attachments = []
    for entry in feed['entries']:
        if entry['title'][-10:] == target_date:
            attachments += [{
                'title': entry['title'],
                'title_link': entry['link'],
                'text': text_of_article(entry['link'])}]
    return attachments


def text_of_article(url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    soup.head.decompose()
    soup.b.decompose()
    text = ''
    for t in soup.find_all(text=True):
        if t.strip():
            text += t
    return text


def yesterday(tz='JST'):
    tzone = timezone(timedelta(hours=+9), tz)
    return (datetime.now(tz=tzone) + timedelta(days=-1)).strftime("%Y-%m-%d")


if __name__ == '__main__':
    main()
