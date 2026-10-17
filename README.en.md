# Jenkins: from the first pipeline to a failed build

English · [Português](README.md)

What happens between clicking **Build Now** and getting a result? This lab is a place to follow that path: watch the stages run, find an error in the logs and see what remains after a build.

The environment starts with a ready-to-use job. A parameter introduces a deliberate failure, making it easier to compare both runs without changing the code.

## Getting started

Linux/WSL, Docker, Bash, Python 3, curl and an available port 8080. The preparation script can install Compose locally on Linux x86_64.

From the repository root:

```bash
bash scripts/prepare.sh
bash scripts/compose.sh up -d --build
```

Open http://localhost:8080. The username is `admin`; read the password in your terminal with `cat .local/admin-password`. It stays out of Git.

## Things to try

1. Run the `jenkins-lab` job and follow its stages.
2. Enable `SIMULATE_FAILURE` on the next run.
3. Compare the logs and download the report archived by each build.
4. Recreate the container and check that the job and history are still there.

## What has been tested

The initial builds finished with SUCCESS and FAILURE as expected. Both retained their report, and the history survived container recreation.

The [results and their limits](docs/validation.en.md) include execution details and evidence. They refer to the revisions recorded in those reports.

## When you are done

```bash
bash scripts/compose.sh down
```

This keeps the volume. Adding `-v` deletes accounts, jobs and history. Tasks run on the controller to keep this exercise simple; a production environment needs dedicated agents.

## A closer look

The [usage guide](docs/guide.en.md) covers architecture, configuration, tests, limitations and troubleshooting. The [portfolio](https://github.com/tommmdl/devops-portfolio) connects this project to the other labs.

[About the history update](docs/history.md)
