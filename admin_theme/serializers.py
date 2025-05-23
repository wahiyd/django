from rest_framework import serializers
from .models import AdminTheme

class AdminThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminTheme
        fields = ['id', 'name', 'css_url', 'js_url', 'is_active', 
                 'primary_color', 'secondary_color', 
                 'sidebar_position', 'scss_variables']
