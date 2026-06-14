from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from .models import BlogPost, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class BlogPostListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            "id", "title", "slug", "excerpt", "category",
            "author_name", "featured_emoji", "read_time",
            "is_featured", "published_at", "views",
        ]


class BlogPostDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = "__all__"


class BlogPostListView(APIView):
    def get(self, request):
        qs = BlogPost.objects.filter(is_published=True)
        category = request.query_params.get("category")
        if category:
            qs = qs.filter(category__slug=category)
        serializer = BlogPostListSerializer(qs, many=True)
        return Response(serializer.data)


class BlogPostDetailView(APIView):
    def get(self, request, slug):
        try:
            post = BlogPost.objects.get(slug=slug, is_published=True)
        except BlogPost.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        post.views += 1
        post.save(update_fields=["views"])
        serializer = BlogPostDetailSerializer(post)
        return Response(serializer.data)
