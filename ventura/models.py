from django.db import models

class Bloco(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome


class Apartamento(models.Model):
    numero_apartamento = models.CharField(max_length=50)
    presenca = models.BooleanField(default=False)
    bloco = models.ForeignKey(Bloco, on_delete=models.CASCADE, related_name="apartamentos")  

    def __str__(self):
        return f"{self.numero_apartamento} - {self.bloco.nome}"


class Vaga(models.Model):
    vaga = models.CharField(max_length=50, unique=True)
    subsolo = models.CharField(max_length=20)  # Ex: "Subsolo 1", "Subsolo 2"

    def __str__(self):
        return f"Vaga {self.vaga} - {self.subsolo}"


class Sorteio(models.Model):
    apartamento = models.OneToOneField(Apartamento, on_delete=models.CASCADE)
    vaga = models.OneToOneField(Vaga, on_delete=models.CASCADE)

    def __str__(self):
        return f"Apartamento {self.apartamento.numero_apartamento} ({self.apartamento.bloco.nome}) - Vaga: {self.vaga.vaga} ({self.vaga.subsolo})"
