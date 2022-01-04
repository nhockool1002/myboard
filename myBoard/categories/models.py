from django.db import models


class ExCategories(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.TextField(blank=True, null=True)
    category_slug = models.CharField(max_length=255, blank=True, null=True, unique=True)
    order = models.IntegerField(blank=True, null=True, default=0)
    sticky = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)


    class Meta:
        db_table = 'ex_categories'
