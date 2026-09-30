public class PagamentoMbWay implements Pagamento {

    private final String hospede;
    private final String nif;
    private final double valor;

    public PagamentoMbWay(String hospede, String nif, double valor) {
        this.hospede = hospede;
        this.nif = nif;
        this.valor = valor;
    }

    @Override
    public String processar() {
        return "pagamento: MB WAY\n"
             + "  pagador: " + hospede + " (NIF " + nif + ")\n"
             + "  valor liquidado: eur " + String.format("%.2f", valor) + "\n"
             + "  status: liquidado no ato da confirmacao da reserva";
    }
}
