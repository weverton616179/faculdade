# Exercicio 2 - Abstract Factory: Checkout Internacional de Marketplace

## Diagrama de Classes UML

```mermaid
classDiagram
    direction TB

    %% ===== FABRICA ABSTRATA =====
    class CheckoutFactory {
        <<interface>>
        +criarDocumentoFiscal() DocumentoFiscal
        +criarPagamento() Pagamento
        +criarEtiqueta() EtiquetaEnvio
    }

    CheckoutFactory <|.. CheckoutBrasilFactory
    CheckoutFactory <|.. CheckoutEuaFactory
    CheckoutFactory <|.. CheckoutAlemanhaFactory

    %% ===== INTERFACES DE PRODUTO =====
    class DocumentoFiscal {
        <<interface>>
        +gerar() String
    }
    class Pagamento {
        <<interface>>
        +processar() String
    }
    class EtiquetaEnvio {
        <<interface>>
        +gerar() String
    }

    %% ===== PRODUTOS CONCRETOS: BRASIL =====
    class NotaFiscalEletronica
    class PagamentoPix
    class PagamentoBoleto
    class EtiquetaCorreios

    %% ===== PRODUTOS CONCRETOS: EUA =====
    class SalesInvoice
    class PagamentoCartaoCredito
    class EtiquetaUsps

    %% ===== PRODUTOS CONCRETOS: ALEMANHA =====
    class VatInvoice
    class PagamentoSepaDebito
    class EtiquetaDeutschePost

    DocumentoFiscal <|.. NotaFiscalEletronica
    DocumentoFiscal <|.. SalesInvoice
    DocumentoFiscal <|.. VatInvoice

    Pagamento <|.. PagamentoPix
    Pagamento <|.. PagamentoBoleto
    Pagamento <|.. PagamentoCartaoCredito
    Pagamento <|.. PagamentoSepaDebito

    EtiquetaEnvio <|.. EtiquetaCorreios
    EtiquetaEnvio <|.. EtiquetaUsps
    EtiquetaEnvio <|.. EtiquetaDeutschePost

    %% ===== RELACAO FABRICA x PRODUTOS (mesmo pais) =====
    CheckoutBrasilFactory ..> NotaFiscalEletronica : cria
    CheckoutBrasilFactory ..> PagamentoPix : cria
    CheckoutBrasilFactory ..> PagamentoBoleto : cria
    CheckoutBrasilFactory ..> EtiquetaCorreios : cria

    CheckoutEuaFactory ..> SalesInvoice : cria
    CheckoutEuaFactory ..> PagamentoCartaoCredito : cria
    CheckoutEuaFactory ..> EtiquetaUsps : cria

    CheckoutAlemanhaFactory ..> VatInvoice : cria
    CheckoutAlemanhaFactory ..> PagamentoSepaDebito : cria
    CheckoutAlemanhaFactory ..> EtiquetaDeutschePost : cria

    %% ===== CLIENTE =====
    class Checkout {
        +finalizarPedido(CheckoutFactory) String
    }

    class MainCheckout {
        +main(String[]) void
    }

    Checkout ..> CheckoutFactory : "depende apenas de abstracoes (RNF02)"
    MainCheckout ..> Checkout : usa
    MainCheckout ..> CheckoutBrasilFactory : "instancia a fabrica do pais"
    MainCheckout ..> CheckoutEuaFactory : "instancia a fabrica do pais"
    MainCheckout ..> CheckoutAlemanhaFactory : "instancia a fabrica do pais"
```

## Legenda

- `CheckoutFactory` (fabrica abstrata): declara um metodo para criar cada um dos tres
  artefatos do pedido. Por construcao, os tres artefatos de um pedido pertencem sempre ao
  mesmo pais (nenhuma combinacao invalida e possivel sem trocar a fabrica).
- Fabricas concretas por pais: `CheckoutBrasilFactory`, `CheckoutEuaFactory` e
  `CheckoutAlemanhaFactory` criam a familia completa de artefatos do respectivo pais.
- Interfaces de produto: `DocumentoFiscal`, `Pagamento` e `EtiquetaEnvio`, com produtos
  concretos por pais.
- `Checkout` (finalizador): usa somente a abstracao `CheckoutFactory` para gerar o
  relatorio padronizado, sem condicionais por pais (RNF02/RNF03).
- Extensao para um 4o pais: adicionar uma fabrica concreta + produtos novos, sem alterar
  nenhuma classe existente (RNF01).
