from django.shortcuts import get_object_or_404
from .models import Category


def get_category_ids(category_slug):
    """Get the category with the given slug and all of its children ids."""
    category = get_object_or_404(Category, slug=category_slug)
    category_ids = [category.id]

    # Iterate over children categories and add their ids to the list
    children = category.children.all()
    while children.exists():
        category_ids.extend(child.id for child in children)
        children = Category.objects.filter(parent__in=children)

    return category_ids