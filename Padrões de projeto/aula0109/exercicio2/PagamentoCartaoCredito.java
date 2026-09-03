/**
 * Produto concreto - Estados Unidos (RF02): pagamento por cartao de
 * credito, com verificacao AVS.
 */
public class PagamentoCartaoCredito implements Pagamento {

    private final double valor;

    public PagamentoCartaoCredito(double valor) {
        this.valor = valor;
    }

    @Override
    public String processar() {
        return "Pagamento via Cartao de Credito (Estados Unidos)\n"
             + "  Valor: US$ " + String.format("%.2f", valor) + "\n"
             + "  Verificacao AVS: aprovada";
    }
}
