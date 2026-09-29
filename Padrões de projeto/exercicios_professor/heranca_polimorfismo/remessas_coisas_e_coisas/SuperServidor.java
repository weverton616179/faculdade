/**
 * SuperServidor {peso: 3.800 g, volume: 120.000 cm³, preço: R$ 30.000,00}
 *
 * PARTICULARIDADE: "para este produto, o frete inclui uma taxa de seguro
 * equivalente a 30% do seu preço".
 *
 * Reaproveitamento: chamamos super.calcularFrete() (regra geral já
 * implementada na classe base) e somamos apenas o que é específico.
 * Se a tarifa geral mudar, este produto acompanha automaticamente.
 */
public class SuperServidor extends Produto {

    /** Taxa de seguro: 30% do preço do produto. */
    public static final double TAXA_SEGURO = 0.30;

    public SuperServidor() {
        super("SuperServidor", 3800, 120000, 30000.00);
    }

    /** Valor do seguro embutido no frete. */
    public double calcularSeguro() {
        return TAXA_SEGURO * preco;
    }

    @Override
    public double calcularFrete() {
        return super.calcularFrete() + calcularSeguro();
    }
}
