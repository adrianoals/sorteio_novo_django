# Sorteio Novo

🇺🇸 [Read in English](README.md)

Sistema automatizado de sorteio de vagas de garagem para condomínios residenciais. Desenvolvido para a **Villa Nova Condomínios** pela **XNAP**.

O Sorteio Novo gerencia a atribuição justa e transparente de vagas de estacionamento em múltiplos empreendimentos, cada um com suas próprias regras de prioridade, acessibilidade e tratamento de vagas duplas/pareadas.

## Tech Stack

- **Backend:** Django 5.0 / Python 3.12
- **Banco de dados:** PostgreSQL (Supabase)
- **Servidor:** Gunicorn + WhiteNoise
- **Deploy:** Docker (build multi-stage) + Traefik como proxy reverso
- **Relatórios:** openpyxl / pandas (Excel), reportlab / WeasyPrint (PDF), qrcode (QR codes)
- **Frontend:** Templates Django, Bootstrap 5, AngularJS (em algumas views)

## Funcionalidades

- **Motor de sorteio por empreendimento** — cada app de condomínio possui seu próprio algoritmo de alocação com suporte a prioridade PNE, vagas duplas/pareadas, alocações fixas e restrições por subsolo
- **Importação/exportação Excel** — gera planilhas de resultados a partir de templates por empreendimento
- **Consulta por QR code** — moradores podem consultar sua vaga atribuída pelo número do apartamento
- **Reset e re-sorteio** — resultados podem ser apagados e o sorteio refeito
- **Django admin** — CRUD completo para apartamentos, vagas e resultados
- **Pronto para produção** — Docker + Traefik com TLS, arquivos estáticos comprimidos, conexões persistentes com o banco

## Estrutura do Projeto

```
setup/                  # Configuração do projeto Django (settings, urls, wsgi)
  static/               # Arquivos estáticos fonte (JS, CSS, assets)
    assets/modelos/      # Templates Excel por condomínio
templates/
  sorteio_novo/          # Templates base compartilhados e partials
  {app_name}/            # Templates específicos por app
{app_name}/              # Um app Django por condomínio (13 apps)
  models.py              # Apartamento, Vaga, Sorteio (+ variantes)
  views.py               # Lógica do sorteio, exportação Excel, QR code, reset
  urls.py                # Padrões de URL prefixados por app
  admin.py               # Configuração do admin
Dockerfile               # Imagem de produção multi-stage
docker-compose.yml       # Orquestração Gunicorn + Traefik
entrypoint.sh            # Wait-for-DB, migrate, collectstatic
```

## Como Começar

### Pré-requisitos

- Python 3.12+
- PostgreSQL (ou descomente a configuração SQLite em `setup/settings.py` para desenvolvimento local)

### Instalação

```bash
git clone <repo-url>
cd sorteio_novo_django

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Preencha as variáveis de ambiente (veja abaixo)

python manage.py migrate
python manage.py runserver
```

### Docker

```bash
docker compose up --build
```

## Variáveis de Ambiente

Copie `.env.example` para `.env` e preencha os valores:

| Variável | Descrição |
|---|---|
| `SECRET_KEY` | Chave secreta do Django |
| `POSTGRES_DB` | Nome do banco de dados |
| `POSTGRES_USER` | Usuário do banco de dados |
| `POSTGRES_PASSWORD` | Senha do banco de dados |
| `DB_HOST` | Host do banco de dados |
| `DB_PORT` | Porta do banco de dados (padrão: 5432) |
| `EMAIL_HOST_PASSWORD` | Senha de app do Gmail para envio de e-mails |

---

Desenvolvido com auxílio de IA usando [Claude Code](https://claude.ai/code)
