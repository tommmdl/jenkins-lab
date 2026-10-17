# Jenkins Lab

[English](README.en.md) | Português

Laboratório local de Jenkins com persistência e pipeline declarativo versionado.

**Status:** scripts verificados localmente; execução do controller e do pipeline Jenkins ainda não validada.

## Arquitetura e escopo

Navegador → `127.0.0.1:8080` → controller Jenkins → volume `jenkins_home`.

Este primeiro exercício executa tarefas leves no controller para simplificar o ambiente local. Em produção, utilize agentes dedicados. A imagem oficial `jenkins/jenkins:lts-jdk21` acompanha atualizações LTS; fixe um digest após validar uma versão para obter reprodução exata. Sem Docker socket montado e sem acesso cloud.

## Pré-requisitos

Docker Engine em execução, Compose v2, Git, Bash e porta 8080 disponível. O primeiro download exige internet. No Windows, use WSL com integração Docker configurada.

## Subir o ambiente

Execute da raiz deste repositório:

```bash
docker compose up -d
docker compose logs --tail=100 jenkins
```

Abra http://localhost:8080 e obtenha a senha inicial **somente no seu terminal**:

```bash
docker compose exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Não salve essa senha no Git ou no diário. Complete o assistente, instale os plugins sugeridos e crie seu administrador. Confirme os plugins Pipeline, Git e Timestamper; instale os ausentes em Manage Jenkins → Plugins.

## Executar o pipeline

1. Crie um item do tipo **Pipeline**.
2. Em Definition, escolha **Pipeline script from SCM**, SCM **Git**.
3. Informe a URL pública deste repositório após a publicação: `https://github.com/tommmdl/jenkins-lab.git`.
4. Use a branch `*/main` e Script Path `Jenkinsfile`.
5. Execute **Build Now**. Após a primeira execução, use **Build with Parameters** para marcar `SIMULATE_FAILURE`.

O checkout de um repositório público não requer token. Antes de publicar, é possível testar criando um item com Pipeline script e colando o Jenkinsfile, mas nesse caso é necessário disponibilizar também `scripts/build.sh` no workspace; prefira validar via SCM após a publicação.

## Verificação e aprendizado

- Fluxo normal: etapas de validação e relatório passam; o build termina SUCCESS e arquiva `artifacts/report.txt`.
- `SIMULATE_FAILURE=true`: o build termina FAILURE e preserva o relatório como artefato.
- O workspace é limpo depois do arquivamento; o histórico retém até dez builds.
- `docker compose down` seguido de `up -d` deve preservar o usuário e o job no volume.

Valide o script independentemente do Jenkins:

```bash
bash -n scripts/build.sh
bash scripts/build.sh
```

Registre no diário um build de sucesso e um de falha, com logs revisados, explicação das etapas e limitações. Esses resultados ainda estão pendentes.

## Troubleshooting

- Permission denied ao acessar Docker: confirme acesso do usuário ao daemon e a integração WSL.
- Porta ocupada: altere apenas a porta do host no Compose, mantendo o vínculo a `127.0.0.1`.
- `timestamps` desconhecido: instale Timestamper.
- Falha de checkout: confirme publicação, URL, branch e conectividade do container.
- Falha de inicialização: consulte os logs; o primeiro boot e download de plugins podem demorar.

## Limpeza

```bash
docker compose down
```

Isso preserva o volume. **`docker compose down -v` apaga permanentemente jobs, usuários e configurações deste laboratório.** Execute apenas quando quiser descartar o ambiente. Remova relatórios locais manualmente quando não forem mais necessários.

## Referências

- [Instalação oficial com Docker](https://www.jenkins.io/doc/book/installing/docker/)
- [Primeiro Pipeline](https://www.jenkins.io/doc/pipeline/tour/hello-world/)
- [Portfólio](https://github.com/tommmdl/devops-portfolio)
