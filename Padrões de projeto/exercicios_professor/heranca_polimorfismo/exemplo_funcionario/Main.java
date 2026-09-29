/**
 * Classe de teste (consumidor) do exemplo de Herança/Polimorfismo.
 *
 * A referência é do tipo da CLASSE BASE (Funcionario) apontando para
 * objetos das classes especializadas — isto é polimorfismo:
 *
 *      Funcionario f = new Diretor(...);
 *
 * Em tempo de execução, a JVM escolhe a implementação de getBonificacao()
 * da classe real do objeto (ligação tardia / dynamic dispatch).
 */
public class Main {

    public static void main(String[] args) {

        Financeiro financeiro = new Financeiro();

        Operador porteiro = new Operador("Escobar", "111.111.111-11", 1500.00);
        Gerente  coord    = new Gerente ("Araci de Almeida", "222.222.222-22", 10000.00, 10);
        Gerente  coord2   = new Gerente ("Pedro de Lara", "333.333.333-33", 8000.00, 5);
        Diretor  diretor  = new Diretor ("Silvio Santos", "444.444.444-44", 20000.00, 30);

        financeiro.computaBonus(porteiro);
        financeiro.computaBonus(coord);
        financeiro.computaBonus(coord2);
        financeiro.computaBonus(diretor);

        financeiro.imprimirFolha();

        System.out.println();
        System.out.println("=== CONFERENCIA MANUAL DAS FORMULAS ===");
        System.out.printf("Operador 1500,00  -> 10%% do salario                    = %.2f%n",
                porteiro.getBonificacao());
        System.out.printf("Gerente 10000,00  -> 10%% + 20%% do salario             = %.2f%n",
                coord.getBonificacao());
        System.out.printf("Diretor 20000,00  -> 10%% + (1,5%% x 20000) x 30        = %.2f%n",
                diretor.getBonificacao());
        System.out.println();
        System.out.println("ATIVIDADE: a classe Diretor foi implementada conforme o enunciado.");

        // Polimorfismo com referencia da classe base
        Funcionario generico = new Diretor("Diretora Generica", "555.555.555-55", 30000.00, 4);
        System.out.printf("Referencia Funcionario -> Diretor: bonificacao = %.2f%n",
                generico.getBonificacao());
    }
}
