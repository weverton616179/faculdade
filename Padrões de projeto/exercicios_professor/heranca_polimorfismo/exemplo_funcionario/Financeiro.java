import java.util.ArrayList;
import java.util.List;

/**
 * Classe que demonstra POLIMORFISMO.
 *
 * Recebe a classe base (Funcionario) como parâmetro, portanto processa
 * qualquer especialização sem conhecer o tipo concreto. Nenhum if/else
 * por tipo de funcionário é necessário.
 */
public class Financeiro {

    private final List<Funcionario> folha = new ArrayList<>();
    private double totalBonus = 0.0;

    /** Polimorfismo: aceita Gerente, Operador, Diretor... qualquer Funcionario. */
    public void computaBonus(Funcionario funcionario) {
        this.folha.add(funcionario);
        this.totalBonus += funcionario.getBonificacao();
    }

    public double getTotalBonus() {
        return this.totalBonus;
    }

    public void imprimirFolha() {
        System.out.printf("%-18s %-12s %14s %14s%n",
                "NOME", "TIPO", "SALARIO", "BONIFICACAO");
        System.out.println("-".repeat(62));
        for (Funcionario f : folha) {
            System.out.printf("%-18s %-12s %14.2f %14.2f%n",
                    f.getNome(),
                    f.getClass().getSimpleName(),   // reflexão: só para exibição
                    f.getSalario(),
                    f.getBonificacao());            // chamada polimórfica
        }
        System.out.println("-".repeat(62));
        System.out.printf("%-46s %14.2f%n", "TOTAL DE BONIFICACOES", totalBonus);
    }
}
