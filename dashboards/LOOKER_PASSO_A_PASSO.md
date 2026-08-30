# Relatório Looker Studio — passo a passo

Não dá para gravar o `.ds` na sua conta Google daqui. Use a planilha `data/sample/looker_brasileirao_2026.xlsx` e este guia (~20 min).

1. Envie o xlsx ao Drive e abra como Planilhas Google.
2. lookerstudio.google.com → Criar → Relatório → fonte Planilhas → aba standings.
3. Adicione fontes matches, scorers e kpi.
4. Tema: fundo #0B3D2E, destaque #D4AF37, texto #F7F3E8.
5. Página 1 Visão da liga: cartões (líder, pontos, artilheiro, jogos restantes) + tabela por position + barras de points + zona.
6. Página 2 Jogos: tabelas FINISHED e SCHEDULED + AVG(goals_total).
7. Página 3 Ataque e defesa: GP vs GC, dispersão points x goal_diff, artilharia.
8. Filtros globais: competition_code e season.
9. Compartilhar → qualquer pessoa com o link.

Detalhe completo no repositório local `dashboards/LOOKER_PASSO_A_PASSO.md`.
