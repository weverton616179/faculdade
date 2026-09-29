# ÍNDICE — Exercícios de Padrões de Projeto (Java)

Mapa de **todos** os exercícios solicitados pelo professor, com o local do código,
o padrão aplicado e o status de verificação.

**Legenda de status:** ✅ compila e executa (saída conferida) · 📄 diagrama UML incluído

---

## Visão geral

| # | Exercício | Padrão / Tema | Pasta | Status | Saída verificada |
|---|---|---|---|---|---|
| 1 | Sistema de Emissão de Apólices | **Factory Method** | [`aula0109/exercicio1`](../aula0109/exercicio1) | ✅ 📄 | [`_build/saida_ex1...txt`](../_build/saida_ex1_apolices_factory_method.txt) |
| 2 | Checkout Internacional de Marketplace | **Abstract Factory** | [`aula0109/exercicio2`](../aula0109/exercicio2) | ✅ 📄 | [`_build/saida_ex2...txt`](../_build/saida_ex2_checkout_abstract_factory.txt) |
| 3 | Classe `Diretor` (bonificação) | Herança / Polimorfismo / `abstract` | [`exemplo_funcionario`](heranca_polimorfismo/exemplo_funcionario) | ✅ 📄 | [`_build/saida_ex3...txt`](../_build/saida_ex3_funcionario_diretor.txt) |
| 4 | Remessas Coisas & Coisas (frete) | Herança / Polimorfismo / `@Override` | [`remessas_coisas_e_coisas`](heranca_polimorfismo/remessas_coisas_e_coisas) | ✅ 📄 | [`_build/saida_ex4...txt`](../_build/saida_ex4_remessas_coisas_e_coisas.txt) |
| 5 | UniLE — Disciplinas e Aluno | Interface / SOLID / Polimorfismo | [`unile`](heranca_polimorfismo/unile) | ✅ 📄 | [`_build/saida_ex5...txt`](../_build/saida_ex5_unile_disciplinas_aluno.txt) |
| 6 | Material da aula 18/08 (UniLE, versão inicial) | Interface `IDisciplina` | [`aula1808`](../aula1808) | ✅ | [`_build/saida_ex6...txt`](../_build/saida_ex6_aula1808_unile_v1.txt) |

> **Exercícios 5 e 6 são a mesma atividade em dois momentos:** o `aula1808` é o
> código produzido em sala (todos os tipos em um único arquivo, com a interface
> `IDisciplina` declarada dentro de `DisciplinaGraduacao.java`); o exercício 5, em
> `unile/`, é a versão **refatorada** — um arquivo por classe, validações de
> entrada, `getNivel()`, `getDetalhamento()` e justificativa SOLID documentada.

---

> 📚 **Material de consulta para a prova:**
> [`material_consulta_prova/`](../material_consulta_prova) — cheatsheet, guia com
> templates Java de cada padrão e referência de UML, em Markdown e PDF.
>
> ⚙️ **Compilar e executar tudo:** `pwsh -File .\compilar_tudo.ps1` (na raiz).

---

## 1. Sistema de Emissão de Apólices — Factory Method

**Fonte:** `conteudos/_Exercicios_Design_Patterns_Java.docx` (Exercício 1) e
`aula0109/atividade.txt`.

**Requisitos implementados**

| Requisito | Regra | Onde |
|---|---|---|
| RF01 Auto | prêmio = 8% da FIPE/12; +30% se condutor < 25 anos; +20% se habilitação < 2 anos; exige cobertura contra terceiros ≥ R$ 50.000 | [`ApoliceAuto.java`](../aula0109/exercicio1/ApoliceAuto.java) |
| RF02 Residencial | prêmio = 1,5% do imóvel/12; +25% se alto padrão; exige escritura ou contrato de locação | [`ApoliceResidencial.java`](../aula0109/exercicio1/ApoliceResidencial.java) |
| RF03 Vida | prêmio = (idade × 12) + (capital × 0,002); +50% se fumante; capital > R$ 500.000 exige atestado médico | [`ApoliceVida.java`](../aula0109/exercicio1/ApoliceVida.java) |
| RF04 Viagem | prêmio = (dias × R$ 15) + R$ 100 se internacional; internacional exige assistência médica ≥ US$ 30.000 **e** passaporte | [`ApoliceViagem.java`](../aula0109/exercicio1/ApoliceViagem.java) |
| RNF01 (OCP) | 5.ª linha de produto entra só com classes novas | superclasse abstrata + 1 factory por linha |
| RNF02 | número único prefixado `AUTO-`, `RES-`, `VID-`, `VIA-` | `Apolice.atribuirNumero()` com contador `static` |
| RNF03 | resumo textual padronizado | `Apolice.gerarResumo()` |

