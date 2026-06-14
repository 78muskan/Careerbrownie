from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "notification_type", "title", "message", "link", "is_read", "created_at"]


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Notification.objects.filter(user=request.user)
        unread_only = request.query_params.get("unread")
        if unread_only:
            qs = qs.filter(is_read=False)
        return Response({
            "notifications": NotificationSerializer(qs[:20], many=True).data,
            "unread_count": Notification.objects.filter(user=request.user, is_read=False).count(),
        })


class MarkReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ids = request.data.get("ids", [])
        if ids == "all":
            Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        else:
            Notification.objects.filter(user=request.user, id__in=ids).update(is_read=True)
        return Response({"message": "Marked as read."})
