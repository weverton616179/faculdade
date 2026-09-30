public class CreditoConsignado extends OperacaoCredito {

    private static final double JUROS_PRIMEIRO_MES = 1.8;

    private static final String[] DOCUMENTOS = {
        "contracheque",
        "extrato de beneficio"
    };

    public CreditoConsignado(String cliente, double valorSolicitado) {
        super(cliente, valorSolicitado);
    }

    @Override
    public String getModalidade() {
        return "Credito Consignado";
    }

    @Override
    public double getPercentualJurosPrimeiroMes() {
        return JUROS_PRIMEIRO_MES;
    }

    @Override
    public String[] getDocumentosExigidos() {
        return DOCUMENTOS.clone();
    }
}
