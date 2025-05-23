from django.db import models
from django.core.validators import URLValidator

class AdminTheme(models.Model):
    name = models.CharField(max_length=100, unique=True)
    css_url = models.URLField(validators=[URLValidator()])
    js_url = models.URLField(validators=[URLValidator()], blank=True, null=True)
    is_active = models.BooleanField(default=False)
    
    # Nouvelles propriétés pour les couleurs
    primary_color = models.CharField(max_length=7, default="#000000")  # Format hexadécimal
    secondary_color = models.CharField(max_length=7, default="#FFFFFF")
    
    # Layout
    SIDEBAR_POSITIONS = [
        ('left', 'Gauche'),
        ('right', 'Droite'),
    ]
    sidebar_position = models.CharField(
        max_length=5,
        choices=SIDEBAR_POSITIONS,
        default='left'
    )
    
    # Variables SCSS
    scss_variables = models.TextField(
        blank=True,
        help_text="Variables SCSS personnalisées (format: variable: valeur;)"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Thème Admin"
        verbose_name_plural = "Thèmes Admin"
    
    def save(self, *args, **kwargs):
        if self.is_active:
            # Désactiver tous les autres thèmes
            AdminTheme.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
