# Como usar no curriculo

## Uma linha

Pipeline em Python que coleta o Brasileirao via API, normaliza o schema para multiplas ligas (Libertadores / Champions), grava Google Sheets e alimenta dashboard no Looker Studio, com GitHub Actions diario e briefing automatico via Grok.

## Bullet points

- Modelei um warehouse estrela (`matches`, `standings`, `scorers`) reutilizavel entre ligas.
- Automatizei ingestao (API + GitHub Actions) e publicacao no Google Sheets.
- Construí dashboard com KPIs de classificacao, calendario e artilharia.
- Separei coleta (Python) de acompanhamento (agente Grok) para nao misturar ETL com narrativa.

## Como um recrutador valida em 3 minutos

1. README com diagrama e link do dashboard publico.
2. `config/leagues.yaml` mostrando BSA ativo e CLI/CL prontos.
3. Action verde no GitHub.
4. Planilha com `pipeline_runs` recente.
