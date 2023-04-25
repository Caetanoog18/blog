from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from posts.models import Post
from django.db.models import Q, Count, Case, When
from comments.forms import FormComment
from comments.models import Comment
from django.contrib import messages


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
    template_name ='posts/post_details.html'
    model = Post
    form_class = FormComment
    context_object_name = 'post'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the current post
        post = self.get_object()
        comments = Comment.objects.filter(published_comment = True, post_comment = post.id)

        context['comments'] = comments
        return context

    def form_valid(self, form):
        post = self.get_object()
        comment = Comment(**form.cleaned_data)
        comment.post_comment = post

        # Checking if the user is logged in
        if self.request.user.is_authenticated:
            comment.user_comment = self.request.user

        comment.save()
        messages.success(self.request, 'Comment sent successfully!')
        return redirect('post_details', pk=post.id)

