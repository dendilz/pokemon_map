from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField('Имя на русском', max_length=200)
    title_en = models.CharField('Имя на английском', max_length=200, blank=True)
    title_jp = models.CharField('Имя на японском', max_length=200, blank=True)
    image = models.ImageField('Изображение', upload_to='pokemons', blank=True)
    description = models.TextField('Описание', blank=True)
    next_evolution = models.ForeignKey('self',
                                       verbose_name='В кого эволюционирует',
                                       related_name='nxt_evolution',
                                       blank=True, null=True,
                                       on_delete=models.SET_NULL)
    previous_evolution = models.ForeignKey('self',
                                           verbose_name='Из кого эволюционирует',
                                           related_name='prv_evolution',
                                           blank=True, null=True,
                                           on_delete=models.SET_NULL)

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField('Координата широты')
    lon = models.FloatField('Координата долготы')
    appeared_at = models.DateTimeField('Дата и время появления')
    disappeared_at = models.DateTimeField('Дата и время исчезновения')
    level = models.IntegerField('Уровень')
    health = models.IntegerField('Здоровье', null=True, blank=True)
    strength = models.IntegerField('Атака', null=True, blank=True)
    defence = models.IntegerField('Защита', null=True, blank=True)
    stamina = models.IntegerField('Выносливость', null=True, blank=True)

    def __str__(self):
        return self.pokemon.title_ru