public abstract class ConcessaoCredito {

    protected final String cliente;

    protected final double valorSolicitado;

    protected ConcessaoCredito(String cliente, double valorSolicitado) {
        this.cliente = cliente;
        this.valorSolicitado = valorSolicitado;
    }

    public abstract OperacaoCredito criarOperacaoCredito();

    public final String concessaoCompleta() {
        OperacaoCredito operacao = criarOperacaoCredito();
        double juros = operacao.calcularJurosPrimeiroMes();

        return "- CONCESSAO DE CREDITO -\n" + operacao.gerarResumo()
             + "Juros calculados pelo procedimento unico de concessao: R$ "
             + String.format(java.util.Locale.ROOT, "%.2f", juros) + "\n";
    }
}
