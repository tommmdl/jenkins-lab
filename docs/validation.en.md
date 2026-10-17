# Validation — 2026-10-17

[Português](validation.md)

Actual Docker execution on Linux/WSL. Builds started at 15:45:28 and 15:45:48 America/Sao_Paulo; console timestamps use UTC. Technical execution performed by the assistant with owner authorization.

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

## Evidence and interpretation

- [Full log #1](../evidence/build-1.log): GitHub checkout, Bash validation, report generation, archiving and cleanup; ends SUCCESS.
- [Full log #2](../evidence/build-2.log): same steps with a deliberate error in Failure drill; ends FAILURE.
- [API metadata](../evidence/results.json) and reports [#1](../evidence/build-1-report.txt) / [#2](../evidence/build-2-report.txt).

Both artifacts were downloaded through the authenticated API. The verifier asserted results and artifact presence. The main pipeline workspace directory was absent after cleanup; auxiliary SCM workspaces may remain.

Anonymous API access returned HTTP 403. After `compose down` and `up -d`, administrator authentication, job and builds #1/#2 remained available in the volume. The container is left running for local exploration.

## Limitations and learning

The failure is a controlled exercise, not a real incident or production recovery test. Persistence was checked by container recreation, without simulating volume loss or restoring a backup. Builds used the initial Jenkinsfile commit; the evidence publication commit adds bootstrap and documentation without changing the executed pipeline.

Compose was installed locally because the plugin was absent and sudo required a password. The managed sandbox blocked the Docker socket; authorized commands ran outside the sandbox. The classic builder was used because Buildx was absent. These conditions did not prevent the builds.

Next improvements: dedicated agents, fully pinned dependencies, healthcheck, backup/restore and an application with tests and deployment.
