# Jenkins Lab

English | [Português](README.md)

Jenkins lab with automated configuration and reproducible builds.

## Run the environment

Prerequisites: Linux/WSL, Docker Engine accessible to your user, Bash, Python 3, curl and available port 8080. Automatic local Compose installation supports Linux x86_64; install the official plugin beforehand on other architectures.

```bash
bash scripts/prepare.sh
bash scripts/compose.sh up -d --build
```

Preparation preserves existing passwords and installs Compose 5.6.0 locally with SHA-256 verification only when the plugin is missing. Local files and secrets are ignored by Git and excluded from the Docker build context.

Open http://localhost:8080. Username: `admin`. Read the password only in your terminal:

```bash
cat .local/admin-password
```

Bootstrap creates the administrator and `jenkins-lab` job, replacing the interactive setup wizard. The volume preserves accounts, jobs and history. Changing the password file does not rotate an existing account.

## Architecture

Browser → `127.0.0.1:8080` → Jenkins → persistent volume. The image derives from Jenkins LTS with Java 21 and installs Pipeline, Git and Timestamper. An initialization hook enables authentication, denies anonymous access and creates a job using public SCM on branch `main`.

This lab runs lightweight tasks on the controller with one executor. Use dedicated agents in production. No Docker socket mount or cloud access. The LTS image and plugins follow updates; the validation report records actual versions, but build dependencies are not all pinned yet.

## Success and failure builds

Open `jenkins-lab` and select **Build Now**. Afterward, **Build with Parameters** exposes `SIMULATE_FAILURE`. The normal path validates Bash, generates a report and archives it. The failure drill performs those steps and deliberately fails while preserving the report. Workspace cleanup follows archiving; up to ten builds are retained.

Run both scenarios automatically:

```bash
python3 scripts/verify-builds.py
```

The verifier uses authentication and a CSRF crumb, follows the queue and asserts both expected results and archived artifacts. Logs and metadata are saved under `.local/evidence/`. Run while Jenkins is idle: a first build without history uses defaults; subsequent builds pass explicit parameters.

## Evidence

See [actual results](docs/validation.en.md) and [reviewed logs](evidence/). Published evidence excludes credentials.

## Troubleshooting

- Docker permission denied: check daemon access and WSL integration. Do not make the socket world-accessible. This managed environment required authorized Docker commands outside the sandbox.
- Compose missing: run `prepare.sh`, then use `compose.sh`.
- Port busy: update the host port and verifier URL, preserving localhost binding.
- Checkout failure: verify container connectivity and public `main` branch access.
- Startup failure: `bash scripts/compose.sh logs --tail=100 jenkins`.

## Cleanup

```bash
bash scripts/compose.sh down
```

Preserves the volume. **`bash scripts/compose.sh down -v` permanently deletes lab accounts, jobs and history.** Use only to discard the environment. Local `.local/` files remain and can be removed separately when no longer needed.

## References

- [Jenkins Docker installation](https://www.jenkins.io/doc/book/installing/docker/)
- [Groovy initialization hooks](https://www.jenkins.io/doc/book/managing/groovy-hook-scripts/)
- [Official Compose plugin installation](https://docs.docker.com/compose/install/linux/)
- [Portfolio](https://github.com/tommmdl/devops-portfolio)
