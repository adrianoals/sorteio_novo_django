from django.db import models

# Create your models here.

# Representa cada apartamento
class Apartamento(models.Model):
    numero = models.CharField(max_length=5, db_index=True)
    torre = models.CharField(max_length=2, default='A', db_index=True)
    pne = models.BooleanField(default=False, db_index=True)  # Campo para identificar apartamentos PNE
    
    class Meta:
        indexes = [
            models.Index(fields=['torre', 'numero']),  # Índice composto para consultas que filtram por torre e número
            models.Index(fields=['pne']),  # Índice para consultas que filtram por PNE
        ]
    
    def __str__(self):
        return f"Apartamento {self.numero} - Torre {self.torre}"

# Representa as vagas de garagem
class Vaga(models.Model):
    numero = models.CharField(max_length=20, db_index=True)
    torre = models.CharField(max_length=2, db_index=True)
    pne = models.BooleanField(default=False, db_index=True)  # Campo para identificar vagas PNE
    
    class Meta:
        indexes = [
            models.Index(fields=['torre', 'numero']),  # Índice composto para consultas que filtram por torre e número
            models.Index(fields=['pne']),  # Índice para consultas que filtram por PNE
        ]
    
    def __str__(self):
        return f"Vaga {self.numero} - Torre {self.torre}"

# Armazena o resultado do sorteio, vinculando apartamentos a vagas
class Sorteio(models.Model):
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE, db_index=True)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, db_index=True)
    data_sorteio = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['apartamento', 'vaga']),  # Índice composto para consultas que relacionam apartamento e vaga
        ]
    
    def __str__(self):
        return f"Sorteio: {self.apartamento} -> {self.vaga}"


