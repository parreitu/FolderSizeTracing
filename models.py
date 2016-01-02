from django.db import models
from localflavor.generic.forms import DateTimeField

# Create your models here.
class Folder(models.Model):
    name = models.CharField(max_length=128, unique=True)
    path = models.CharField(max_length=128, unique=True)
    managers_name = models.CharField(max_length=128)
    managers_email = models.EmailField()
    quota_mb = models.IntegerField()

    def __unicode__(self):
        return self.name

class Historical(models.Model):
    folder = models.ForeignKey(Folder)
    size_mb = models.IntegerField()
    timestamp = models.DateTimeField()
    # Files changed since the last check
    files_changed = models.TextField()
    delta_mb = models.IntegerField()
    # Ficheros no accedidos en los ultimos X meses
    files_not_accessed = models.TextField()
    not_accessed_mb = models.IntegerField()       
    # Ficheros grandes creados desde el last check
    big_files_changed = models.TextField()
    big_files_delta_mb = models.IntegerField()
    big_files_size_mb = models.IntegerField()

    def __unicode__(self):
        return str(self.folder) + "-" + str(self.timestamp)
