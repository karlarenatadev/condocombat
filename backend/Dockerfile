# =============================================================================
# Stage 1: Dependencies — instala dependências Python
# =============================================================================

FROM python:3.12-slim AS deps

WORKDIR /app

# Instala dependências de compilação
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt


# =============================================================================
# Stage 2: Runtime — imagem final
# =============================================================================

FROM python:3.12-slim AS runtime

WORKDIR /app

# Instala dependências necessárias em runtime
# curl é necessário para o HEALTHCHECK
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*


# =============================================================================
# Usuário da aplicação
# =============================================================================

RUN useradd --create-home --shell /bin/bash app


# =============================================================================
# Copia dependências instaladas
# =============================================================================

COPY --from=deps /usr/local/lib/python3.12/site-packages \
    /usr/local/lib/python3.12/site-packages

COPY --from=deps /usr/local/bin \
    /usr/local/bin


# =============================================================================
# Copia código da aplicação
# =============================================================================

COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./


# =============================================================================
# Script de inicialização
# =============================================================================

COPY entrypoint.sh .

RUN chmod +x entrypoint.sh


# =============================================================================
# Permissões
# =============================================================================

RUN chown -R app:app /app


# =============================================================================
# Executa como usuário não-root
# =============================================================================

USER app


# =============================================================================
# Configuração do serviço
# =============================================================================

EXPOSE 8000


HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1


# =============================================================================
# Inicialização
# =============================================================================

ENTRYPOINT ["./entrypoint.sh"]