**Estrutura exigida × entregue**

| Exigência do enunciado | Classe |
|---|---|
| Produto abstrato com prêmio, validação, documentos e resumo | `Apolice` (abstrata) |
| Uma subclasse concreta por linha de produto | `ApoliceAuto`, `ApoliceResidencial`, `ApoliceVida`, `ApoliceViagem` |
| Criador abstrato com método fábrica **abstrato** | `ApoliceFactory.criarApolice()` |
| Método **concreto e `final`** que processa a contratação | `ApoliceFactory.processarContratacao()` — `public final String` |
| Subclasse de criador por linha, sobrescrevendo o método fábrica | `ApoliceAutoFactory`, `ApoliceResidencialFactory`, `ApoliceVidaFactory`, `ApoliceViagemFactory` |
| Cliente que escolhe o criador e **nunca** instancia produto concreto | `MainApolice` |

**Critérios de avaliação — conferência**

- ✅ Método fábrica isolado nas subclasses de criador; algoritmo centralizado na
  superclasse (`processarContratacao` é `final`).
- ✅ Regras de RF01–RF04 fiéis, com rejeição (`validarCobertura()` retorna o
  motivo; `processarContratacao()` retorna `"Contratacao REJEITADA - ..."`).
- ✅ **Nenhuma** estrutura condicional que decida o tipo de produto no cliente ou
  na superclasse de criador (as condicionais existentes são de **regra de negócio**:
  idade, fumante, alto padrão — permitidas e necessárias).
- ✅ Diagrama aderente: [`diagrama.md`](../aula0109/exercicio1/diagrama.md).

**Saída observada (amostra):** `AUTO-1` prêmio R$ 533,33 · `RES-2` R$ 781,25 ·
`VID-3` R$ 760,00 · `VIA-4` R$ 250,00 · `AUTO-5` (jovem, 1 ano de CNH) R$ 832,00.

---

## 2. Checkout Internacional de Marketplace — Abstract Factory

**Fonte:** `conteudos/_Exercicios_Design_Patterns_Java.docx` (Exercício 2).

**Padrão identificado a partir do enunciado (não foi informado):**
**Abstract Factory** — o texto exige que **três artefatos** (documento fiscal,
pagamento, etiqueta) pertençam sempre ao **mesmo país**, e que a inclusão de um
novo país só adicione classes. Isso é exatamente "criar famílias de objetos
relacionados".

| Requisito | Regra | Onde |
|---|---|---|
| RF01 Brasil | NF-e, CFOP 5.102 / 6.102, ICMS 18% / 12% interestadual, chave de 44 dígitos; Pix com 5% de desconto ou boleto em 3 dias úteis; Correios CEP `00000-000` | [`NotaFiscalEletronica`](../aula0109/exercicio2/NotaFiscalEletronica.java), [`PagamentoPix`](../aula0109/exercicio2/PagamentoPix.java), [`PagamentoBoleto`](../aula0109/exercicio2/PagamentoBoleto.java), [`EtiquetaCorreios`](../aula0109/exercicio2/EtiquetaCorreios.java) |
| RF02 EUA | Sales invoice, sales tax por estado (CA 7,25% · TX 6,25% · OR isento), EIN do vendedor; cartão de crédito com AVS; USPS ZIP+4 | [`SalesInvoice`](../aula0109/exercicio2/SalesInvoice.java), [`PagamentoCartaoCredito`](../aula0109/exercicio2/PagamentoCartaoCredito.java), [`EtiquetaUsps`](../aula0109/exercicio2/EtiquetaUsps.java) |
| RF03 Alemanha | VAT invoice, Umsatzsteuer 19% (7% essenciais), VAT-ID; SEPA Direct Debit; Deutsche Post PLZ 5 dígitos | [`VatInvoice`](../aula0109/exercicio2/VatInvoice.java), [`PagamentoSepaDebito`](../aula0109/exercicio2/PagamentoSepaDebito.java), [`EtiquetaDeutschePost`](../aula0109/exercicio2/EtiquetaDeutschePost.java) |
| RNF01 | novo país = só classes novas | fábrica abstrata + fábricas concretas |
| RNF02 | finalizador sem condicionais por país | [`Checkout.finalizarPedido(CheckoutFactory)`](../aula0109/exercicio2/Checkout.java) |
| RNF03 | relatório padronizado dos três artefatos | `Checkout.finalizarPedido()` |

