public abstract class OperacaoCredito {

    protected final String cliente;

    protected final double valorSolicitado;

    protected OperacaoCredito(String cliente, double valorSolicitado) {
        if (cliente == null || cliente.trim().isEmpty()) {
            throw new IllegalArgumentException("O nome do cliente e obrigatorio.");
        }
        if (valorSolicitado <= 0) {
            throw new IllegalArgumentException("O valor solicitado deve ser maior que zero.");
        }
        this.cliente = cliente.trim();
        this.valorSolicitado = valorSolicitado;
    }

    public abstract String getModalidade();

    public abstract double getPercentualJurosPrimeiroMes();

    public abstract String[] getDocumentosExigidos();

    public final double calcularJurosPrimeiroMes() {
        return valorSolicitado * getPercentualJurosPrimeiroMes() / 100.0;
    }

    public final String getCliente() {
        return cliente;
    }

    public final double getValorSolicitado() {
        return valorSolicitado;
    }

    public final String gerarResumo() {
        StringBuilder sb = new StringBuilder();
        sb.append("modalidade: ").append(getModalidade()).append("\n");
        sb.append("cliente: ").append(cliente).append("\n");
        sb.append("valor solicitado: R$ ").append(String.format("%.2f", valorSolicitado)).append("\n");
        sb.append("juros do primeiro mes (").append(formatarPercentual())
          .append("%): R$ ").append(String.format("%.2f", calcularJurosPrimeiroMes())).append("\n");
        sb.append("documentos exigidos: ").append(String.join(", ", getDocumentosExigidos())).append("\n");
        return sb.toString();
    }

    private String formatarPercentual() {
        return String.format(java.util.Locale.ROOT, "%.1f", getPercentualJurosPrimeiroMes());
    }
}
