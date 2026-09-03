/**
 * Produto concreto - Brasil (RF01): pagamento via boleto,
 * com compensacao em 3 dias uteis.
 */
public class PagamentoBoleto implements Pagamento {

    private final double valor;

    public PagamentoBoleto(double valor) {
        this.valor = valor;
    }

    @Override
    public String processar() {
        return "Pagamento via Boleto (Brasil)\n"
             + "  Valor: R$ " + String.format("%.2f", valor) + "\n"
             + "  Compensacao em 3 dias uteis";
    }
}
