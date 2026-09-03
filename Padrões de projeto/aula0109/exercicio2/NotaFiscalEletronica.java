/**
 * Produto concreto - Brasil (RF01): Nota Fiscal Eletronica.
 * CFOP 5.102 (dentro do estado) ou 6.102 (interestadual),
 * ICMS de 18% (ou 12% em operacoes interestaduais) e chave de acesso
 * simulada de 44 digitos.
 */
public class NotaFiscalEletronica implements DocumentoFiscal {

    private final double valor;
    private final boolean interestadual;
    private final String chaveAcesso;

    public NotaFiscalEletronica(double valor, boolean interestadual) {
        this.valor = valor;
        this.interestadual = interestadual;
        this.chaveAcesso = gerarChaveAcesso();
    }

    // Chave de acesso simulada com 44 digitos
    private String gerarChaveAcesso() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 44; i++) {
            sb.append((int) (Math.random() * 10));
        }
        return sb.toString();
    }

    @Override
    public String gerar() {
        String cfop = interestadual ? "6.102 (interestadual)" : "5.102 (dentro do estado)";
        double icms = interestadual ? 0.12 : 0.18;
        double valorIcms = valor * icms;

        return "Nota Fiscal Eletronica (Brasil)\n"
             + "  Valor da operacao: R$ " + String.format("%.2f", valor) + "\n"
             + "  CFOP: " + cfop + "\n"
             + "  ICMS: " + String.format("%.2f%%", icms * 100)
             + " (R$ " + String.format("%.2f", valorIcms) + ")\n"
             + "  Chave de acesso (44 digitos): " + chaveAcesso;
    }
}
