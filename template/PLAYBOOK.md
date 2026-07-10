# Playbook — Diagnóstico Econômico Financeiro (O2 Inc.)

Este documento descreve o **padrão** usado para montar o Diagnóstico Econômico
Financeiro em HTML (o modelo construído para a Fight Analytics) e como repetir
o processo para qualquer outro cliente da O2. O objetivo é que o próximo
diagnóstico saia em horas, não em dias — e que a identidade visual, as regras
de negócio e o comportamento (senha, edição, simulador) sejam sempre os
mesmos, independente do cliente.

## 1. Como identificar as abas certas na planilha do cliente

**Regra (definida pela O2): as abas que entram no diagnóstico são sempre as
abas com cor de aba (tab color) preenchida na planilha.** Abas de apoio,
rascunho ou cálculo auxiliar (ex.: `Base`, `Apoio`, `Histórico da empresa`)
ficam sem cor e nunca entram no HTML.

No arquivo da Fight Analytics, todas as abas do relatório (`1. Capa` até
`7.8 Ponto de Atenção`) estão pintadas com o **verde de marca da O2**
(`#6CF269` / RGB `FF6CF269`). Use `common.colored_sheets(wb)` para listar
automaticamente as abas coloridas de qualquer planilha nova — é o primeiro
comando a rodar antes de mapear qualquer célula:

```python
import openpyxl
from common import colored_sheets
wb = openpyxl.load_workbook("planilha_do_cliente.xlsx", data_only=True)
for nome, cor in colored_sheets(wb):
    print(nome, cor)
```

⚠️ **Atenção a exceções**: no arquivo da Fight Analytics, duas abas usadas no
diagnóstico ficaram **sem cor** por esquecimento (`7.4.1 Projeção 13 Semanas`
e `Relação de Endividamento`). Sempre confira manualmente se alguma aba usada
no relatório final não está pintada — e avise o cliente para colorir todas as
abas-fonte da próxima vez, para a regra ficar 100% confiável.

## 2. Estrutura fixa do documento (15 abas)

| # | Aba do HTML | Tipo de conteúdo | Fonte típica |
|---|---|---|---|
| 1 | Capa | Narrativa/institucional | Nome do cliente, data |
| 2 | Sumário | Narrativa | Fixo (modelo de sumário) |
| 3 | Disclaimer | Narrativa | Fixo (modelo de disclaimer) |
| 4 | Fonte de Dados | Estruturada | Aba "Fonte de Dados" |
| 5 | Cenário Macroeconômico | Dados externos | Indicadores econômicos (Selic, IPCA, PIB, Câmbio, Desemprego, ICC) |
| 6 | Panorama do Segmento | Narrativa/pesquisa | Site do cliente + pesquisa de setor |
| 7 | DRE Gerencial | Tabular + análise | Aba "DRE Gerencial" |
| 8 | DFC | Tabular + análise | Aba "DFC" |
| 9 | Ciclo Operacional | Tabular + análise | Aba "Ciclo Operacional" |
| 10 | Projeção de Caixa, 13 Semanas | **Simulador interativo** | Aba "Projeção 13 Semanas" + aba transacional "Base" |
| 11 | Endividamento | Tabular + análise | Aba "Endividamento" |
| 12 | Cronograma da Dívida | Tabular | Aba "Cronograma da Dívida" |
| 13 | Indicadores | Tabular | Aba "Indicadores" |
| 14 | Benchmark | Tabular + análise | Aba "Benchmark" |
| 15 | Ponto de Atenção | Callouts | Aba "Ponto de Atenção" |

**Importante**: as abas 1–6 são majoritariamente **narrativas** (texto livre,
pesquisa externa, dados institucionais) — normalmente não vêm de uma tabela
estruturada e por isso continuam sendo escritas à mão (ou com ajuda do
Claude), seguindo o mesmo visual das demais. As abas 7–15 são as
**financeiras**, extraídas mecanicamente de tabelas da planilha — são essas
que o motor (`common.py` + `build.py`) automatiza de fato.

## 3. Regras de negócio (não mudam de cliente para cliente)

- **Nada inventado**: todo número e todo texto vem da planilha base. Campo
  vazio na planilha → mostrar *"Não informado na planilha base."*, nunca
  preencher com estimativa própria.
- **Benchmark de mercado só em índices/percentuais**, nunca em valores
  absolutos em R$ (não existe "benchmark de mercado" para um faturamento
  absoluto — depende do porte da empresa). Se a planilha já traz essa
  distinção (célula com "—" para linhas absolutas), respeite — é
  intencional, não uma lacuna.
- **Senha de acesso** = Nome do Cliente + Ano corrente da análise, sem
  espaço (ex.: `Fight Analytics2026`).
