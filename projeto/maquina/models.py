from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Maquina(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    empresa_contratante = models.ForeignKey("empresa.Empresa", on_delete=models.CASCADE)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class EstoqueProduto(models.Model):
    produto = models.ForeignKey("Produto", on_delete=models.CASCADE)
    maquina = models.ForeignKey("Maquina", on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data_entrada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.produto} - {self.quantidade} unidades"

class TransacaoMaquina(models.Model):
    maquina = models.ForeignKey("Maquina", on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    is_entrada = models.BooleanField(default=False)
    is_saida = models.BooleanField(default=False)
    produto_movimentado = models.ForeignKey("Produto", on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    usuario_responsavel = models.ForeignKey("usuario.Usuario", on_delete=models.CASCADE)

    def __str__(self):
        return f"Transação de {self.maquina} em {self.data}"

    def save(self, *args, **kwargs):
        try:
            produto_estoque = EstoqueProduto.objects.get(
                produto=self.produto_movimentado, maquina=self.maquina
            )
        except ObjectDoesNotExist:
            raise ValueError("Estoque para este produto e máquina não encontrado.")

        if self.is_entrada:
            produto_estoque.quantidade += self.quantidade
            produto_estoque.save()
        elif self.is_saida:
            usuario = self.usuario_responsavel

            if usuario.carteira.saldo < self.produto_movimentado.preco * self.quantidade:
                raise ValueError("Saldo insuficiente.")
            if produto_estoque.quantidade < self.quantidade:
                raise ValueError("Estoque insuficiente.")

            usuario.carteira.saldo -= self.produto_movimentado.preco * self.quantidade
            usuario.carteira.save()
            produto_estoque.quantidade -= self.quantidade
            produto_estoque.save()

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-data"]
