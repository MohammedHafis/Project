from rest_framework import serializers
from adminapp.models import Movie,Watch_later,View_history

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        
class WatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watch_later
        fields = '__all__'
        
class ViewHistorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='movie.id', read_only=True)
    title = serializers.CharField(source='movie.title', read_only=True)
    thumbnail = serializers.ImageField(source='movie.thumbnail', read_only=True)
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = View_history
        fields = ['id','title', 'thumbnail', 'date']