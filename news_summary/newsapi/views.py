from rest_framework import generics, permissions
from rest_framework.response import Response
from django.conf import settings
import requests
from .models import SavedArticle
from .serializers import UserSerializer, SavedArticleSerializer
from transformers import pipeline

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text):
    # Return fallback if text too short
    if not text or len(text.strip()) < 20:
        return "No summary available"
    summary = summarizer(text, max_length=50, min_length=20, do_sample=False)
    return summary[0]['summary_text']


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer


class LatestNewsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        url = f"https://newsapi.org/v2/everything?q=technology&apiKey={settings.NEWSAPI_KEY}"
        response = requests.get(url).json()
        articles = response.get('articles', [])
        summarized = []
        for art in articles[:3]:   # limit to first 3
            summarized.append({
                'title': art['title'],
                'url': art['url'],
                'summary': summarize_text(art.get('description') or art.get('content') or '')
            })
        return Response(summarized)


class SearchNewsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        term = request.GET.get('q')
        url = f"https://newsapi.org/v2/everything?q={term}&apiKey={settings.NEWSAPI_KEY}"
        response = requests.get(url).json()
        articles = response.get('articles', [])
        summarized = []
        for art in articles[:3]:
            summarized.append({
                'title': art['title'],
                'url': art['url'],
                'summary': summarize_text(art.get('description') or art.get('content') or '')
            })
        return Response(summarized)


class SaveArticleView(generics.CreateAPIView):
    serializer_class = SavedArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class SavedArticlesView(generics.ListAPIView):
    serializer_class = SavedArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedArticle.objects.filter(user=self.request.user)
