from tastypie.resources import ModelResource
from tastypie import fields
from cadastro.models import *
from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class UsuarioResource(ModelResource):

    def obj_create(self, bundle, **kwargs):
        if not (Usuario.objects.filter(nome=bundle.data['nome'])):
            usuario = Usuario()
            usuario.nome = bundle.data['nome']
            usuario.email = bundle.data['email']
            usuario.senha = bundle.data['senha']
            usuario.save()
            bundle.obj = usuario
            return bundle
        else:
            raise Unauthorized('Já existe um usuario com este nome')

    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Não é possível apagar a lista!")

    class Meta:
        queryset = Usuario.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        excludes = ['senha']
        filtering = {
            "nome": ('exact', 'startswith',)
        }


class ProjetoResource(ModelResource):

    def obj_create(self, bundle, **kwargs):
        if not (Projeto.objects.filter(nome=bundle.data['nome'])):
            projeto = Projeto()
            projeto.nome = bundle.data['nome']
            projeto.save()
            bundle.obj = projeto
            return bundle
        else:
            raise Unauthorized('Já existe um projeto com este nome')

    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Não é possível apagar a lista!")

    class Meta:
        queryset = Projeto.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "nome": ('exact', 'startswith',)
        }




class TarefaResource(ModelResource):
    usuario = fields.ToOneField(UsuarioResource, 'usuario')
    projeto = fields.ToOneField(ProjetoResource, 'projeto')

    class Meta:
        queryset = Tarefa.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "titulo": ('exact', 'startswith',)
        }

    def obj_create(self, bundle, **kwargs):
        u = bundle.data['usuario'].split("/")[-2]
        p = bundle.data['projeto'].split("/")[-2]

        if not Tarefa.objects.filter(nome=bundle.data['nome']):
            tarefa = Tarefa()
            tarefa.nome = bundle.data['nome']
            tarefa.dataEHoraDeInicio = bundle.data['dataEHoraDeInicio']
            tarefa.usuario = Usuario.objects.get(pk=u)
            tarefa.projeto = Projeto.objects.get(pk=p)
            tarefa.save()
            bundle.obj = tarefa
            return bundle
        else:
            raise Unauthorized("Tarefa ja cadastrada.")

    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Não é possível apagar a lista!")




class ProjetoUsuarioResource(ModelResource):
    projeto = fields.ToOneField(ProjetoResource, 'projeto')
    usuario = fields.ToOneField(UsuarioResource, 'usuario')

    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Não é possível apagar a lista!")

    class Meta:
        queryset = ProjetoUsuario.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "titulo": ('exact', 'startswith',)
        }

    def obj_create(self, bundle, **kwargs):
        u = bundle.data['usuario'].split("/")
        p = bundle.data['projeto'].split("/")
        if not (ProjetoUsuario.objects.filter(usuario=u[4], projeto=p[4])):

            projetoUsuario = ProjetoUsuario()
            projetoUsuario.usuario = Usuario.objects.get(pk=int(u[4]))
            projetoUsuario.projeto = Projeto.objects.get(pk=int(p[4]))
            projetoUsuario.save()
            bundle.obj = projetoUsuario
            return bundle
        else:
            raise Unauthorized("Associação já cadastrada anteriormente!")


