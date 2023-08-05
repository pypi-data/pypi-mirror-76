from django.db import models


class Exc(models.Model):
    exc_type = models.TextField()
    exc_value = models.TextField()
    exc_traceback = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'django_exc'
