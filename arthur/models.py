from django.db import models


class Apartamento(models.Model):
    numero_apartamento = models.CharField(max_length=50)
    presenca = models.BooleanField(default=False)  
    prioridade = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.numero_apartamento}"


class Vaga(models.Model):
    vaga = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Vaga {self.vaga}"


class Sorteio(models.Model):
    apartamento = models.OneToOneField(Apartamento, on_delete=models.CASCADE)
    vaga = models.OneToOneField(Vaga, on_delete=models.CASCADE)

    def __str__(self):
        return f"Apartamento {self.apartamento.numero_apartamento} - Vaga: {self.vaga.vaga}"
