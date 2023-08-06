from django.db import models
import core.models
# Create your models here.


class EmailEndereco(core.models.Log):
    email = models.EmailField(max_length=200, null=True)
    port = models.IntegerField(null=True)
    host = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'comunicacao_email_endereco'


class Email(core.models.Log):
    nome = models.CharField(max_length=200, primary_key=True)
    nm_descritivo = models.CharField(max_length=200, null=True)
    assunto = models.CharField(max_length=200, null=True)
    conteudo = models.TextField(null=True)
    endereco = models.ForeignKey('EmailEndereco', on_delete=models.DO_NOTHING, null=True, related_name='endereco_email')
    variaveis = models.TextField(null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'comunicacao_email'


class EmailLog(core.models.Log):
    email = models.ForeignKey('Email', on_delete=models.DO_NOTHING, null=True)
    destinatario = models.CharField(max_length=200, null=True)
    retorno = models.TextField(null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'comunicacao_email_log'
