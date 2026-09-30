public class ConcessaoCreditoImobiliario extends ConcessaoCredito {

    public ConcessaoCreditoImobiliario(String cliente, double valorSolicitado) {
        super(cliente, valorSolicitado);
    }

    @Override
    public OperacaoCredito criarOperacaoCredito() {
        return new CreditoImobiliario(cliente, valorSolicitado);
    }
}
