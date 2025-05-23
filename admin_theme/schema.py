import graphene
from graphene_django.types import DjangoObjectType
from .models import AdminTheme
from .tasks import set_active_theme
from django.core.exceptions import ValidationError


# ✅ Type GraphQL basé sur le modèle Django
class AdminThemeType(DjangoObjectType):
    class Meta:
        model = AdminTheme


# ✅ Mutation pour activer un thème
class ActivateTheme(graphene.Mutation):
    class Arguments:
        theme_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    message = graphene.String()
    theme = graphene.Field(AdminThemeType)

    def mutate(self, info, theme_id):
        user = info.context.user
        if not user.is_authenticated or not user.is_superuser:
            raise Exception("🚫 Accès interdit : superutilisateur requis.")

        try:
            theme = AdminTheme.objects.get(id=theme_id)
            theme.is_active = True
            theme.save()

            # Appeler Celery pour désactiver les autres
            set_active_theme.delay(theme.id)

            return ActivateTheme(ok=True, message="Thème activé via Celery", theme=theme)
        except AdminTheme.DoesNotExist:
            return ActivateTheme(ok=False, message="Thème introuvable", theme=None)


# ✅ Mutation pour créer un thème avec validation
class CreateTheme(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        css_url = graphene.String(required=True)
        js_url = graphene.String()

    ok = graphene.Boolean()
    message = graphene.String()
    theme = graphene.Field(AdminThemeType)

    def mutate(self, info, name, css_url, js_url=None):
        user = info.context.user
        if not user.is_authenticated or not user.is_superuser:
            raise Exception("🚫 Accès interdit : superutilisateur requis.")

        try:
            theme = AdminTheme(
                name=name.strip(),
                css_url=css_url.strip(),
                js_url=js_url.strip() if js_url else None
            )
            theme.full_clean()  # exécute les validations du modèle
            theme.save()
            return CreateTheme(ok=True, message="Thème créé avec succès.", theme=theme)
        except ValidationError as e:
            return CreateTheme(ok=False, message=str(e), theme=None)
        except Exception as e:
            return CreateTheme(ok=False, message=str(e), theme=None)


# ✅ Mutations GraphQL disponibles
class Mutation(graphene.ObjectType):
    activate_theme = ActivateTheme.Field()
    create_theme = CreateTheme.Field()


# ✅ Requêtes disponibles
class Query(graphene.ObjectType):
    all_themes = graphene.List(AdminThemeType)

    def resolve_all_themes(self, info):
        return AdminTheme.objects.all()


# ✅ Schéma final à exposer
schema = graphene.Schema(query=Query, mutation=Mutation)


