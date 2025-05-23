from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import AdminTheme
from .serializers import AdminThemeSerializer
from .tasks import compile_theme_css  
from django.http import HttpResponse

class AdminThemeViewSet(viewsets.ModelViewSet):
    queryset = AdminTheme.objects.all()
    serializer_class = AdminThemeSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [permissions.IsAdminUser()]  # seul un admin peut modifier
        return [permissions.AllowAny()]  # lecture ouverte


def upload_scss_view(request):
    if request.method == 'POST':
        scss_file = request.FILES['scss_file']
        # Enregistrez le fichier SCSS et obtenez son chemin
        scss_file_path = save_scss_file(scss_file) # type: ignore
        # Appeler la tâche Celery
        compile_theme_css.delay(scss_file_path)
        return HttpResponse('Fichier SCSS téléchargé et en cours de compilation.')


def theme_editor(request):
    return render(request, 'admin_theme/theme_editor.html')
