from datetime import datetime

from django.shortcuts import render, redirect
from django.conf import settings
import json
from django.views import View
from django.http import Http404, HttpResponse



class MainPage(View):
    def get(self, request):
        return redirect('/news')


class NewsPage(View):
    def get(self, request):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            article_list = json.loads(json_file.read())

        articles = []
        for article in article_list:
            article['created'] = article['created'][0:10]
            articles.append(article) # aa

        q = request.GET.get('q')
        if q:
            filtered_articles = []
            for article in articles:
                if q in article['title']:
                    filtered_articles.append(article)
            articles = filtered_articles
        print(articles)
        sorted_articles = sorted(articles, key=lambda d: d['created'], reverse=True)
        return render(request, 'news/index.html', {'d': sorted_articles})


class Article(View):
    def get(self, request, article_id):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            json_content = json.loads(json_file.read())
        for article in json_content:
            if article_id == article['link']:
                return render(request, 'news/single_article.html', {'article': article})
        raise Http404


class CreateNews(View):
    def get(self, request):
        return render(request, 'news/create_news.html')

    def post(self, request):
        existing_links = []
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            json_content = json.loads(json_file.read())
        for item in json_content:
            existing_links.append(int(item['link']))
        link = max(existing_links) + 1
        title = request.POST.get('title')
        text = request.POST.get('text')
        json_content.append(
            {'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'text': text, 'title': title, 'link': link}
        )
        with open(settings.NEWS_JSON_PATH, 'w') as json_file_w:
            json_file_w.truncate(0)
            json_file_w.write(json.dumps(json_content))
        return redirect('/news')
