from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from posts.models import Post
from django.db.models import Q, Count, Case, When

class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 5
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('category_post')
        qs = qs.order_by('-id').filter(published_post = True)
        qs = qs.annotate(
            number_comments = Count(
                Case(
                    When(comment__published_comment = True, then=1)
                )
            )
        )

        return qs


class PostSearch(PostIndex):
    template_name = 'posts/post_search.html'
    def get_queryset(self):
        qs = super().get_queryset()
        term = self.request.GET.get('term')

        if not term:
            return qs

        qs = qs.filter(
            Q(title_post__icontains=term) |
            Q(author_post__first_name__iexact=term) |
            Q(content_post__icontains=term) |
            Q(excerpt_post__icontains=term) |
            Q(category_post__name_cate__iexact=term)
        )

        return qs
    
class PostCategory(PostIndex):
    template_name = 'posts/post_category.html'

    def get_queryset(self):
        qs = super().get_queryset()

        category = self.kwargs.get('category', None)

        if not category:
            return qs

        qs = qs.filter(category_post__name_cate__iexact=category)
        return qs

class PostDetails(UpdateView):
    pass
