from django.db import models
from django.urls import reverse
from apps.blog.models.abstract import BlogObject


class Article(BlogObject):
    trello_card = models.OneToOneField("trello.Card", related_name="article", on_delete=models.CASCADE)
    blog = models.ForeignKey("blog.Blog", related_name="articles", on_delete=models.CASCADE)

    # topics = models.ManyToManyField("Topic", related_name='articles')
    # keywords = models.CharField(max_length=200, null=False)


    # MODEL PROPERTIES
    @property
    def slug_source(self):
        return self.trello_card.name

    @property
    def title(self):
        return self.trello_card.name

    @property
    def markdown(self):
        return self.trello_card.markdown


    # MODEL FUNCTIONS

    def get_absolute_url(self):
        return reverse('blog:article', kwargs={'blog_slug': self.blog.slug, 'article_slug': self.slug})

