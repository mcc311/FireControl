from django.db import models

BELONG_STATE = (('e', 'Enemy'),
                ('a', 'Ally'),
                ('b', 'Both'))
# Create your models here.
class Missile(models.Model):
    type = models.CharField(unique=True, blank=False, max_length=100, null=True)
    default_num = models.IntegerField(null=False, default=2)
    belongs_to = models.CharField(max_length=1, choices=BELONG_STATE, default='b')

    def __str__(self):
        return self.type
    class Meta:
        db_table = "missile"

    # ordering = ('type', 'default_num')

class Vessel(models.Model):
    typename = models.CharField(blank=False, max_length=100, null=True)
    type_id = models.CharField(blank=False, max_length=100, null=True)
    value = models.FloatField(null=False, default=.5)
    belongs_to = models.CharField(max_length=1, choices=BELONG_STATE, default='b')
    default_fires = models.ManyToManyField(Missile, default=0)

    class Meta:
        unique_together = [('typename', 'type_id')]