- **Paleta O2**: vivid green `#6CF269` (Pantone 802 C) + intense gray
  `#494949` (Pantone 438 C) sobre fundo branco. Não muda por cliente — é a
  marca da O2, não a do cliente.
- **Documento editável**: modo de edição (grifar/negrito), autosave em
  `localStorage`, botão de exportar HTML editado — sempre presentes, sempre
  do mesmo jeito (já vêm prontos no `shell.html`, nada a refazer).

## 4. Como montar um diagnóstico novo, passo a passo

1. Peça a planilha do cliente e rode `colored_sheets(wb)` (seção 1) para
   confirmar as abas-fonte.
2. Copie `build.py` para o projeto do novo cliente e preencha o topo
   (`CLIENT_NAME`, `YEAR`, `XLSX_PATH`).
3. Para cada aba colorida, escreva o bloco de extração usando as funções de
   `common.py` (`table`, `table_h`, `sheet_rows`, `ul_cur`, `fmt`, etc.) e
   registre com `pb.add(id, número, título, corpo_html)`. Use o `gen.py`
   original da Fight Analytics como referência de "como ficou" para cada
   tipo de aba (DRE, DFC, indicadores, endividamento, etc.) — a estrutura
   visual é a mesma, só os números/rótulos mudam.
4. **Simulador (aba 10)** — precisa de um passo extra: os números
   `CUM_RECV`, `CUM_PAY`, `D21`, `F21` do motor JS não vêm de uma célula
   direta, são a **agregação semanal reversa-cumulativa** dos lançamentos da
   aba transacional `Base` do cliente (equivalente ao `SUMIFS`/`SUMPRODUCT`
   da planilha original). Isso precisa ser recalculado para a base do novo
   cliente — não existe hoje uma função pronta em `common.py` para isso
   (foi feito manualmente para a Fight Analytics); ao repetir para um novo
   cliente, escreva esse cálculo a partir da aba `Base` dele e injete o
   resultado nos placeholders `{{SIM_CUM_RECV}}` / `{{SIM_CUM_PAY}}` /
   `{{SIM_D21}}` / `{{SIM_F21}}` do `shell.html`.
5. Rode `build.py` — ele monta o HTML final substituindo os placeholders do
   `shell.html` pelo conteúdo gerado.
6. Abra o HTML final e confira visualmente (senha, todas as abas, o
   simulador recalculando ao editar um campo).
7. Publique (ver seção 6) e entregue o link ao cliente.

## 5. Convenções visuais de destaque (usar sempre os mesmos critérios)

- **Verde carregado (`.keyrow`)**: subtotais e a linha de Receita Bruta nas
  tabelas financeiras (`table(..., green_key=True)`), ou linhas específicas
  passadas em `key_labels`.
- **Verde claro (`.hlrow`)**: linhas que o próprio cliente destacou
  manualmente no HTML (via "Grifar verde" no modo de edição) e que devem
  permanecer marcadas depois — vira permanente só quando o cliente confirma
  a intenção (não assuma automaticamente).
- **Vermelho (`.riskrow` / `.riskcell`)**: linhas de risco/alerta (ex.: saldo
  projetado negativo no simulador).
- **`«texto»` nos bullets escritos à mão** (`ul_cur`): tudo entre aspas
  angulares vira grifo verde — é a marcação usada nos textos de análise
  (Revisão Analítica, Leitura e Recomendações, Observações, Pontos de
  Atenção).

## 6. Onde publicar o link para o cliente

Duas opções manuais testadas e funcionando, sem precisar de login por parte
do cliente:

- **Netlify Drop** (`app.netlify.com/drop`) — arrasta os arquivos, gera link
  na hora. Mais simples.
- **Vercel** (`vercel.com/new` → "Continue with GitHub", importando o
  repositório) — se o HTML já estiver no GitHub.

(A tentativa de publicar via ferramenta automatizada de IA neste projeto foi
bloqueada por política de permissão do ambiente para chamadas muito grandes —
por isso o caminho manual acima é o recomendado por enquanto.)

## 7. O que ainda não está automatizado (de propósito)

- **Abas 1–6** (narrativas/institucionais) continuam sendo escritas à mão
  por cliente — cada empresa tem uma história, um site, um setor diferentes.
- **Mapeamento de células por aba** (linhas 7–15): a posição exata de cada
  número na planilha do próximo cliente vai variar, mesmo que o "tipo" da
  aba (DRE, DFC...) seja o mesmo. `common.py` automatiza a formatação e o
  HTML; o mapeamento linha↔célula é sempre um passo de revisão humana (ou
  assistida por IA) por cliente.
- **Base histórica do simulador** (seção 4, passo 4) — cálculo específico
  por cliente, ainda não generalizado em código.
