public class ConcessaoCreditoConsignado extends ConcessaoCredito {

    public ConcessaoCreditoConsignado(String cliente, double valorSolicitado) {
        super(cliente, valorSolicitado);
    }

    @Override
    public OperacaoCredito criarOperacaoCredito() {
        return new CreditoConsignado(cliente, valorSolicitado);
    }
}
