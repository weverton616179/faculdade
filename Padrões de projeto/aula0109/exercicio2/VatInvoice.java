/**
 * Produto concreto - Alemanha (RF03): VAT Invoice.
 * Umsatzsteuer de 19% (ou 7% para produtos essenciais) e VAT-ID do vendedor.
 */
public class VatInvoice implements DocumentoFiscal {

    private final double valor;
    private final boolean produtoEssencial;
    private final String vatId = "DE123456789"; // VAT-ID do vendedor (simulado)

    public VatInvoice(double valor, boolean produtoEssencial) {
        this.valor = valor;
        this.produtoEssencial = produtoEssencial;
    }

    @Override
    public String gerar() {
        double taxa = produtoEssencial ? 0.07 : 0.19;
        double imposto = valor * taxa;
        double total = valor + imposto;

        String tipo = produtoEssencial ? "produto essencial" : "produto padrao";

        return "VAT Invoice (Alemanha)\n"
             + "  Tipo: " + tipo + "\n"
             + "  Valor liquido: EUR " + String.format("%.2f", valor) + "\n"
             + "  Umsatzsteuer: " + String.format("%.2f%%", taxa * 100)
             + " (EUR " + String.format("%.2f", imposto) + ")\n"
             + "  Total: EUR " + String.format("%.2f", total) + "\n"
             + "  Vendedor (VAT-ID): " + vatId;
    }
}
