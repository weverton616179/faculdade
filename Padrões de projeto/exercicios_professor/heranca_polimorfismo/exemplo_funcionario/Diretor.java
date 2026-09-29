/**
 * ATIVIDADE DOS SLIDES — classe Diretor.
 *
 * Enunciado:
 *   "A partir das classes do exemplo acima, implemente a classe diretor,
 *    cuja bonificação é (1,5% do salário) multiplicado pelo número de
 *    funcionários sob sua gestão."
 *
 * Fórmula pedida: bonusGestao = (0,015 * salario) * numeroDeFuncionarios
 *
 * Interpretação adotada (a mesma do Gerente, pelo slide "Herança"):
 * o Diretor recebe a BONIFICAÇÃO PADRÃO (reaproveitada da classe base)
 * SOMADA ao adicional de gestão do enunciado.
 *
 * Se o professor quiser SOMENTE a fórmula literal, basta retornar
 * "bonusGestao" sem somar o bonusPadrao.
 */
public class Diretor extends Funcionario {

    /** Percentual do enunciado: 1,5% do salário por funcionário gerido. */
    public static final double PERCENTUAL_POR_GERIDO = 0.015;

    private final int numeroDeFuncionariosGerenciados;

    public Diretor(String nome, String cpf, double salario,
                   int numeroDeFuncionariosGerenciados) {
        super(nome, cpf, salario);
        this.numeroDeFuncionariosGerenciados = numeroDeFuncionariosGerenciados;
    }

    public int getNumeroDeFuncionariosGerenciados() {
        return numeroDeFuncionariosGerenciados;
    }

    @Override
    public double getBonificacao() {
        double bonusPadrao = calcularBonificacaoPadrao();               // herdado
        double bonusGestao = (PERCENTUAL_POR_GERIDO * this.salario)
                             * this.numeroDeFuncionariosGerenciados;    // enunciado
        return bonusPadrao + bonusGestao;
    }
}
