/**
 * Fabrica concreta - Alemanha (RF03).
 * Cria VAT invoice (Umsatzsteuer 19% ou 7% para produtos essenciais),
 * pagamento via SEPA Direct Debit e etiqueta da Deutsche Post.
 */
public class CheckoutAlemanhaFactory implements CheckoutFactory {

    private final double valor;
    private final boolean produtoEssencial;
    private final String plz;

    public CheckoutAlemanhaFactory(double valor, boolean produtoEssencial, String plz) {
        this.valor = valor;
        this.produtoEssencial = produtoEssencial;
        this.plz = plz;
    }

    @Override
    public DocumentoFiscal criarDocumentoFiscal() {
        return new VatInvoice(valor, produtoEssencial);
    }

    @Override
    public Pagamento criarPagamento() {
        return new PagamentoSepaDebito(valor);
    }

    @Override
    public EtiquetaEnvio criarEtiqueta() {
        return new EtiquetaDeutschePost(plz);
    }
}
