from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.translation import gettext as _

from PIL import Image
import io


# Create your models here.

class Village(models.Model):
    name = models.CharField(_('गांव का नाम'), max_length=100, default=None)
    code = models.IntegerField(_('गांव कोड'), default=None)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super(Village, self).save(*args, **kwargs)

    def __str__(self):
        return "%s" % (self.name)


class Shreni(models.Model):
    shreni = models.CharField(_('श्रेणी'), max_length=10)
    shreni_description = models.TextField(default=None)

    def __str__(self):
        return self.shreni


class Plot(models.Model):
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    shreni = models.ForeignKey(Shreni, on_delete=models.CASCADE)
    gata_number = models.CharField(_('गाटा संख्या'), max_length=50, default=None)
    area = models.FloatField(_('क्षेत्रफल (हैक्‍टेयर)'), default=None)
    shreni_desc = models.TextField()
    distance_road = models.FloatField(_('सड़क से दूरी (कि.मी.)'), default=None)
    connectivity = models.BooleanField(_('कनेक्टिविटी'))
    allotted = models.BooleanField(_('आवंटित'), default=False)
    latitude_coordinate = models.CharField(_('अक्षांश निर्देशांक'), max_length=15, default=None)
    longitude_coordinate = models.CharField(_('देशांतर निर्देशांक'), max_length=15, default=None)
    image = models.ImageField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # print(io.StringIO(self.image.read()))
        shreni_obj = Shreni.objects.get(shreni=self.shreni)
        self.shreni_desc = shreni_obj.shreni_description

        if self.image:
            img = Image.open(self.image)
            resize = img.resize((400, 400), Image.ANTIALIAS)
            new_image = io.BytesIO()
            resize.save(new_image, format=img.format, quality=90)
            temp_name = self.image.name
            self.image.save(temp_name, content=ContentFile(new_image.getvalue()), save=False)
        return super(Plot, self).save(*args, **kwargs)

    def __str__(self):
        return "%s" % (self.gata_number)
