from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from posts.models import Group, Post, User

from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """Позволяет получить доступ к постам через API, к созданию,
    редактированию или удалению. Не позволяет изменять/удалять
    пост не автору. Не позволяет создавать/изменять/удалять
    посты неавторизованному пользователю.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Создаём пост."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Позволяет получить доступ только к просмотру данных
    о существующей группе.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    """Позволяет получить доступ к комментариям через API, к созданию,
    редактированию или удалению. Не позволяет изменять/удалять
    комментарии не автору поста. Не позволяет создавать/изменять/удалять
    комментарии неавторизованному пользователю.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """Получаем информацию о комментариях к конкретному посту."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)

        return post.comments.all()

    def perform_create(self, serializer):
        """Создаём комментарий."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)

        serializer.save(author=self.request.user, post=post)


class FollowViewSet(generics.ListCreateAPIView, viewsets.GenericViewSet):
    """Позволяет получить доступ к подпискам через API, к созданию,
    или удалению. Не позволяет подписываться неаутенцифицированным
    пользователям.
    """
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        following = get_object_or_404(
            User,
            username=self.request.user.username,
        )

        return following.follower.all()
