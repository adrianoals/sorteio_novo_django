from django.db import models

class Apartamento(models.Model):
    
    APARTAMENTO_CHOICES = [
        ('Apto 11', 'Apto 11'),
        ('Apto 12', 'Apto 12'),
        ('Apto 13', 'Apto 13'),
        ('Apto 14', 'Apto 14'),
        ('Apto 21', 'Apto 21'),
        ('Apto 22', 'Apto 22'),
        ('Apto 23', 'Apto 23'),
        ('Apto 24', 'Apto 24'),
        ('Apto 31', 'Apto 31'),
        ('Apto 32', 'Apto 32'),
        ('Apto 33', 'Apto 33'),
        ('Apto 34', 'Apto 34'),
        ('Apto 41', 'Apto 41'),
        ('Apto 42', 'Apto 42'),
        ('Apto 43', 'Apto 43'),
        ('Apto 44', 'Apto 44'),
        ('Apto 51', 'Apto 51'),
        ('Apto 52', 'Apto 52'),
        ('Apto 53', 'Apto 53'),
        ('Apto 54', 'Apto 54'),
        ('Apto 61', 'Apto 61'),
        ('Apto 62', 'Apto 62'),
        ('Apto 63', 'Apto 63'),
        ('Apto 64', 'Apto 64'),
        ('Apto 71', 'Apto 71'),
        ('Apto 72', 'Apto 72'),
        ('Apto 73', 'Apto 73'),
        ('Apto 74', 'Apto 74'),
        ('Apto 81', 'Apto 81'),
        ('Apto 82', 'Apto 82'),
        ('Apto 83', 'Apto 83'),
        ('Apto 84', 'Apto 84'),
        
    ]

    numero_apartamento = models.CharField(max_length=50, choices=APARTAMENTO_CHOICES)
    presenca = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.numero_apartamento}"


class Vaga(models.Model):

    VAGAS_CHOICES = [
        ('Vaga 01', 'Vaga 01'), 
        ('Vaga 02', 'Vaga 02'), 
        ('Vaga 03', 'Vaga 03'), 
        ('Vaga 04', 'Vaga 04'), 
        ('Vaga 05', 'Vaga 05'), 
        ('Vaga 06', 'Vaga 06'), 
        ('Vaga 07', 'Vaga 07'), 
        ('Vaga 08', 'Vaga 08'), 
        ('Vaga 09', 'Vaga 09'), 
        ('Vaga 10', 'Vaga 10'), 
        ('Vaga 11', 'Vaga 11'), 
        ('Vaga 12', 'Vaga 12'), 
        ('Vaga 13', 'Vaga 13'), 
        ('Vaga 14', 'Vaga 14'), 
        ('Vaga 15', 'Vaga 15'), 
        ('Vaga 16', 'Vaga 16'), 
        ('Vaga 17', 'Vaga 17'), 
        ('Vaga 18', 'Vaga 18'), 
        ('Vaga 19', 'Vaga 19'), 
        ('Vaga 20', 'Vaga 20'), 
        ('Vaga 21', 'Vaga 21'), 
        ('Vaga 22', 'Vaga 22'), 
        ('Vaga 23', 'Vaga 23'), 
        ('Vaga 24', 'Vaga 24'), 
        ('Vaga 25', 'Vaga 25'), 
        ('Vaga 26', 'Vaga 26'), 
        ('Vaga 27', 'Vaga 27'), 
        ('Vaga 28', 'Vaga 28'), 
        ('Vaga 29', 'Vaga 29'), 
        ('Vaga 30', 'Vaga 30'), 
        ('Vaga 31', 'Vaga 31'), 
        ('Vaga 32', 'Vaga 32'), 
     
    ]

    vaga = models.CharField(max_length=50, unique=True, choices=VAGAS_CHOICES)

    def __str__(self):
        return self.vaga


class Sorteio(models.Model):
    apartamento = models.OneToOneField(Apartamento, on_delete=models.CASCADE)
    vaga = models.OneToOneField(Vaga, on_delete=models.CASCADE)

    def __str__(self):
        # Acesso ao bloco através do apartamento
        return f"Apartamento {self.apartamento.numero_apartamento}  Vaga: {self.vaga.vaga}"
