# Arquitetura

```
football-data.org          Grok Automation (briefing diario)
        \                       /
         \                     /
          v                   v
     football_intel (Python)
        |     |     |
       CSV  SQLite  Google Sheets
                      |
                      +-- Looker Studio  (recomendado para o curriculo)
                      +-- Tableau Public (opcional, marca Tableau)
```

## Por que esse desenho

- **Uma liga por adapter, um schema so.** Adicionar Libertadores ou Champions e ligar `enabled: true` em `config/leagues.yaml` e incluir o codigo em `ACTIVE_LEAGUES`.
- **Google Sheets e o contrato.** Looker Studio e Tableau leem as mesmas abas.
- **CSV no Git** serve de backup e de evidencia no repositorio.
- **Grok bot** nao substitui o ETL: ele acompanha rodada, valida outliers e escreve o briefing. O Python e a fonte da verdade.

## Tabelas (schema)

| Aba            | Grain                         | Chave              |
|----------------|-------------------------------|--------------------|
| matches        | 1 linha por jogo              | match_id           |
| standings      | 1 linha por clube na tabela   | competition + team |
| scorers        | 1 linha por jogador           | player_id          |
| teams          | 1 linha por clube             | team_id            |
| competitions   | 1 linha por liga ativa        | competition_code   |
| pipeline_runs  | 1 linha por execucao          | run_at             |

Campos de `matches` ja nascem prontos para filtro de liga: `competition_code` (`BSA`, `CLI`, `CL`).

## Extensao para outra liga

1. Confirme o codigo em [football-data.org lookup](https://docs.football-data.org/general/v4/lookup_tables.html) (`CLI`, `CL`, `EL`...).
2. Ative em `config/leagues.yaml`.
3. `ACTIVE_LEAGUES=BSA,CL python -m football_intel sync`.
4. No Looker Studio, o filtro `competition_code` passa a ter a nova liga. Nao precisa recortar o modelo.

Se a liga nao estiver no plano free, implemente outro cliente em `src/football_intel/clients/` herdando `StatsClient` e devolvendo o mesmo `Snapshot`.
