from django.db import models


class FederalEntity(models.Model):
    slug = models.SlugField(max_length=30)
    key = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)

    def __str__(self):
        return "{0}: {1}".format(self.slug, self.name)


class Municipality(models.Model):
    slug = models.SlugField(max_length=30)
    key = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return "{0}: {1}".format(self.slug, self.name)


class Settlement(models.Model):
    slug = models.SlugField(max_length=30)
    key = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=200)
    zone_type = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

    def __str__(self):
        return "{0}: {1}".format(self.slug, self.name)


class Entity(models.Model):
    zip_code = models.PositiveIntegerField()
    locality = models.CharField(max_length=400)  # ciudad
