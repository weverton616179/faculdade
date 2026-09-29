/**
 * Especialização concreta: Operador.
 *
 * O operador NÃO tem adicional: sua bonificação é exatamente a bonificação
 * padrão da empresa, reaproveitada do método concreto da classe base.
 * (Máximo reaproveitamento de código — slide "Herança".)
 */
public class Operador extends Funcionario {

    public Operador(String nome, String cpf, double salario) {
        super(nome, cpf, salario);
    }

    @Override
    public double getBonificacao() {
        return calcularBonificacaoPadrao();   // 10% do salário
    }
}
