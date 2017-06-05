from django.db import models
from django.utils import timezone


class Usuario(models.Model):
    nome = models.CharField('nome',max_length=100)
    email = models.CharField('email', max_length=50)
    senha = models.CharField('senha', max_length=50)


class Projeto(models.Model):
    nome = models.CharField('nome', max_length=100)


class Tarefa(models.Model):
    nome = models.CharField('nome', max_length=100)
    dataEHoraDeInicio = models.DateTimeField('dataEHoraDeInicio', default=timezone.now)
    usuario = models.ForeignKey('usuario')
    projeto = models.ForeignKey('projeto')


class ProjetoUsuario(models.Model):
    projeto = models.ForeignKey('projeto')
    usuario = models.ForeignKey('usuario')
