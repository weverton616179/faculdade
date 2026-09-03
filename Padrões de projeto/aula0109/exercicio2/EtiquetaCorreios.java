/**
 * Produto concreto - Brasil (RF01): etiqueta de envio gerada pelos Correios,
 * com CEP no formato 00000-000.
 */
public class EtiquetaCorreios implements EtiquetaEnvio {

    private final String cep;

    public EtiquetaCorreios(String cep) {
        this.cep = cep;
    }

    @Override
    public String gerar() {
        return "Etiqueta de envio - Correios (Brasil)\n"
             + "  CEP: " + cep + " (formato 00000-000)";
    }
}
