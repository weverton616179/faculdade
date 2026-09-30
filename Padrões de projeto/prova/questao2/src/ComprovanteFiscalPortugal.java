public class ComprovanteFiscalPortugal implements ComprovanteFiscal {

    private static final double ALIQUOTA_IVA = 6.0;

    private final String hospede;
    private final double valorDiarias;

    public ComprovanteFiscalPortugal(String hospede, double valorDiarias) {
        this.hospede = hospede;
        this.valorDiarias = valorDiarias;
    }

    @Override
    public String gerar() {
        double iva = valorDiarias * ALIQUOTA_IVA / 100.0;
        return "comprovante fiscal fatura\n"
             + "  adquirente: " + hospede + "\n"
             + "  base tributavel: eur " + String.format("%.2f", valorDiarias) + "\n"
             + "  iva (6%): eur " + String.format("%.2f", iva) + "\n"
             + "  total da fatura: eur " + String.format("%.2f", valorDiarias + iva);
    }
}
