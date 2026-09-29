/**
 * Especialização concreta: Gerente.
 *
 * Regra do slide "Herança - implementação":
 *   "O gerente recebe uma bonificação adicional somada à bonificação
 *    padrão (da classe funcionário)."
 *
 * Implementação: bonificação padrão (reaproveitada da classe base) MAIS o
 * adicional de gestão (20% do salário, conforme o exemplo da aula).
 */
public class Gerente extends Funcionario {

    /** Adicional de gestão sobre o salário. */
    public static final double PERCENTUAL_ADICIONAL_GESTAO = 0.20;

    private final int numeroDeFuncionariosGerenciados;

    public Gerente(String nome, String cpf, double salario,
                   int numeroDeFuncionariosGerenciados) {
        super(nome, cpf, salario);
        this.numeroDeFuncionariosGerenciados = numeroDeFuncionariosGerenciados;
    }

    public int getNumeroDeFuncionariosGerenciados() {
        return numeroDeFuncionariosGerenciados;
    }

    @Override
    public double getBonificacao() {
        double bonusPadrao = calcularBonificacaoPadrao();      // reaproveitado
        double adicionalGestao = PERCENTUAL_ADICIONAL_GESTAO * this.salario;
        return bonusPadrao + adicionalGestao;
    }
}
