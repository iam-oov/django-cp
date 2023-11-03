from django.db import models


class Settlement(models.Model):
    slug = models.SlugField(max_length=200)
    key = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    zone_type = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

    def __str__(self):
        return "{0}: {1}".format(self.pk, self.name)


class Municipality(models.Model):
    slug = models.SlugField(max_length=200)
    key = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    settlement_r = models.ForeignKey(
        Settlement, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}: {1}".format(self.pk, self.name)


class FederalEntity(models.Model):
    slug = models.SlugField(max_length=200)
    key = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200, null=True)
    municipality_r = models.ForeignKey(
        Municipality, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}: {1}".format(self.pk, self.name)


class Entity(models.Model):
    slug = models.SlugField(max_length=200)
    zip_code = models.PositiveIntegerField()
    locality = models.CharField(max_length=200)  # ciudad
    federal_entity_r = models.ForeignKey(
        FederalEntity,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "{0}: {1}".format(self.zip_code, self.locality)

    @property
    def federal_entity(self):
        return {
            'key': self.federal_entity_r.key,
            'name': self.federal_entity_r.name,
            'code': self.federal_entity_r.code
        }
