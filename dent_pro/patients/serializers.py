from rest_framework import serializers
from .models import Patient
from django.conf import settings

class PatientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Patient
        fields = ['id', 'name', 'info', 'image', 'created_at']
        extra_kwargs = {
            'image': {'required': False, 'allow_null': True}
        }
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['image']:
            request = self.context.get('request')
            if request:
                data['image'] = request.build_absolute_uri(instance.image.url)
        return data 