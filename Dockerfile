# Stage 1: build dependencies
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code

# Instala compiladores e bibliotecas para psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# Copia arquivos de dependências e instala
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . /code/

# Stage 2: prepara imagem final
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code

# Instala as bibliotecas necessárias para rodar e o netcat para o entrypoint
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libpq5 \
       netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copia dependências e código da etapa builder
COPY --from=builder /usr/local /usr/local
COPY --from=builder /code /code

# Copia e dá permissão ao entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "setup.wsgi:application", "--bind", "0.0.0.0:8000"]
