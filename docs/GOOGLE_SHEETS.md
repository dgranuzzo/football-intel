# Google Sheets

## 1. Planilha

Crie uma planilha vazia no Drive, por exemplo `football-intel-warehouse`.
Copie o ID da URL:

`https://docs.google.com/spreadsheets/d/<ID>/edit`

## 2. Service account

1. Google Cloud Console → novo projeto `football-intel`.
2. Ative **Google Sheets API** e **Google Drive API**.
3. Credentials → Service account → JSON.
4. Salve o arquivo em `credentials/service_account.json` (nao commitar).
5. Compartilhe a planilha com o e-mail da service account (`...@....iam.gserviceaccount.com`) como Editor.

## 3. Variaveis

```bash
GOOGLE_SHEETS_SPREADSHEET_ID=<ID>
GOOGLE_SERVICE_ACCOUNT_JSON=credentials/service_account.json
```

## 4. GitHub Actions

Secrets do repositorio:

- `FOOTBALL_DATA_TOKEN`
- `GOOGLE_SHEETS_SPREADSHEET_ID`
- `GOOGLE_SA_JSON` (conteudo inteiro do JSON)

O workflow `daily-sync.yml` roda 08:00 BRT e republica as abas.
