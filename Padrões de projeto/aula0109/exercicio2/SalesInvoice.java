/**
 * Produto concreto - Estados Unidos (RF02): Sales Invoice.
 * Sales tax conforme o estado de destino
 * (California 7,25%, Texas 6,25%, Oregon isento) e EIN do vendedor.
 */
public class SalesInvoice implements DocumentoFiscal {

    private final double valor;
    private final String estado;
    private final String ein = "12-3456789"; // EIN do vendedor (simulado)

    public SalesInvoice(double valor, String estado) {
        this.valor = valor;
        this.estado = estado;
    }

    private double getTaxa() {
        switch (estado.toLowerCase()) {
            case "california": return 0.0725;
            case "texas":      return 0.0625;
            case "oregon":     return 0.0;
            default:           return 0.0;
        }
    }

    @Override
    public String gerar() {
        double taxa = getTaxa();
        double imposto = valor * taxa;
        double total = valor + imposto;

        return "Sales Invoice (Estados Unidos)\n"
             + "  Estado de destino: " + estado + "\n"
             + "  Subtotal: US$ " + String.format("%.2f", valor) + "\n"
             + "  Sales tax: " + String.format("%.2f%%", taxa * 100)
             + " (US$ " + String.format("%.2f", imposto) + ")\n"
             + "  Total: US$ " + String.format("%.2f", total) + "\n"
             + "  Vendedor (EIN): " + ein;
    }
}
