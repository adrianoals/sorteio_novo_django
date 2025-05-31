# syntax=docker/dockerfile:1   ## permite camadas mais eficientes

##########################
# Stage 1 – build layer  #
##########################
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

# Dependências de sistema para compilar psycopg2 e afins
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev && \
    pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt .
# Se NÃO acrescentou whitenoise no requirements, descomente a linha de baixo
# RUN echo "whitenoise==6.6.0" >> requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte
COPY . .

#############################
# Stage 2 – runtime layer   #
#############################
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

# Bibliotecas SO necessárias apenas para execução
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 \
        netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Copia pacotes Python já instalados e a aplicação
COPY --from=builder /usr/local /usr/local
COPY --from=builder /code /code

# Script de inicialização (wait-for-db, migrate, collectstatic)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "setup.wsgi:application", "--bind", "0.0.0.0:8000"]
