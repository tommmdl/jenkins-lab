# Validação — 17/10/2026

[English](validation.en.md)

Execução real em Docker sobre Linux/WSL. Builds iniciados às 15:45:28 e 15:45:48 no fuso America/Sao_Paulo; os logs usam UTC. Execução técnica realizada pelo assistente, com autorização do proprietário.

| Build | SIMULATE_FAILURE | Result | Duration | Artifact |
| --- | --- | --- | --- | --- |
| #1 | false | SUCCESS | 13.263 s | report.txt |
| #2 | true | FAILURE | 4.827 s | report.txt |

- Jenkins: 2.580.1
- Java: Temurin 21.0.12.1+1-LTS
- Docker Engine: 29.1.3
- Compose: 5.6.0
- workflow-aggregator: 608.v67378e9d3db_1
- workflow-cps: 4395.v738456a_5da_6b_
- workflow-job: 1609.v8926e7962024
- git plugin: 5.11.0
- timestamper: 1.30
- Base image: `jenkins/jenkins@sha256:a660310e39ade10631f774bacd5219de767dfd08947ea5c32a739b5e5bb382c1`
- Pipeline commit: `1b55f5d210dd7c00425fe7d0d8165d315e0ae5a1`

## Evidências e interpretação

- [Log completo #1](../evidence/build-1.log): checkout do GitHub, validação Bash, geração, arquivamento e limpeza; termina em SUCCESS.
- [Log completo #2](../evidence/build-2.log): mesmas etapas, com erro intencional na etapa Failure drill; termina em FAILURE.
- [Metadados da API](../evidence/results.json) e relatórios [#1](../evidence/build-1-report.txt) / [#2](../evidence/build-2-report.txt).

Ambos os artefatos foram baixados pela API autenticada. O verificador conferiu os resultados e a presença do artefato. A pasta principal do workspace não existia após a limpeza; workspaces auxiliares de SCM podem permanecer.

A API sem autenticação retornou HTTP 403. Após `compose down` e `up -d`, o login de administrador, o job e os builds #1/#2 continuaram disponíveis no volume. O container permanece em execução para exploração local.

## Limitações e aprendizado

A falha é um exercício controlado, não um incidente real ou teste de recuperação de produção. A persistência foi validada por recriação do container, sem simular perda do volume ou restauração de backup. Os builds usaram o commit inicial do Jenkinsfile; o commit que publica estas evidências acrescenta bootstrap e documentação, sem alterar o pipeline executado.

O Compose foi instalado localmente porque o plugin estava ausente e sudo exigia senha. O sandbox gerenciado bloqueava o socket Docker; os comandos foram executados com autorização fora do sandbox. O builder clássico foi usado por ausência de Buildx. Essas condições não impediram os builds.

Próximas melhorias: agentes dedicados, dependências integralmente fixadas, healthcheck, backup/restauração e uma aplicação com testes e deploy.
