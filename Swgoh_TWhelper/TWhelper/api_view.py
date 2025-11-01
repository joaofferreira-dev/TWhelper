from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Team
from .serializers import TeamSerializer


class ArticleView(APIView):
    def get(self, request):
        teams = Team.objects.all()
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = TeamSerializer(teams, many=True)
        return Response({"articles": serializer.data})

    def update(self, instance, validated_data):
        instance.assignment = validated_data.get('assignment', instance.assignment)

        instance.save()
        return instance
