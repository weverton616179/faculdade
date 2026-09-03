/**
 * Cliente (teste) do Exercicio 1 - Factory Method.
 * Seleciona o criador adequado para cada tipo de apolice e NUNCA instancia
 * diretamente uma classe concreta de produto (nenhum "new Apolice..." aqui).
 */
public class MainApolice {

    public static void main(String[] args) {
        System.out.println("===== EMISSAO DE APOLICES (Factory Method) =====\n");

        // ---- CASOS DE SUCESSO: uma apolice de cada linha ----

        // RF01 - Auto: FIPE 80.000, condutor de 30 anos, habilitacao de 5 anos,
        // cobertura contra terceiros de 60.000 (>= 50.000, valida)
        ApoliceFactory auto = new ApoliceAutoFactory(
                "Carlos Souza", 80000, 30, 5, 60000);
        System.out.println(auto.processarContratacao());
        System.out.println();

        // RF02 - Residencial: imovel de 500.000, alto padrao, com escritura
        ApoliceFactory residencial = new ApoliceResidencialFactory(
                "Maria Oliveira", 500000, true, true);
        System.out.println(residencial.processarContratacao());
        System.out.println();

        // RF03 - Vida: segurado de 30 anos, capital 200.000, nao fumante
        ApoliceFactory vida = new ApoliceVidaFactory(
                "Joao Pereira", 30, 200000, false, false);
        System.out.println(vida.processarContratacao());
        System.out.println();

        // RF04 - Viagem: 10 dias internacionais, cobertura medica de 50.000 USD,
        // com passaporte
        ApoliceFactory viagem = new ApoliceViagemFactory(
                "Ana Lima", 10, true, 50000, true);
        System.out.println(viagem.processarContratacao());
        System.out.println();

        // ---- DEMONSTRACAO DE ACRESCIMOS E VARIANTES (RF01 a RF04) ----

        // Auto: condutor de 20 anos (< 25) e habilitacao de 1 ano (< 2)
        // -> 8% de 80.000 = 6.400/ano x1,30 x1,20 = 9.984 -> R$ 832,00/mes
        ApoliceFactory autoJovem = new ApoliceAutoFactory(
                "Pedro Ferreira", 80000, 20, 1, 60000);
        System.out.println(autoJovem.processarContratacao());
        System.out.println();

        // Residencial padrao (sem acrescimo de alto padrao)
        // -> 1,5% de 400.000/12 = R$ 500,00/mes
        ApoliceFactory residencialPadrao = new ApoliceResidencialFactory(
                "Fernanda Paes", 400000, false, true);
        System.out.println(residencialPadrao.processarContratacao());
        System.out.println();

        // Vida: segurado fumante -> acrescimo de 50%
        // -> (40x12) + (100.000x0,002) = 680 x1,50 = R$ 1.020,00
        ApoliceFactory vidaFumante = new ApoliceVidaFactory(
                "Marcos Lima", 40, 100000, true, false);
        System.out.println(vidaFumante.processarContratacao());
        System.out.println();

        // Viagem nacional (sem acrescimo de destino internacional)
        // -> 10 dias x R$ 15,00 = R$ 150,00
        ApoliceFactory viagemNacional = new ApoliceViagemFactory(
                "Lucas Reis", 10, false, 0, false);
        System.out.println(viagemNacional.processarContratacao());
        System.out.println();

        // ---- CASOS DE REJEICAO: provam as validacoes RF01 a RF04 ----

        // Auto sem cobertura minima (30.000 < 50.000) -> REJEITADA
        ApoliceFactory autoInvalida = new ApoliceAutoFactory(
                "Paulo Dias", 80000, 22, 1, 30000);
        System.out.println(autoInvalida.processarContratacao());
        System.out.println();

        // Residencial sem escritura nem contrato -> REJEITADA
        ApoliceFactory residencialInvalida = new ApoliceResidencialFactory(
                "Rita Alves", 300000, false, false);
        System.out.println(residencialInvalida.processarContratacao());
        System.out.println();

        // Vida com capital 600.000 sem atestado medico -> REJEITADA
        ApoliceFactory vidaInvalida = new ApoliceVidaFactory(
                "Bruno Costa", 40, 600000, false, false);
        System.out.println(vidaInvalida.processarContratacao());
        System.out.println();

        // Viagem internacional sem cobertura medica minima -> REJEITADA
        ApoliceFactory viagemInvalida = new ApoliceViagemFactory(
                "Carla Mendes", 7, true, 10000, true);
        System.out.println(viagemInvalida.processarContratacao());
    }
}
