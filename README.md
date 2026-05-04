# project-start-react

Template React pronto para produção com CI/CD, Docker e qualidade de código configurados.

## Stack

- **React 18** + React Router v6
- **Styled Components** para estilização
- **ESLint** (Airbnb) + **Prettier** para qualidade de código
- **Husky** + **lint-staged** para pre-commit automático
- **Docker** (dev + prod com nginx)
- **GitHub Actions** para CI/CD

## Pré-requisitos

- Node 20+ (use `nvm use` se tiver o nvm instalado)
- Yarn
- Docker (opcional)

## Começando

```bash
# 1. Instalar dependências (também instala os hooks do husky)
yarn install

# 2. Copiar variáveis de ambiente
cp .env.example .env

# 3. Rodar em desenvolvimento
yarn start
```

## Scripts

| Comando | Descrição |
|---|---|
| `yarn start` | Sobe o servidor de desenvolvimento |
| `yarn build` | Gera o build de produção |
| `yarn test` | Roda os testes em modo watch |
| `yarn test:ci` | Roda os testes com coverage (para CI) |
| `yarn lint` | Verifica erros de lint |
| `yarn lint:fix` | Corrige erros de lint automaticamente |
| `yarn format` | Formata o código com Prettier |
| `yarn format:check` | Verifica formatação (para CI) |

## Docker

```bash
# Desenvolvimento (hot reload)
docker compose --profile dev up

# Produção (nginx)
docker compose --profile prod up
```

## CI/CD

O pipeline roda automaticamente via GitHub Actions:

- **CI** (`ci.yml`): em push para `main` e `dev`, e em PRs para `main`
  - Lint + format check
  - Testes com coverage
  - Build
  - Build da imagem Docker (apenas na `main`)

- **CD** (`cd.yml`): em push para `main` ou em tags `v*`
  - Faz build e push da imagem para o Docker Hub

### Secrets necessários no repositório

| Secret | Descrição |
|---|---|
| `DOCKER_USERNAME` | Usuário do Docker Hub |
| `DOCKER_TOKEN` | Access token do Docker Hub |

## Fluxo de branches

```
feature/* → dev → main (release)
```

- Crie sua feature a partir de `dev`
- Abra PR de `feature/*` → `dev`
- Quando pronto para release, abra PR de `dev` → `main`

## Estrutura

```
src/
├── pages/          # Páginas da aplicação
│   ├── Main/
│   └── Repository/
├── styles/         # Estilos globais
├── App.js
├── index.js
└── routes.js
```
