from django.urls import path
from myBoard.labels.views import ExLabelsAPI
urlpatterns = [
    path('ex-labels/', ExLabelsAPI.as_view(), name='ex_labels'),
    path('ex-labels/<int:id>', ExLabelsAPI.as_view(), name='ex_labels_update'),
]
