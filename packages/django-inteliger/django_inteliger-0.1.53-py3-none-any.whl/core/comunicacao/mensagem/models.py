from django.db import models
import core.models


# Create your models here.
class Mensagem(core.models.Log):
    nome = models.CharField(max_length=200, primary_key=True)
    nm_descritivo = models.CharField(max_length=200, null=True)
    conteudo = models.TextField(null=True)
    variaveis = models.TextField(null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'comunicacao_mensagem'


class MensagemLog(core.models.Log):
    mensagem = models.ForeignKey('Mensagem', on_delete=models.DO_NOTHING, null=True)
    destinatario = models.CharField(max_length=200, null=True)
    retorno = models.TextField(null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'comunicacao_mensagem_log'