public class VoucherPortugal implements Voucher {

    private final String hospede;
    private final String nif;
    private final String periodo;

    public VoucherPortugal(String hospede, String nif, String periodo) {
        this.hospede = hospede;
        this.nif = nif;
        this.periodo = periodo;
    }

    @Override
    public String gerar() {
        return "voucher: padrao portugues\n"
             + "  hospede: " + hospede + "\n"
             + "  identificacao: nif " + nif + "\n"
             + "  periodo da hospedagem: " + periodo;
    }
}
