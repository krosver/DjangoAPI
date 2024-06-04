from rest_framework import status, viewsets, generics, permissions, mixins, renderers, authentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.http import Http404
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Color, Embroidery
from .serializers import ColorSerializer, EmbroiderySerializer, UserSerializer
# from .permissions import IsOwnerOrReadOnly


class EmbroiderList(APIView):
    def get(self, request, format=None):
        embroiders = Embroidery.objects.all()
        serializer_class = EmbroiderySerializer(embroiders, many=True)
        return Response(serializer_class.data)


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all().order_by('id')
    serializer_class = ColorSerializer


class EmbroideryDetail(APIView):
    def get_object(self, embroidery_id):
        try:
            return Embroidery.objects.get(id=embroidery_id)
        except Embroidery.DoesNotExist:
            raise Http404

    def get(self, request, embroidery_id, format=None):
        embroidery = self.get_object(embroidery_id)
        serializer = EmbroiderySerializer(embroidery)
        return Response(serializer.data)


@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        embroiders = Embroidery.objects.filter(Q(Name__icontains=query) | Q(Description__icontains=query))
        serializer = EmbroiderySerializer(embroiders, many=True)
        return Response(serializer.data)
    else:
        return Response({"embroiders": []})


class CurrentUserView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class MyEmbroideryList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        embroiders = Embroidery.objects.filter(User_id=request.user)
        serializer = EmbroiderySerializer(embroiders, many=True)
        return Response(serializer.data)



# class EmbroideryDetail(generics.RetrieveAPIView):
#     queryset = Embroidery.objects.all()
#     serializer_class = EmbroiderySerializer


# class SnippetList(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     permission_classes = [IsOwnerOrReadOnly]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'users': reverse('user-list', request=request, format=format),
#         'snippets': reverse('snippet-list', request=request, format=format)
#     })
#
# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     renderer_classes = [renderers.StaticHTMLRenderer]
#
#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)
