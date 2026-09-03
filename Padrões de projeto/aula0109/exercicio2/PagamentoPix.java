/**
 * Produto concreto - Brasil (RF01): pagamento via Pix, com desconto de 5%.
 */
public class PagamentoPix implements Pagamento {

    private final double valor;

    public PagamentoPix(double valor) {
        this.valor = valor;
    }

    @Override
    public String processar() {
        double desconto = valor * 0.05;
        double total = valor - desconto;
        return "Pagamento via Pix (Brasil)\n"
             + "  Valor original: R$ " + String.format("%.2f", valor) + "\n"
             + "  Desconto de 5%: R$ " + String.format("%.2f", desconto) + "\n"
             + "  Total a pagar: R$ " + String.format("%.2f", total);
    }
}
