# Jenkins Lab

[English](README.en.md) | Português

Laboratório Jenkins com configuração automatizada e builds reproduzíveis.

## Executar o ambiente

Pré-requisitos: Linux/WSL, Docker Engine acessível ao usuário, Bash, Python 3, curl e porta 8080 disponível. A instalação local automática do Compose suporta Linux x86_64; em outras arquiteturas, instale o plugin oficial previamente.

```bash
bash scripts/prepare.sh
bash scripts/compose.sh up -d --build
```

O primeiro comando preserva senhas existentes e instala o Compose 5.6.0 localmente, com verificação SHA-256, somente se o plugin estiver ausente. Arquivos locais e segredos são ignorados pelo Git e excluídos do contexto Docker.

Abra http://localhost:8080. Usuário: `admin`. Consulte a senha somente no seu terminal:

```bash
cat .local/admin-password
```

O bootstrap cria o administrador e o job `jenkins-lab`; não é necessário executar o assistente de instalação. O volume preserva contas, jobs e histórico. Alterar o arquivo de senha não rotaciona uma conta já criada.

## Arquitetura

Navegador → `127.0.0.1:8080` → Jenkins → volume persistente. A imagem deriva de Jenkins LTS com Java 21 e instala Pipeline, Git e Timestamper. Um script de inicialização configura autenticação, bloqueia acesso anônimo e cria o job com SCM público e branch `main`.

Este laboratório executa tarefas leves no controller com um executor. Em produção, use agentes dedicados. Não há montagem do socket Docker ou acesso cloud. A imagem LTS e os plugins acompanham atualizações; o relatório registra as versões reais da execução, mas os arquivos de build ainda não fixam todas as dependências.

## Builds de sucesso e falha

Abra o job `jenkins-lab` e clique em **Build Now**. Depois, **Build with Parameters** permite ativar `SIMULATE_FAILURE`. O fluxo normal valida o Bash, gera um relatório e arquiva o artefato. O cenário de falha executa essas etapas e falha intencionalmente; o relatório também é preservado. O workspace é limpo após o arquivamento, e até dez builds são retidos.

Para executar e verificar os dois cenários automaticamente:

```bash
python3 scripts/verify-builds.py
```

O verificador usa autenticação e crumb CSRF, acompanha a fila e valida o resultado esperado e o artefato de cada build. Logs e metadados são salvos em `.local/evidence/`. Execute com o Jenkins ocioso: a primeira execução sem histórico usa os parâmetros padrão; execuções seguintes usam os parâmetros explícitos.

## Evidências

Veja [resultados reais](docs/validation.md) e [logs revisados](evidence/). Credenciais não fazem parte das evidências publicadas.

## Troubleshooting

- Docker permission denied: verifique acesso ao daemon e a integração WSL. Não torne o socket acessível a todos. Neste ambiente gerenciado, comandos Docker exigiram execução autorizada fora do sandbox.
- Compose ausente: execute `prepare.sh` e use o wrapper `compose.sh`.
- Porta ocupada: ajuste a porta do host e a URL no verificador, mantendo o vínculo a localhost.
- Falha de checkout: confira conectividade do container e acesso à branch `main` pública.
- Falha de startup: `bash scripts/compose.sh logs --tail=100 jenkins`.

## Limpeza

```bash
bash scripts/compose.sh down
```

Preserva o volume. **`bash scripts/compose.sh down -v` apaga permanentemente contas, jobs e histórico deste laboratório.** Só execute para descartar o ambiente. Os arquivos `.local/` permanecem locais e podem ser removidos separadamente quando não forem mais necessários.

## Referências

- [Instalação Jenkins com Docker](https://www.jenkins.io/doc/book/installing/docker/)
- [Hooks Groovy de inicialização](https://www.jenkins.io/doc/book/managing/groovy-hook-scripts/)
- [Instalação oficial do plugin Compose](https://docs.docker.com/compose/install/linux/)
- [Portfólio](https://github.com/tommmdl/devops-portfolio)
