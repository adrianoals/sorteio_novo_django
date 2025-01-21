from django.db import models

# Representa um bloco do condomínio
class Bloco(models.Model):
    numero = models.CharField(max_length=5, unique=True)  # Ex: "01", "02"

    def __str__(self):
        return f"Bloco {self.numero}"

# Representa cada apartamento
class Apartamento(models.Model):
    bloco = models.ForeignKey(Bloco, on_delete=models.CASCADE, related_name="apartamentos")  # Relaciona com o bloco
    numero = models.CharField(max_length=5)  # Ex: "1404", "1501"
    is_pne = models.BooleanField(default=False)  # Indica se o apartamento é adaptado para PNE

    def __str__(self):
        return f"Apartamento {self.numero} - {self.bloco}"

# Representa as vagas de garagem
class Vaga(models.Model):
    bloco = models.ForeignKey(Bloco, on_delete=models.CASCADE, related_name="vagas", blank=True, null=True)  # Opcionalmente associada a um bloco
    numero = models.CharField(max_length=40)  # Ex: "Vaga 01"
    is_pne = models.BooleanField(default=False)  # Indica se a vaga é reservada para PNE

    def __str__(self):
        if self.bloco:
            return f"{self.numero} - Bloco {self.bloco.numero}"
        return f"{self.numero}"

# Armazena o resultado do sorteio, vinculando apartamentos a vagas
class Sorteio(models.Model):
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    data_sorteio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sorteio: {self.apartamento} -> {self.vaga}"
