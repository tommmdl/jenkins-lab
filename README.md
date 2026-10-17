# Jenkins: do primeiro pipeline ao build quebrado

[English](README.en.md) · Português

O que acontece entre clicar em **Build Now** e receber o resultado? Este laboratório é um lugar para acompanhar esse caminho com calma: ver as etapas rodarem, encontrar um erro nos logs e entender o que fica salvo depois do build.

O ambiente sobe com um job pronto. Um parâmetro permite provocar uma falha, então dá para comparar as duas execuções sem precisar quebrar o código.

## Para começar

Linux/WSL, Docker, Bash, Python 3, curl e porta 8080 livre. O script instala o Compose localmente quando necessário em Linux x86_64.

Na raiz deste repositório:

```bash
bash scripts/prepare.sh
bash scripts/compose.sh up -d --build
```

Abra http://localhost:8080. O usuário é `admin`; veja a senha no seu terminal com `cat .local/admin-password`. Ela fica fora do Git.

## Experimente

1. Rode o job `jenkins-lab` e acompanhe as etapas.
2. Na próxima execução, marque `SIMULATE_FAILURE`.
3. Compare os logs e baixe o relatório arquivado nos dois builds.
4. Recrie o container e confira se o job e o histórico continuam lá.

## O que já foi testado

Os builds iniciais terminaram em SUCCESS e FAILURE, como esperado. O relatório foi preservado nos dois casos, e o histórico sobreviveu à recriação do container.

Os [resultados e seus limites](docs/validation.md) estão registrados com os comandos e evidências da execução. Eles se referem às revisões indicadas nos relatórios.

## Quando terminar

```bash
bash scripts/compose.sh down
```

O comando preserva o volume. Adicionar `-v` apaga contas, jobs e histórico. Aqui as tarefas rodam no controller para simplificar o exercício; um ambiente de produção pede agentes dedicados.

## Para ir além

O [guia de uso](docs/guide.md) reúne arquitetura, configuração, testes, limitações e ajuda para investigar problemas. O [portfólio](https://github.com/tommmdl/devops-portfolio) conecta este projeto aos outros laboratórios.

[Sobre a revisão do histórico](docs/history.md)
