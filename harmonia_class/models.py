from django.db import models


class Apartamento(models.Model):
    numero = models.CharField(max_length=5)
    direito_vaga_dupla = models.BooleanField(default=False)
    is_pne = models.BooleanField(default=False)

    def __str__(self):
        return f"Apartamento {self.numero}"


class Vaga(models.Model):
    LOCALIZACAO_CHOICES = [
        ('Térreo', 'Térreo'),
        ('Pavimento 1', 'Pavimento 1'),
        ('Pavimento 2', 'Pavimento 2'),
    ]

    numero = models.CharField(max_length=50)
    localizacao = models.CharField(max_length=15, choices=LOCALIZACAO_CHOICES)
    tipo_vaga = models.CharField(max_length=10, choices=[('Simples', 'Simples'), ('Dupla', 'Dupla')])
    is_pne = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.numero} - {self.localizacao} ({self.tipo_vaga})"


class Sorteio(models.Model):
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    data_sorteio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sorteio: {self.apartamento} -> {self.vaga}"
