public class ConcessaoCreditoPessoal extends ConcessaoCredito {

    public ConcessaoCreditoPessoal(String cliente, double valorSolicitado) {
        super(cliente, valorSolicitado);
    }

    @Override
    public OperacaoCredito criarOperacaoCredito() {
        return new CreditoPessoal(cliente, valorSolicitado);
    }
}
