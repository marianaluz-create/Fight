# Diagnóstico Econômico Financeiro — Fight Analytics

HTML interativo do Diagnóstico Econômico Financeiro da **Fight Analytics**, gerado a
partir da planilha base de modelagem (`DFC_Fight.xlsx`, abas 1 a 6) e da Planilha de
Indicadores Econômicos.

## Arquivo

- **`diagnostico-fight-analytics.html`** — documento completo e autocontido (abrir em qualquer navegador).

## Acesso

O documento é protegido por senha. A senha segue a regra **Nome do Cliente + Ano Corrente da análise**:

```
Fight Analytics2026
```

## Abas (conforme a planilha base)

| # | Aba | Origem dos dados |
|---|-----|------------------|
| 1 | Capa | Nome do cliente e Data da Apresentação (aba `1. Capa`) |
| 2 | Sumário | Modelo de Sumário |
| 3 | Disclaimer | Modelo de Disclaimer |
| 4 | Fonte de Dados · Premissas · Metodologia | aba `4. Fonte de Dados` (somente campos preenchidos) |
| 5 | Cenário Macroeconômico | Planilha de Indicadores Econômicos (Selic, IPCA, PIB, Câmbio, Desemprego, ICC) |
| 6 | Panorama do Segmento | Site do cliente + pesquisa do setor (Sports Analytics) |

## Edição

- **No próprio HTML:** botão **"✎ Modo de edição"** torna os textos editáveis diretamente na página.
- **No código-fonte:** os dados dos gráficos ficam no bloco `<script>` (`INDICATORS`), fáceis de ajustar.

## Regras aplicadas

- Somente dados presentes na planilha base — nada inventado.
- Campos vazios na base (Premissas e Metodologia) são exibidos como *"Não informado na planilha base."*
- Paleta: fundo branco, verde e preto.
