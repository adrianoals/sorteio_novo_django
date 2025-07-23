from django.db import models

# Create your models here.

# Representa cada apartamento
class Apartamento(models.Model):
    numero = models.CharField(max_length=5, db_index=True)
    bloco = models.CharField(max_length=30, db_index=True)
    pne = models.BooleanField(default=False, db_index=True)  # Campo para identificar apartamentos PNE
    vaga_coberta = models.BooleanField(default=False, db_index=True)  # Campo para identificar apartamentos com vaga coberta
    vaga_dupla = models.BooleanField(default=False, db_index=True)  # Campo para identificar apartamentos com direito a duas vagas
    
    class Meta:
        indexes = [
            models.Index(fields=['bloco', 'numero']),  # Índice composto para consultas que filtram por bloco e número
            models.Index(fields=['pne']),  # Índice para consultas que filtram por PNE
            models.Index(fields=['vaga_coberta']),  # Índice para consultas que filtram por cobertura
            models.Index(fields=['vaga_dupla']),  # Índice para consultas que filtram por apartamentos com duas vagas
        ]
    
    def __str__(self):
        return f"Apartamento {self.numero} - Bloco {self.bloco}"

# Representa as vagas de garagem
class Vaga(models.Model):
    TAMANHO_CHOICES = [
        ('MEDIA', 'Média'),
        ('GRANDE', 'Grande'),
    ]
    
    ANDAR_CHOICES = [
        ('SUBSOLO_1', 'S1'),
        ('SUBSOLO_2', 'S2'),
        ('SUBSOLO_3', 'S3'),
        ('TERREO', 'Térreo'),
    ]
    
    numero = models.CharField(max_length=80, db_index=True)
    bloco = models.CharField(max_length=30, db_index=True)
    pne = models.BooleanField(default=False, db_index=True)  # Campo para identificar vagas PNE
    vaga_coberta = models.BooleanField(default=False, db_index=True)  # Campo para identificar vagas cobertas
    andar = models.CharField(max_length=20, choices=ANDAR_CHOICES, default='TERREO', db_index=True)  # Campo para identificar o andar/subsolo
    tamanho = models.CharField(max_length=10, choices=TAMANHO_CHOICES, default='MEDIA', db_index=True)  # Campo para identificar o tamanho da vaga
    
    class Meta:
        indexes = [
            models.Index(fields=['bloco', 'numero']),  # Índice composto para consultas que filtram por bloco e número
            models.Index(fields=['pne']),  # Índice para consultas que filtram por PNE
            models.Index(fields=['vaga_coberta']),  # Índice para consultas que filtram por cobertura
            models.Index(fields=['andar']),  # Índice para consultas que filtram por andar
            models.Index(fields=['tamanho']),  # Índice para consultas que filtram por tamanho
        ]
    
    def __str__(self):
        return f"Vaga {self.numero} - Bloco {self.bloco} - {self.get_andar_display()} - {self.get_tamanho_display()}"

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
