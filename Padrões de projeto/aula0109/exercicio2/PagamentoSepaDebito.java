/**
 * Produto concreto - Alemanha (RF03): pagamento processado por
 * SEPA Direct Debit.
 */
public class PagamentoSepaDebito implements Pagamento {

    private final double valor;

    public PagamentoSepaDebito(double valor) {
        this.valor = valor;
    }

    @Override
    public String processar() {
        return "Pagamento via SEPA Direct Debit (Alemanha)\n"
             + "  Valor: EUR " + String.format("%.2f", valor);
    }
}
