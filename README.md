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
| 4 | Fonte de Dados | aba `4. Fonte de Dados` (somente campos preenchidos) |
| 5 | Cenário Macroeconômico | Planilha de Indicadores Econômicos (Selic, IPCA, PIB, Câmbio, Desemprego, ICC) |
| 6 | Panorama do Segmento | Site do cliente + pesquisa do setor (Sports Analytics) |
| 7 | DRE Gerencial | aba `7.1 DRE Gerencial` — tabela do DRE + Revisão Analítica (ao lado) |
| 8 | DFC | aba `7.2 DFC` — somente a tabela do fluxo de caixa |
| 9 | Ciclo Operacional | aba `7.4 Ciclo Operacional` — tabelas + Análise Executiva + Plano de Ação (Recomendações) + demais textos da aba |
| 10 | Projeção de Caixa, 13 Semanas | aba `7.4.1 Projeção 13 Semanas` — simulador rolante: parâmetros, capital de giro mínimo (2 metodologias), grade semanal e alertas do horizonte |
| 11 | Endividamento | aba `7.5 Endividamento` — tabelas + Observações/Riscos/Recomendações (ao lado) |
| 12 | Cronograma da Dívida | aba `7.5.1 Cronograma da Dívida` — parâmetros por operação + cronograma SAC consolidado (12 meses) + nota metodológica |
| 13 | Indicadores | aba `7.6 Indicadores` — indicadores por grupo (Rentabilidade, Custos, Ponto de Equilíbrio, Caixa, Endividamento, Distribuição) |
| 14 | Benchmark | aba `7.7 Benchmark` — comparativo de mercado + recomendações |
| 15 | Ponto de Atenção | aba `7.8 Ponto de Atenção` — Pontos de Atenção + Pontos de Validação (callouts) |

> As abas 7 a 15 foram extraídas da planilha base de modelagem (`DFC_Fight`, versão mais recente
> enviada pelo cliente). Números e textos foram reproduzidos exatamente como na base (inclusive a
> formatação de células — R$, %, x — e as referências internas do tipo "4.1", "4.2", "4.6" que
> constam nas próprias abas de origem).

## Edição

- **No próprio HTML:** botão **"✎ Modo de edição"** torna textos, bullets e células das tabelas editáveis diretamente na página. Uma barra inferior permite **grifar em verde** e aplicar **negrito** na seleção.
- **No código-fonte:** os dados dos gráficos ficam no bloco `<script>` (`INDICATORS`); as tabelas das abas 7 a 15 são HTML estático, fáceis de ajustar.

## Regras aplicadas

- Somente dados presentes na planilha base — nada inventado.
- Campos vazios na base (Premissas e Metodologia) são exibidos como *"Não informado na planilha base."*
- Identidade visual O2 Inc.: logo O2 e paleta **vivid green `#6CF269`** (Pantone 802 C) + **intense gray `#494949`** (Pantone 438 C) sobre fundo branco.
