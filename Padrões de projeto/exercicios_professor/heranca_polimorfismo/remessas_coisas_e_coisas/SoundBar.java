/**
 * SoundBar {peso: 670 g, volume: 8.000 cm³, preço: R$ 1.800,00}
 *
 * Também herda integralmente o frete geral da classe Produto.
 */
public class SoundBar extends Produto {

    public SoundBar() {
        super("SoundBar", 670, 8000, 1800.00);
    }
}
