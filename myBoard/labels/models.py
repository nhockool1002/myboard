from django.db import models


class ExLabels(models.Model):
    id = models.AutoField(primary_key=True)
    label_name = models.TextField(blank=True, null=True)
    label_slug = models.CharField(max_length=255, blank=True, null=True, unique=True)
    label_type = models.IntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)


    class Meta:
        db_table = 'ex_labels'
