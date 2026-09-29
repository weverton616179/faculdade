/**
 * Atividade (slide "Polimorfismo" / "Herança e Polimorfismo").
 *
 * Enunciado:
 *   "A partir das classes do exemplo acima, implemente a classe diretor,
 *    cuja bonificação é (1,5% do salário) multiplicado pelo número de
 *    funcionários sob sua gestão."
 *
 * Formula: getBonificacao() = (0,015 * salario) * numeroDeFuncionariosGerenciados
 */
public class diretor extends funcionario {

    public int numeroDeFuncionariosGerenciados;

    /**
     * Salário base + adicional de gestão.
     *
     * Observe o uso de super.getBonifacao(): o diretor recebe a bonificação
     * padrão da classe funcionario MAIS o adicional de 1,5% do salário por
     * funcionário sob sua gestão. Se a regra base mudar, o diretor acompanha
     * automaticamente (reaproveitamento de código, slide "Herança").
     */
    @Override
    public double getBonifacao() {
        double bonusBase = super.getBonifacao();
        double bonusGestao = (0.015 * this.salario) * this.numeroDeFuncionariosGerenciados;
        return bonusBase + bonusGestao;
    }
}
