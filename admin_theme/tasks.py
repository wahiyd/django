from celery import shared_task
import time
from celery import shared_task
from .models import AdminTheme


@shared_task
def compile_theme_css(theme_name):
    print(f"🛠 Compilation SCSS pour le thème : {theme_name}")
    time.sleep(2)
    return f"Le thème '{theme_name}' a été compilé avec succès."

@shared_task
def set_active_theme(theme_id):
    try:
        # Désactiver tous les thèmes
        AdminTheme.objects.exclude(id=theme_id).update(is_active=False)

        # Activer le thème sélectionné
        selected_theme = AdminTheme.objects.get(id=theme_id)
        selected_theme.is_active = True
        selected_theme.save()

        return f"Thème '{selected_theme.name}' activé. Tous les autres désactivés."

    except AdminTheme.DoesNotExist:
        return "Thème introuvable."




