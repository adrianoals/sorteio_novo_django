from django.db import models

# Representa cada apartamento
class Apartamento(models.Model):
    numero = models.CharField(max_length=20)  # Ex: "101", "202"
    bloco = models.CharField(max_length=10)  # Ex: "Bloco A", "Bloco 1", "1", "2", etc.
    
    def __str__(self):
        return f"Bloco {self.bloco} - Apartamento {self.numero}"

# Representa as vagas de garagem (apenas carro)
class Vaga(models.Model):
    numero = models.CharField(max_length=20)  # Ex: "Vaga 01", "Vaga 101"
    bloco = models.CharField(max_length=10, null=True, blank=True, help_text="Bloco da vaga (opcional)")  # Ex: "Bloco A", "1", etc.
    
    def __str__(self):
        if self.bloco:
            return f"{self.numero} - Bloco {self.bloco}"
        return f"{self.numero}"

# Armazena o resultado do sorteio, vinculando apartamentos a vagas
class Sorteio(models.Model):
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    data_sorteio = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Sorteio: {self.apartamento} -> {self.vaga}"