**Garantia estrutural** (critério mais importante): o cliente **não tem acesso**
aos construtores dos produtos — só os recebe via `CheckoutFactory`. Misturar
países exigiria **trocar a fábrica dentro do método**, alterando o código cliente.

**Extensão para um 4.º país:** criar `CheckoutXxxFactory` + os produtos concretos.
**Zero** classes existentes alteradas.

📄 [`diagrama.md`](../aula0109/exercicio2/diagrama.md)

---

## 3. Classe `Diretor` — atividade dos slides

**Fonte:** `conteudos/Padrões de Projetos - Herança, Polimorfismo e Method.pptx`,
slide "Atividade" (*Polimorfismo*).

> "A partir das classes do exemplo acima, implemente a classe **diretor**, cuja
> bonificação é **(1,5% do salário) multiplicado pelo número de funcionários sob
> sua gestão**."

**Entregue em** [`exemplo_funcionario/Diretor.java`](heranca_polimorfismo/exemplo_funcionario/Diretor.java),
junto com o exemplo completo: `Funcionario` (abstrata) · `Operador` · `Gerente` ·
`Diretor` · `Financeiro` (polimorfismo) · `Main`.

**Verificação:** salário R$ 20.000 com 30 geridos →
`(0,10 × 20.000) + (0,015 × 20.000 × 30)` = `2.000 + 9.000` = **R$ 11.000,00** ✅

📄 [`diagrama.md`](heranca_polimorfismo/exemplo_funcionario/diagrama.md)

> **Nota sobre `aula1108`:** os arquivos originais da aula (`funcionario.java`,
> `gerente.java`, `operador.java`, `financeiro.java`, `teste.java`) foram
> **preservados** — eles **não compilam** porque `operador` não implementa o
> método abstrato `getBonifacao()` e há `super.salario = 5` em `gerente.java`.
> A versão corrigida e completa está em `exemplo_funcionario/`.

---

## 4. Sistema de remessas da Coisas & Coisas — frete

**Fonte:** mesmo PPTX, slide "Atividade" (*Polimorfismo*).

> Todos os produtos têm `peso` (gramas), `volume` (cm³) e `preço`, e um método que
> calcula frete com base em **R$ 0,80/kg** e **R$ 1,00/m³**. `SuperServidor` inclui
> **seguro de 30% do preço**. "Implemente com o máximo de reaproveitamento de código."

**Entregue em** [`remessas_coisas_e_coisas`](heranca_polimorfismo/remessas_coisas_e_coisas):
`Produto` (regra geral do frete **uma única vez**) · `MiniPC` · `SoundBar` ·
`SuperServidor` (`super.calcularFrete() + seguro`) · `Remessa` (método que recebe
vários produtos) · `MainRemessa`.

**Verificação numérica**

| Produto | Frete |
|---|---|
| MiniPC | 0,500×0,80 + 0,0002×1,00 = **R$ 0,40** |
| SoundBar | 0,670×0,80 + 0,008×1,00 = **R$ 0,54** |
| SuperServidor | 3,800×0,80 + 0,12×1,00 = 3,16 · + 30%×30.000 = **R$ 9.003,16** |
| **Total** | **R$ 9.004,10** |

