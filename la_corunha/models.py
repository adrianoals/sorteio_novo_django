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
    is_carro = models.BooleanField(default=False, help_text="True se for vaga de carro")
    is_moto = models.BooleanField(default=False, help_text="True se for vaga de moto")
    
    def save(self, *args, **kwargs):
        # Atualizar automaticamente os campos booleanos baseado no tipo_vaga
        if self.tipo_vaga == 'Carro':
            self.is_carro = True
            self.is_moto = False
        elif self.tipo_vaga == 'Moto':
            self.is_carro = False
            self.is_moto = True
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.numero} ({self.tipo_vaga})"

# Armazena o resultado do sorteio, vinculando apartamentos a vagas
class Sorteio(models.Model):
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    data_sorteio = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Sorteio: {self.apartamento} -> {self.vaga}"

