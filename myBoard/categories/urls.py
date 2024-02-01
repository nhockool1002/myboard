from django.urls import path
from myBoard.categories.views import ExCategoriesAPI
urlpatterns = [
    path('ex-categories/', ExCategoriesAPI.as_view(), name='ex_categories'),
    path('ex-categories/<int:id>', ExCategoriesAPI.as_view(), name='ex_categories_update'),
]
