from django.db import models

class Imagem(models.Model):
    imagem = models.ImageField(upload_to='imagens/')

    def __str__(self):
        return self.descricao