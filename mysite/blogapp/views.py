from django.views.generic import ListView, DetailView
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy, reverse
from .models import Article


class ArticlesListView(ListView):
    queryset = (
        Article.objects
        .filter(published_at__isnull=False)
        .order_by('-published_at')
    )
    # template_name = 'blogapp/article_list.html'
    # context_object_name = 'articles'
    # queryset = (Article.objects
    #             .select_related("author", "category")
    #             .prefetch_related("tags")
    #             .defer("content")
    #             )


class ArticleDetailView(DetailView):
    model = Article


class LatestArticlesFeed(Feed):
    title = "Blog articles (latest)"
    description = "Updates on changes and addiction blog articles"
    link = reverse_lazy("blogapp:articles")

    def items(self):
        return (
            Article.objects
            .filter(published_at__isnull=False)
            .order_by('-published_at')[:5]
        )

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body[:200]

