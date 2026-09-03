# Exercicio 1 - Factory Method: Sistema de Emissao de Apolices

## Diagrama de Classes UML

```mermaid
classDiagram
    direction TB

    %% ===== Hierarquia de PRODUTOS =====
    class Apolice {
        <<abstract>>
        #String numero
        #String segurado
        #LocalDate dataEmissao
        #double premio
        -static int contador
        +getPrefixo()* String
        +calcularPremio()* double
        +validarCobertura()* String
        +getDocumentosExigidos()* List~String~
        +atribuirNumero() void
        +setDataEmissao(LocalDate) void
        +setPremio(double) void
        +gerarResumo() String
    }

    class ApoliceAuto {
        -double valorFipe
        -int idadeCondutor
        -int anosHabilitacao
        -double coberturaTerceiros
        +calcularPremio() double
        +validarCobertura() String
    }

    class ApoliceResidencial {
        -double valorImovel
        -boolean altoPadrao
        -boolean temEscrituraOuContrato
        +calcularPremio() double
        +validarCobertura() String
    }

    class ApoliceVida {
        -int idade
        -double capitalSegurado
        -boolean fumante
        -boolean temAtestadoMedico
        +calcularPremio() double
        +validarCobertura() String
    }

    class ApoliceViagem {
        -int diasViagem
        -boolean internacional
        -double coberturaMedicaUsd
        -boolean temPassaporte
        +calcularPremio() double
        +validarCobertura() String
    }

    Apolice <|-- ApoliceAuto
    Apolice <|-- ApoliceResidencial
    Apolice <|-- ApoliceVida
    Apolice <|-- ApoliceViagem

    %% ===== Hierarquia de CRIADORES =====
    class ApoliceFactory {
        <<abstract>>
        +criarApolice()* Apolice
        +processarContratacao() String <<final>>
    }

    class ApoliceAutoFactory {
        +criarApolice() Apolice
    }
    class ApoliceResidencialFactory {
        +criarApolice() Apolice
    }
    class ApoliceVidaFactory {
        +criarApolice() Apolice
    }
    class ApoliceViagemFactory {
        +criarApolice() Apolice
    }

    ApoliceFactory <|-- ApoliceAutoFactory
    ApoliceFactory <|-- ApoliceResidencialFactory
    ApoliceFactory <|-- ApoliceVidaFactory
    ApoliceFactory <|-- ApoliceViagemFactory

    %% Relacao entre metodo fabrica e o produto criado
    ApoliceFactory --> Apolice : "criarApolice()"

    %% ===== CLIENTE =====
    class MainApolice {
        +main(String[]) void
    }

    MainApolice ..> ApoliceFactory : "seleciona criador\n(usa subclasses concretas)"
    MainApolice ..> Apolice : "recebe resumo\n(nunca instancia produto)"
```

## Legenda

- `Apolice` (abstrata): declara os metodos comuns a toda apolice (calculo de premio,
  validacao de cobertura, listagem de documentos e geracao de resumo).
- `ApoliceFactory` (abstrata): declara o **metodo fabrica** abstrato `criarApolice()` e o
  metodo concreto e final `processarContratacao()`, que usa apenas a abstracao do produto.
- Subclasses concretas de criador: cada uma sobrescreve `criarApolice()` para retornar a
  apolice correspondente.
- `MainApolice` (cliente): seleciona o criador pelo tipo de apolice e nunca instancia
  diretamente uma classe concreta de produto.