📄 [`diagrama.md`](heranca_polimorfismo/remessas_coisas_e_coisas/diagrama.md)

---

## 5. UniLE — Disciplinas e Aluno

**Fonte:** mesmo PPTX, slide "Atividade" (*Métodos abstratos*).

> Disciplinas de **graduação** têm notas 0–10 e média ≥ 7 aprova; de
> **especialização** têm conceitos {A, B, C, D} e reprovam se houver "D". "Com
> atenção aos princípios **SOLID**, desenhe e implemente as classes disciplina e
> aluno."

**Entregue em** [`unile`](heranca_polimorfismo/unile): `Disciplina` (interface) ·
`DisciplinaGraduacao` · `DisciplinaEspecializacao` · `Aluno` · `MainUniLE`.

**Decisão de projeto justificada:** interface em vez de classe abstrata porque o
único elemento comum é o **contrato** — não há estado nem algoritmo compartilhado
(graduação guarda `List<Double>`, especialização guarda `List<String>`).

**Verificação:** Matemática (8,0 · 7,0 · 9,5 → média 8,17) APROVADO · Física
(5,0 · 6,0 · 7,0 → média 6,00) REPROVADO · Algoritmos (7,0 · 7,0 → média 7,00)
APROVADO · Gestão de Projetos (A, B) APROVADO · Arquitetura (A, B, **D**) REPROVADO.

📄 [`diagrama.md`](heranca_polimorfismo/unile/diagrama.md)

---

## Como recompilar e executar tudo

**Opção 1 — script pronto (recomendado):** na raiz do projeto,

```powershell
pwsh -File .\compilar_tudo.ps1
```

Ele localiza o JDK automaticamente, compila os 6 exercícios em `_build/<exercicio>/`,
executa cada `main()` e grava a saída em `_build/saida_<exercicio>.txt`.

**Opção 2 — manualmente:**

```powershell
# Exercício 1
javac -encoding UTF-8 -d _build\ex1 aula0109\exercicio1\*.java
java  -cp _build\ex1 MainApolice

# Exercício 2
javac -encoding UTF-8 -d _build\ex2 aula0109\exercicio2\*.java
java  -cp _build\ex2 MainCheckout

# Exercício 3
javac -encoding UTF-8 -d _build\ex3 exercicios_professor\heranca_polimorfismo\exemplo_funcionario\*.java
java  -cp _build\ex3 Main

# Exercício 4
javac -encoding UTF-8 -d _build\ex4 exercicios_professor\heranca_polimorfismo\remessas_coisas_e_coisas\*.java
java  -cp _build\ex4 MainRemessa

# Exercício 5
javac -encoding UTF-8 -d _build\ex5 exercicios_professor\heranca_polimorfismo\unile\*.java
java  -cp _build\ex5 MainUniLE

# Exercício 6 (material da aula 18/08)
javac -encoding UTF-8 -d _build\ex6 aula1808\*.java
java  -cp _build\ex6 Main
```

Os arquivos `*.class` **não** ficam soltos nas pastas de código: toda a compilação
vai para `_build/<exercicio>/`. O `.gitignore` da raiz já ignora `*.class` e `_build/`.

> **Atenção ao compilar em Java moderno:** sempre use `-encoding UTF-8` (há acentos
> nos fontes e nos comentários) e, ao executar, defina a saída em UTF-8 para que
> acentos não virem `?`. No `compilar_tudo.ps1` isso é feito com `JAVA_TOOL_OPTIONS`.

---

## Observações sobre os arquivos originais

- Os `.class` antigos que existiam em `aula0109/exercicio1`, `aula0109/exercicio2`,
  `aula1808` e `aula1108` foram **removidos** para que o repositório contenha apenas
  fontes (boa prática com Git — `.class` é artefato gerado e passa a ser ignorado).
- O código-fonte original (`aula1108`, `aula1808`) foi **mantido intacto**, para
  preservar o que foi feito em sala.
- `aula1108` **não compila como está** (detalhes na seção 3) — por isso a versão
  corrigida e completa está em `exemplo_funcionario/`. O `aula1808`, por outro lado,
  **compila e executa** normalmente e é mantido como exercício 6.
