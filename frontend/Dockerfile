# =============================================================================
# Stage 1: Dependencies — instala dependências
# =============================================================================
FROM node:20-alpine AS deps

WORKDIR /app

# Copia apenas os arquivos de dependências
COPY package.json package-lock.json ./

# Instala dependências conforme o lockfile
RUN npm ci

# =============================================================================
# Stage 2: Builder — compila a aplicação
# =============================================================================
FROM node:20-alpine AS builder

WORKDIR /app

# Copia dependências instaladas
COPY --from=deps /app/node_modules ./node_modules

# Copia o restante do projeto
COPY . .

# Gera o build de produção
RUN npm run build

# =============================================================================
# Stage 3: Runner — imagem final
# =============================================================================
FROM node:20-alpine AS runner

WORKDIR /app

# Define ambiente de produção
ENV NODE_ENV=production
ENV PORT=3000

# Instala apenas o necessário para o healthcheck
RUN apk add --no-cache curl

# Cria usuário não-root
RUN addgroup -S nodejs && \
    adduser -S nextjs -G nodejs

# Copia os arquivos necessários para execução
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Troca para usuário não-root
USER nextjs

# Expõe a porta da aplicação
EXPOSE 3000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

# Inicializa o servidor
CMD ["node", "server.js"]