from api.serializers import (CategorySerializer, CommentsSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleReadSerializer, TitleWriteSerializer)
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from api.permissions import (IsAdmin,
                             IsAdminModeratorAuthorOrReadOnly,
                             IsAdminOrReadOnly)
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAdminOrReadOnly, ]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = TitleReadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year', )

    def get_queryset(self):
        queryset = Title.objects.all()

        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(category__slug=category)

        genre = self.request.query_params.get('genre')
        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)

        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__contains=name)

        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminModeratorAuthorOrReadOnly, ]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_permissions(self):
        if self.action == 'destroy':
            return (IsAdmin(),)
        return super().get_permissions()


class CommentsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminModeratorAuthorOrReadOnly, ]
    serializer_class = CommentsSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)

    def get_permissions(self):
        if self.action == 'destroy':
            return (IsAdmin(),)
        return super().get_permissions()
