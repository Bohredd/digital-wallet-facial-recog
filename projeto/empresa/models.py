from django.db import models

class Estado(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.nome} ({self.sigla})"

class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome}/{self.estado}"

class Endereco(models.Model):
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.bairro} - {self.cidade}/{self.estado}"


class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=11, blank=True)
    email = models.EmailField(blank=True)
    logo = models.ImageField(upload_to='imagens/', blank=True, null=True)

    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.nome