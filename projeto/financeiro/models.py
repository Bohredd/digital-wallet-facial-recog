from django.db import models

class Carteira(models.Model):
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    usuario = models.OneToOneField("usuario.Usuario", on_delete=models.CASCADE)

    def __str__(self):
        return f"Carteira de {self.usuario.nome_completo}"

class Transacao(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)
    carteira = models.ForeignKey("financeiro.Carteira", on_delete=models.CASCADE)
    is_entrada = models.BooleanField(default=False)
    is_saida = models.BooleanField(default=False)

    def __str__(self):
        return f"Transação de {self.valor} em {self.data}"

    class Meta:
        ordering = ["-data"]