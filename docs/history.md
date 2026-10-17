# Sobre o histórico / About the history

Em 17/10/2026, as mensagens dos commits da branch `main` foram encurtadas para facilitar a leitura. Essa etapa preservou os arquivos de cada commit, seus autores e suas datas. Depois vieram as alterações de documentação. Os backups do histórico anterior foram salvos localmente antes do force push.

Os relatórios, logs e metadados de imagens continuam mostrando os SHAs usados nas execuções originais. Eles são registros históricos e não foram alterados para aparentar novas execuções. A tabela relaciona esses commits com os commits equivalentes do histórico revisado. O pipeline passa a usar uma revisão acessível do histórico novo em `source.json`.

On 2026-10-17, commit messages on `main` were shortened for readability. This step preserved each commit's files, authors and dates; documentation edits came afterward. Local backups were saved before the force push.

Reports, logs and image metadata still show the SHAs used by their original runs. They are historical records, not rewritten test results. The table maps those commits to their equivalents in the revised history. The pipeline's `source.json` uses an accessible revision from the new history.

| SHA anterior / Previous SHA | SHA equivalente / Equivalent SHA | Mensagem / Message |
| --- | --- | --- |
| `1b55f5d210dd7c00425fe7d0d8165d315e0ae5a1` | `c7624593fa9da533a2a60449b6b1c88dd20d4670` | Cria o laboratório Jenkins e o primeiro pipeline |
| `4c1d28cad4a17577f61df1fa5011f776e04b1124` | `c835ff7eccbcab2e7297b3a10d4a446d74120786` | Configura o Jenkins e testa sucesso e falha |
