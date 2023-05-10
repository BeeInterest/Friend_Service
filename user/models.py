import uuid

from django.db import models


class Users(models.Model):
    '''Таблица пользователей'''

    class Meta:
        db_table = 'users'

    id = models.UUIDField(verbose_name='Уникальный идентификатор пользователя', primary_key=True, default=uuid.uuid4)
    username = models.CharField(verbose_name='Логин пользователя', max_length=500)

    def __str__(self):
        return f'Пользователь: {self.username}'


class Relations(models.Model):
    '''Таблица отношений пользователей'''

    class Meta:
        db_table = 'relations'

    id = models.AutoField(verbose_name='Уникальный идентификатор связи', primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.RESTRICT, verbose_name='Логин пользователя, установившего связь',
                             max_length=500, related_name='user')
    user_friend = models.ForeignKey(Users, on_delete=models.RESTRICT,
                                    verbose_name='Логин пользователя, с которым связь эта установлена', max_length=500, related_name='user_friend')
    status = models.CharField(verbose_name='Их статус', max_length=50)

    def __str__(self):
        return f'Пользователь1:{self.user}, пользователь2: {self.user_friend} -> Статус: {self.status}'
