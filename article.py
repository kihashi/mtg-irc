'''
This module allows a bot to give out the 5 most recent articles from a site.

Author: John Cleaver
License: BSD 3 Clause.
'''

import feedparser

rss = {
    'scg': 'http://www.starcitygames.com/rss/rssfeed.xml',
    'tcg': 'http://www.tcgplayer.com/RSS/rssfeed.xml',
    'mtg': 'http://www.wizards.com/Magic/Magazine/rss.aspx',
    'gm': 'http://www.gatheringmagic.com/feed/',
    'cf': 'http://www.channelfireball.com/feed/rss/'
}



def get_rss(site):
    rss_data = feedparser.parse(rss[site])
    return rss_data

def get_articles(site):
    rss_data = get_rss(site)
    length = min(rss_data.entries, 5)

    return rss_data.entries[:length]

def article(phenny, input):

    switch = {
        'scg' : get_scg_articles,
        'tcg' : get_scg_articles,
        'mtg' : get_mtg_articles,
        'gm' : get_gm_articles,
        'cf' : get_cf_articles
    }

    if not input.group(2):
        phenny.reply('Perhaps you meant to specify a site?')
    else:
        if input.group(2).lower() not in rss:
            phenny.reply('That is not a site that I know of.')
        else:
            articles = switch[input.group(2)]()
            for article in articles:
                phenny.reply(article)
article.commands = ['article']
article.priority = 'medium'
article.example = '.article scg'

def get_scg_articles():
    raw_articles = get_articles('scg')
    article_list = []

    for article in raw_articles:
        article_list.append(article['title'] + " | " + article['link'])

    return article_list

def get_tcg_articles():
    raw_articles = get_articles('tcg')
    article_list = []

    for article in raw_articles:
        article_list.append(article['title'] + " | " + article['link'])

    return article_list

def get_mtg_articles():
    raw_articles = get_articles('mtg')
    article_list = []

    for article in raw_articles:
        article_list.append(article['title'] + " | " + article['author'] + " | " + article['link'])

    return article_list

def get_gm_articles():
    raw_articles = get_articles('gm')
    article_list = []

    for article in raw_articles:
        article_list.append(article['title'] + " | " + article['author'] + " | " + article['link'])

    return article_list

def get_cf_articles():
    raw_articles = get_articles('cf')
    article_list = []

    for article in raw_articles:
        article_list.append(article['title'] + " | " + article['author'] + " | " + article['link'])

    return article_list
