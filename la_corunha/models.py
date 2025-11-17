from django.db import models

# Representa cada apartamento
class Apartamento(models.Model):
    TIPO_VAGA_CHOICES = [
        ('Carro', 'Carro'),  # Apartamento com direito a vaga de carro
        ('Moto', 'Moto'),    # Apartamento com direito a vaga de moto
    ]
    
    numero = models.CharField(max_length=20)  # Ex: "Apartamento 1", "Apartamento 46"
    tipo_vaga_direito = models.CharField(
        max_length=10, 
        choices=TIPO_VAGA_CHOICES,
        help_text="Tipo de vaga que o apartamento tem direito (Carro ou Moto)"
    )
    
    def __str__(self):
        return self.numero

# Representa as vagas de garagem (carro ou moto)
class Vaga(models.Model):
    TIPO_VAGA_CHOICES = [
        ('Carro', 'Carro'),
        ('Moto', 'Moto'),
    ]
    
    numero = models.CharField(max_length=20)  # Ex: "Vaga 01", "Vaga Moto 01"
    tipo_vaga = models.CharField(max_length=10, choices=TIPO_VAGA_CHOICES)
    
    def __str__(self):
        return f"{self.numero} ({self.tipo_vaga})"

# Armazena o resultado do sorteio, vinculando apartamentos a vagas
class Sorteio(models.Model):
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    data_sorteio = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Sorteio: {self.apartamento} -> {self.vaga}"

