from django.db import models

# Create your models here.

# Representa cada apartamento
class Apartamento(models.Model):
    numero = models.CharField(max_length=5)
    torre = models.CharField(max_length=2, default='A')
    
    def __str__(self):
        return f"Apartamento {self.numero} - Torre {self.torre}"

# Representa as vagas de garagem
class Vaga(models.Model):
    numero = models.CharField(max_length=20)
    torre = models.CharField(max_length=2)
    
    def __str__(self):
        return f"Vaga {self.numero} - Torre {self.torre}"

# Armazena o resultado do sorteio, vinculando apartamentos a vagas
class Sorteio(models.Model):
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    data_sorteio = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Sorteio: {self.apartamento} -> {self.vaga}"


