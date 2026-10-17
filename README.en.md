# Jenkins Lab

English | [Português](README.md)

Local Jenkins lab with persistent storage and a versioned declarative pipeline.

**Status:** scripts checked locally; controller startup and execution inside Jenkins have not been validated yet.

## Architecture and scope

Browser → `127.0.0.1:8080` → Jenkins controller → `jenkins_home` volume.

This introductory lab runs lightweight tasks on the controller. Use dedicated agents in production. The official `jenkins/jenkins:lts-jdk21` image follows LTS updates; pin a digest after validating a version for exact reproducibility. No Docker socket mount or cloud access is required.

## Prerequisites

Running Docker Engine, Compose v2, Git, Bash and available port 8080. Initial downloads require internet. On Windows, use WSL with Docker integration configured.

## Start

Run from this repository root:

```bash
docker compose up -d
docker compose logs --tail=100 jenkins
```

Open http://localhost:8080. Retrieve the initial password **only in your terminal**:

```bash
docker compose exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Never commit the password or add it to the journal. Finish the setup wizard, install suggested plugins and create your administrator account. Confirm Pipeline, Git and Timestamper are installed under Manage Jenkins → Plugins.

## Run the pipeline

1. Create a **Pipeline** item.
2. Select **Pipeline script from SCM**, then **Git**.
3. After publication, set repository URL to `https://github.com/tommmdl/jenkins-lab.git`.
4. Use branch `*/main` and Script Path `Jenkinsfile`.
5. Select **Build Now**. After the first run, use **Build with Parameters** to enable `SIMULATE_FAILURE`.

Public repository checkout does not require a token. SCM execution requires the repository to be published first.

## Verification and learning

- Normal path: validation and report stages pass; build ends SUCCESS and archives `artifacts/report.txt`.
- `SIMULATE_FAILURE=true`: build ends FAILURE while retaining the report artifact.
- Workspace cleanup runs after archiving. Up to ten builds are retained.
- `docker compose down` followed by `up -d` should preserve the user and job in the volume.

Check the script independently:

```bash
bash -n scripts/build.sh
bash scripts/build.sh
```

Record a successful and a failed Jenkins build, reviewed logs, stage explanations and limitations. These results are still pending.

## Troubleshooting

- Docker permission denied: check daemon access and WSL integration.
- Port in use: change the host port only, retaining the `127.0.0.1` binding.
- Unknown `timestamps`: install Timestamper.
- Checkout error: verify repository publication, URL, branch and container connectivity.
- Startup failure: inspect logs; initial startup and plugin downloads may take time.

## Cleanup

```bash
docker compose down
```

The volume is preserved. **`docker compose down -v` permanently deletes this lab's jobs, users and configuration.** Run it only to discard the environment. Delete local reports manually when no longer needed.

## References

- [Official Docker installation](https://www.jenkins.io/doc/book/installing/docker/)
- [First Pipeline](https://www.jenkins.io/doc/pipeline/tour/hello-world/)
- [Portfolio](https://github.com/tommmdl/devops-portfolio)
