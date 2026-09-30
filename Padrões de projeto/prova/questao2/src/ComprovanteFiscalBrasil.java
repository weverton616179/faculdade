public class ComprovanteFiscalBrasil implements ComprovanteFiscal {

    private static final double ALIQUOTA_ISS = 5.0;

    private final String hospede;
    private final double valorDiarias;

    public ComprovanteFiscalBrasil(String hospede, double valorDiarias) {
        this.hospede = hospede;
        this.valorDiarias = valorDiarias;
    }

    @Override
    public String gerar() {
        double iss = valorDiarias * ALIQUOTA_ISS / 100.0;
        return "comprovante fiscal: NFSe\n"
             + "  tomador do servico: " + hospede + "\n"
             + "  vase de calculo: R$ " + String.format("%.2f", valorDiarias) + "\n"
             + "  iss (5%): R$ " + String.format("%.2f", iss) + "\n"
             + "  total da nota: R$ " + String.format("%.2f", valorDiarias + iss);
    }
}
