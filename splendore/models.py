from django.db import models

# Create your models here.

# Representa cada apartamento
class Apartamento(models.Model):
    numero = models.CharField(max_length=5)
    direito_vaga_dupla = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Apartamento {self.numero}"

# Representa as vagas de garagem, incluindo simples e duplas
class Vaga(models.Model):
    numero = models.CharField(max_length=20) 
    subsolo = models.CharField(max_length=10)
    tipo_vaga = models.CharField(max_length=10, choices=[('Simples', 'Simples'), ('Dupla', 'Dupla')])
    
    def __str__(self):
        return f"{self.numero} - {self.subsolo} ({self.tipo_vaga})"

# Armazena o resultado do sorteio, vinculando apartamentos a vagas
class Sorteio(models.Model):
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    data_sorteio = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Sorteio: {self.apartamento} -> {self.vaga}"
