import graphene
from admin_theme.schema import Query as ThemeQuery, Mutation as ThemeMutation

class Query(ThemeQuery, graphene.ObjectType):
    pass

class Mutation(ThemeMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
