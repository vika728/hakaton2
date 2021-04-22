from rest_framework import generics, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from .models import Product, Review, Category, Like, Favorite
from .serializers import ProductSerializer, ReviewSerializer, CategoryDetailSerializer, CategoryListSerializer, \
    FavoriteSerializer
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from cart_product.permissions import IsAuth


class PaginationProduct(PageNumberPagination):
    page_size = 2


class PaginationReview(PageNumberPagination):
    page_size = 2


class PermissionMixin:
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAuth, ]
        else:
            permissions = []
        return [permission() for permission in permissions]


class ProductViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PaginationProduct
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', ]

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        product = self.get_object()
        obj, created = Like.objects.get_or_create(user=request.user, product=product)
        if not created:
            obj.like = not obj.like
            obj.save()
        liked_or_unliked = 'liked' if obj.like else 'unliked'
        return Response('Successfully {} product'.format(liked_or_unliked), status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        product = self.get_object()
        obj, created = Favorite.objects.get_or_create(user=request.user, product=product)
        if not created:
            obj.favorite = not obj.favorite
            obj.save()
        added_removed = 'added' if obj.favorite else 'removed'
        return Response('Successfully {} favorite'.format(added_removed), status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def search(self, request):
        query = request.query_params.get('q')
        queryset = self.get_queryset().filter(Q(title__icontains=query) | Q(description__icontains=query))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def sort(self, request):
        filter = request.query_params.get('filter')
        if filter == 'A-Z':
            queryset = self.get_queryset().order_by('title')
        elif filter == 'Z-A':
            queryset = self.get_queryset().order_by('-title')
        elif filter == 'replies':
            maximum = 0
            for problem in self.get_queryset():
                if maximum < problem.replies.count():
                    maximum = problem.replies.count()
                    queryset = self.get_queryset().filter(id=problem.id)
        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [AllowAny, ]


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class ReviewViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuth, ]


class FavoriteListViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    # permission_classes = [IsAuth, ]

    def get_queryset(self):
        qs = self.request.user
        queryset = super().get_queryset()
        if qs.is_anonymous:
            return ''
            # return Response('вы должны зарегаться', status=status.HTTP_401_UNAUTHORIZED)
        queryset = queryset.filter(user=qs)
        return queryset


    # def get_queryset(self):
    #     qs = self.request.user
    #     queryset = Favorite.objects.filter(user=qs, favorite=True)
    #     return queryset

class FavoriteView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer








