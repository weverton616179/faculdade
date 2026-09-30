public class CreditoImobiliario extends OperacaoCredito {

    private static final double JUROS_PRIMEIRO_MES = 0.8;

    private static final String[] DOCUMENTOS = {
        "matricula do imovel",
        "comprovante de renda"
    };

    public CreditoImobiliario(String cliente, double valorSolicitado) {
        super(cliente, valorSolicitado);
    }

    @Override
    public String getModalidade() {
        return "Credito Imobiliario";
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
