/**
 * Fabrica concreta - Brasil (RF01).
 * Cria NF-e, pagamento (Pix com desconto de 5% ou boleto) e etiqueta dos
 * Correios. A escolha do meio de pagamento fica DENTRO desta fabrica.
 */
public class CheckoutBrasilFactory implements CheckoutFactory {

    private final double valor;
    private final boolean interestadual;
    private final String cep;
    private final String modoPagamento; // "pix" ou "boleto"

    public CheckoutBrasilFactory(double valor, boolean interestadual,
                                 String cep, String modoPagamento) {
        this.valor = valor;
        this.interestadual = interestadual;
        this.cep = cep;
        this.modoPagamento = modoPagamento;
    }

    @Override
    public DocumentoFiscal criarDocumentoFiscal() {
        return new NotaFiscalEletronica(valor, interestadual);
    }

    @Override
    public Pagamento criarPagamento() {
        if (modoPagamento.equalsIgnoreCase("boleto")) {
            return new PagamentoBoleto(valor);
        }
        return new PagamentoPix(valor);
    }

    @Override
    public EtiquetaEnvio criarEtiqueta() {
        return new EtiquetaCorreios(cep);
    }
}
