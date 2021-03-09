import graphene
from graphene_django import DjangoObjectType

# import models.
from cookbook.ingredients.models import Category, Ingredient

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")

class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    # is this a graphen convention to point to resolve function.
    def resolve_all_ingredients(root, info):
        return Ingredient.objects.select_related("category").all()
    
    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            # what is None? Is it like Null.
            return None

schema =graphene.Schema(query=Query)
