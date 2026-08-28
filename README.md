# Football Intel

Pipeline de estatisticas de futebol pensado para **curriculo**: coleta o Brasileirão, grava Google Sheets e alimenta um dashboard. O schema ja nasce pronto para **Libertadores** e **UEFA Champions League**.

![Python](https://img.shields.io/badge/python-3.11+-3776AB)
![Looker Studio](https://img.shields.io/badge/dashboard-Looker%20Studio-4285F4)
![Tableau](https://img.shields.io/badge/optional-Tableau%20Public-E97627)

## Por que Looker Studio (e nao so Tableau)

| Ferramenta | Custo | Ligacao com Sheets | Link publico no CV | Quando usar |
|---|---|---|---|---|
| **Looker Studio** | Gratis | Nativa | Sim, 2 cliques | Escolha padrao deste projeto |
| **Tableau Public** | Gratis | Via CSV | Sim | Se a vaga cita Tableau |
| Tableau Cloud | Pago | Conector | Depende da licenca | Empresa que ja tem Tableau |
| Power BI | Freemium | Via Excel | Limitado | Vagas Microsoft |

Recomendacao: **Looker Studio no dia a dia** + **um workbook no Tableau Public** se quiser a marca Tableau no LinkedIn. Os dois leem as mesmas abas.

## Arquitetura

```
API football-data.org ──► Python (football_intel)
                              │
                    ┌───────┼──────────┐
                    ▼         ▼          ▼
                  CSV       Sheets     briefing Grok
                    │         │
                    └────┬────┘
                         ▼
              Looker Studio / Tableau
```

- `BSA` (Brasileirão Série A) e `CL` (Champions) entram no plano **free** da [football-data.org](https://www.football-data.org/coverage).
- `CLI` (Libertadores) usa o mesmo codigo; pode exigir plano pago da API. Trocar o adapter nao muda o schema.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

cp .env.example .env
# FOOTBALL_DATA_TOKEN=  (gratis em https://www.football-data.org/client/register)
# ACTIVE_LEAGUES=BSA

python -m football_intel sync --no-sheets
```

CSV de saida: `data/warehouse/bsa_*.csv`.

Para publicar no Google Sheets siga `docs/GOOGLE_SHEETS.md` e rode sem `--no-sheets`.

Ativar Champions no mesmo warehouse:

```bash
ACTIVE_LEAGUES=BSA,CL python -m football_intel sync --no-sheets
```

## Grok bot

O acompanhamento diario (placares, G4/Z4, proxima rodada) e um prompt em `automations/grok_prompt.txt`.
O bot **nao escreve** na planilha; o Python + GitHub Action escrevem. Os dois se complementam:

| Papel | Dono |
|---|---|
| Fonte da verdade, schema, historico | `football_intel` |
| Briefing, checagem, texto para o CV | Grok Automation |

## Dashboard

1. Rode o pipeline (ou importe `data/sample/football_intel_sample.xlsx` no Drive).
2. Siga `dashboards/looker_studio.md`.
3. Publique o link no README.

Modelo de metricas em `dashboards/metrics.md`. Texto pronto para o curriculo em `docs/CURRICULO.md`.

## Estrutura

```
config/leagues.yaml          # ligar/desligar BSA, CLI, CL
src/football_intel/          # clientes + exporters + CLI
data/sample/                 # planilha e CSV de demonstracao
dashboards/                  # Looker Studio e Tableau
automations/                 # prompt do Grok bot
.github/workflows/           # sync diario 08:00 BRT
```

## Stack

Python 3.11+, httpx, pydantic, pandas, gspread, GitHub Actions, Google Sheets, Looker Studio.
