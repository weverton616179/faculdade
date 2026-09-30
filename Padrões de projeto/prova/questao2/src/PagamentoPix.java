public class PagamentoPix implements Pagamento {

    private final String hospede;
    private final String cpf;
    private final double valor;

    public PagamentoPix(String hospede, String cpf, double valor) {
        this.hospede = hospede;
        this.cpf = cpf;
        this.valor = valor;
    }

    @Override
    public String processar() {
        return "pagamento: pix\n"
             + "  pagador: " + hospede + " (CPF " + cpf + ")\n"
             + "  valor liquidado: R$ " + String.format("%.2f", valor) + "\n"
             + "  status: liquidado no ato da confirmacao da reserva";
    }
}
