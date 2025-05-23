from django.contrib import admin
from .models import AdminTheme
from django import forms

class AdminThemeForm(forms.ModelForm):
    primary_color = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'color',
            'onchange': 'updateBackgroundColor(this.value, this.form.dataset.themeId);'
        })
    )
    secondary_color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))
    
    class Meta:
        model = AdminTheme
        fields = ('name', 'css_url', 'js_url', 'is_active', 'primary_color', 'secondary_color')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter l'ID du thème au formulaire
        if self.instance.pk:
            self.fields['primary_color'].widget.attrs.update({
                'data-theme-id': str(self.instance.pk),
                'class': 'theme-color-picker'
            })

@admin.register(AdminTheme)
class AdminThemeAdmin(admin.ModelAdmin):
    form = AdminThemeForm
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'css_url', 'js_url', 'is_active')
        }),
        ('Personnalisation des couleurs', {
            'fields': ('primary_color', 'secondary_color')
        })
    )

    class Media:
        js = ('admin_theme/js/color_picker.js',)
    
    
   