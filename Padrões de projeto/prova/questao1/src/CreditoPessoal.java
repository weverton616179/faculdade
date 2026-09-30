public class CreditoPessoal extends OperacaoCredito {

    private static final double JUROS_PRIMEIRO_MES = 3.5;

    private static final String[] DOCUMENTOS = {
        "documento de identidade",
        "comprovante de renda"
    };

    public CreditoPessoal(String cliente, double valorSolicitado) {
        super(cliente, valorSolicitado);
    }

    @Override
    public String getModalidade() {
        return "Credito Pessoal";
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
