from django.db import models

# Create your models here.

class Web(models.Model):
    address = models.TextField() #url que queremos acortar.

    def __str__(self):
        return "(" + str(self.id) + ")" + " " + self.address
