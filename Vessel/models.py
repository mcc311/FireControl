from django.db import models

BELONG_STATE = (('e', '敵軍'),
                ('a', '我軍'),
                ('b', '共同'))
# Create your models here.
class Missile(models.Model):
    type = models.CharField(unique=True, blank=False, max_length=100, null=True)
    default_num = models.IntegerField(null=False, default=2)
    belongs_to = models.CharField(max_length=1, choices=BELONG_STATE, default='b')
    damage = models.FloatField(null=False, default=.5)
    cost = models.FloatField(null=False, default=.5)

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
    fire1 = models.ForeignKey(Missile, default=1, on_delete=models.SET_DEFAULT, related_name='fire1')
    fire2 = models.ForeignKey(Missile, default=1, on_delete=models.SET_DEFAULT, related_name='fire2')
    def __str__(self):
        return f"{self.typename}({self.type_id})"
    class Meta:
        unique_together = [('typename', 'type_id')]

