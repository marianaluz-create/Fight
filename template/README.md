# Modelo reaproveitável — Diagnóstico Econômico Financeiro (O2 Inc.)

Motor genérico extraído do diagnóstico da Fight Analytics, para reaproveitar
em qualquer outro cliente.

- **`PLAYBOOK.md`** — leia primeiro. Regras, estrutura das 15 abas e passo a
  passo completo.
- **`common.py`** — biblioteca Python (formatação de números/tabelas no
  estilo do design system O2, detecção de abas-fonte pela cor).
- **`shell.html`** — a "casca" HTML/CSS/JS completa (marca O2, senha, modo de
  edição, autosave/exportação, motor do simulador de caixa), já genérica,
  com placeholders `{{CLIENT_NAME}}`, `{{SENHA}}`, `{{NAV_BUTTONS}}`,
  `{{NAV_PANES}}`, `{{SIM_CUM_RECV}}`, `{{SIM_CUM_PAY}}`, `{{SIM_D21}}`,
  `{{SIM_F21}}`.
- **`build.py`** — esqueleto de script para o próximo cliente: copie,
  preencha as seções marcadas "PREENCHER" com os dados do cliente e rode.

Este motor foi conferido gerando de volta, byte a byte, o HTML da Fight
Analytics a partir do `shell.html` + dos mesmos dados — ou seja, não é uma
proposta teórica, é o mesmo código que já está em produção, só reorganizado
para reaproveitar.
