/**
 * MiniPC {peso: 500 g, volume: 200 cm³, preço: R$ 5.000,00}
 *
 * Nenhuma linha de cálculo é escrita: herda integralmente o frete geral da
 * classe Produto (máximo reaproveitamento de código).
 */
public class MiniPC extends Produto {

    public MiniPC() {
        super("MiniPC", 500, 200, 5000.00);
    }
}
