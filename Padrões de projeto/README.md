# Padrões de Projeto — Exercícios resolvidos + Material de consulta

Disciplina **Padrões de Projeto** (Prof. Escobar) — 1.º bimestre.
Este repositório contém **todos os exercícios solicitados** resolvidos e
verificados, além de **material de consulta para a prova**.

---

## Comece por aqui

| Quero… | Abra |
|---|---|
| Ver **o que foi feito** e onde está cada exercício | [`exercicios_professor/INDICE_EXERCICIOS.md`](exercicios_professor/INDICE_EXERCICIOS.md) |
| **Consultar durante a prova** (resumo de 1 página por padrão) | [`material_consulta_prova/01_CHEATSHEET_RAPIDO.md`](material_consulta_prova/01_CHEATSHEET_RAPIDO.md) |
| **Escrever um padrão do zero** (templates Java prontos) | [`material_consulta_prova/02_GUIA_PADROES_COM_TEMPLATES.md`](material_consulta_prova/02_GUIA_PADROES_COM_TEMPLATES.md) |
| **Desenhar o UML** (notação, setas, exemplos) | [`material_consulta_prova/03_REFERENCIA_UML_E_SINTAXE.md`](material_consulta_prova/03_REFERENCIA_UML_E_SINTAXE.md) |
| **Versão para imprimir / consultar offline** | [`material_consulta_prova/pdf/`](material_consulta_prova/pdf) (3 PDFs) |
| **Compilar e rodar tudo de uma vez** | `compilar_tudo.ps1` |

---

## Exercícios entregues

| # | Exercício | Padrão / Tema | Código | Status |
|---|---|---|---|---|
| 1 | Sistema de Emissão de Apólices (4 linhas de produto) | **Factory Method** | [`aula0109/exercicio1`](aula0109/exercicio1) | ✅ compila e executa |
| 2 | Checkout Internacional de Marketplace (BR / EUA / DE) | **Abstract Factory** | [`aula0109/exercicio2`](aula0109/exercicio2) | ✅ compila e executa |
| 3 | Classe `Diretor` — bonificação por nº de geridos | Herança · Polimorfismo · `abstract` | [`exemplo_funcionario`](exercicios_professor/heranca_polimorfismo/exemplo_funcionario) | ✅ compila e executa |
| 4 | Sistema de remessas Coisas & Coisas (frete) | Herança · `@Override` · `super` | [`remessas_coisas_e_coisas`](exercicios_professor/heranca_polimorfismo/remessas_coisas_e_coisas) | ✅ compila e executa |
| 5 | UniLE — disciplinas de graduação e especialização | Interface · SOLID · Polimorfismo | [`unile`](exercicios_professor/heranca_polimorfismo/unile) | ✅ compila e executa |
| 6 | Material didático da aula 18/08 (versão inicial) | Interface `IDisciplina` | [`aula1808`](aula1808) | ✅ compila e executa |

Cada exercício tem: **código-fonte comentado**, **diagrama UML em Mermaid**
(`diagrama.md`) e **saída de execução registrada** em `_build/saida_*.txt`.

---

## Compilar e executar

Requer o **JDK** instalado (o script localiza sozinho via `JAVA_HOME`, `PATH` ou
`C:\Program Files\Java`).

```powershell
pwsh -File .\compilar_tudo.ps1
```

Saída esperada: `TODOS OS EXERCICIOS COMPILARAM E EXECUTARAM COM SUCESSO.`

Os `.class` vão para `_build/<exercicio>/` — nada de artefato solto nas pastas de
código. Para gerar novamente os PDFs do material de consulta:

```powershell
pwsh -File .\gerar_pdf_material.ps1
```

---

## Estrutura do repositório

```
Padrões de projeto/
├── README.md                       <- este arquivo
├── compilar_tudo.ps1               <- compila e executa os 6 exercícios
├── gerar_pdf_material.ps1          <- .md -> .html -> .pdf do material
├── .gitignore                      <- ignora *.class e _build/
│
├── conteudos/                      <- material do professor (docx/pptx/txt)
│   ├── _Exercicios_Design_Patterns_Java.docx
│   ├── Padrões de Projetos - Aula 01(v2).pptx
│   ├── Padrões de Projetos - Herança, Polimorfismo e Method.pptx
│   └── instrucoes_avaliacao.txt
│
├── aula0109/                       <- aula 01/09 — Factory Method e Abstract Factory
│   ├── atividade.txt
│   ├── exercicio1/                 <- Exercício 1 (apólices) + diagrama.md
│   └── exercicio2/                 <- Exercício 2 (checkout)  + diagrama.md
│
├── aula1108/                       <- aula 11/08 — herança/polimorfismo (original)
│   └── diretor.java                <- atividade dos slides (nova)
│
├── aula1808/                       <- aula 18/08 — UniLE (versão inicial)
│
├── exercicios_professor/           <- exercícios das aulas herança/polimorfismo
│   ├── INDICE_EXERCICIOS.md        <- índice detalhado com critérios de avaliação
│   └── heranca_polimorfismo/
│       ├── exemplo_funcionario/         <- Ex. 3 (Diretor)      + diagrama.md
│       ├── remessas_coisas_e_coisas/    <- Ex. 4 (frete)        + diagrama.md
│       └── unile/                       <- Ex. 5 (disciplinas)  + diagrama.md
│
├── material_consulta_prova/        <- MATERIAL PARA A PROVA
│   ├── 01_CHEATSHEET_RAPIDO.md
│   ├── 02_GUIA_PADROES_COM_TEMPLATES.md
│   ├── 03_REFERENCIA_UML_E_SINTAXE.md
│   └── pdf/                        <- os mesmos 3 documentos em HTML e PDF
│
├── _extracted_text/                <- texto extraído do docx/pptx (apoio)
└── _build/                         <- classes compiladas e saídas (ignorado no Git)
```

---

## Leituras dos arquivos originais do professor

- `conteudos/_Exercicios_Design_Patterns_Java.docx` → Exercícios 1 e 2.
- `conteudos/Padrões de Projetos - Aula 01(v2).pptx` → ementa, SOLID, dicas de sala.
- `conteudos/Padrões de Projetos - Herança, Polimorfismo e Method.pptx` →
  herança, polimorfismo, classes/métodos abstratos, interfaces, Factory Method,
  Abstract Factory, Observer, Decorator — e as **três atividades** (Diretor,
  Coisas & Coisas, UniLE).
  Os arquivos `...(1).pptx` e `...(2).pptx` são **cópias idênticas** (mesmo MD5).
- `conteudos/instrucoes_avaliacao.txt` → regras da prova (a seguir).

## Regras da avaliação (do enunciado do professor)

- Turma 1: 19h00–20h00 · Turma 2: 20h15–21h15.
- Mesas voltadas para o fundo da sala; iniciar um **projeto Java no VS Code**.
- **Sem IA** na prova · **internet desativada** · **Wi-Fi do notebook desligado**.
- Similaridade acima de **85%** = cópia = nota zero.
- Entrega **exclusivamente pelo Git**; pedir ao professor para religar a internet.
