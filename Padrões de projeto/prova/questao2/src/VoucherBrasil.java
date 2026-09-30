public class VoucherBrasil implements Voucher {

    private final String hospede;
    private final String cpf;
    private final String periodo;

    public VoucherBrasil(String hospede, String cpf, String periodo) {
        this.hospede = hospede;
        this.cpf = cpf;
        this.periodo = periodo;
    }

    @Override
    public String gerar() {
        return "voucher: padrao brasileiro\n"
             + "  hospede: " + hospede + "\n"
             + "  identificacao: cpf " + cpf + "\n"
             + "  periodo da hospedagem: " + periodo;
    }
}
