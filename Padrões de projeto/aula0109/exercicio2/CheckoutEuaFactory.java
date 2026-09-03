/**
 * Fabrica concreta - Estados Unidos (RF02).
 * Cria sales invoice (taxa conforme o estado), cartao de credito com AVS
 * e etiqueta da USPS no formato ZIP+4.
 */
public class CheckoutEuaFactory implements CheckoutFactory {

    private final double valor;
    private final String estado; // California, Texas ou Oregon
    private final String zip;

    public CheckoutEuaFactory(double valor, String estado, String zip) {
        this.valor = valor;
        this.estado = estado;
        this.zip = zip;
    }

    @Override
    public DocumentoFiscal criarDocumentoFiscal() {
        return new SalesInvoice(valor, estado);
    }

    @Override
    public Pagamento criarPagamento() {
        return new PagamentoCartaoCredito(valor);
    }

    @Override
    public EtiquetaEnvio criarEtiqueta() {
        return new EtiquetaUsps(zip);
    }
}
