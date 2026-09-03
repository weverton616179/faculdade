import java.util.ArrayList;
import java.util.List;

/**
 * Produto concreto: Apolice Viagem (RF04).
 * Premio = (dias de viagem x R$ 15,00) + R$ 100,00 se destino internacional.
 * Viagem internacional exige cobertura medica de, no minimo, US$ 30.000,00
 * e apresentacao de passaporte.
 */
public class ApoliceViagem extends Apolice {

    private final int diasViagem;
    private final boolean internacional;
    private final double coberturaMedicaUsd;
    private final boolean temPassaporte;

    public ApoliceViagem(String segurado, int diasViagem, boolean internacional,
                         double coberturaMedicaUsd, boolean temPassaporte) {
        this.segurado = segurado;
        this.diasViagem = diasViagem;
        this.internacional = internacional;
        this.coberturaMedicaUsd = coberturaMedicaUsd;
        this.temPassaporte = temPassaporte;
    }

    @Override
    public String getPrefixo() {
        return "VIA-";
    }

    @Override
    public double calcularPremio() {
        double premio = diasViagem * 15.0;
        if (internacional) {
            premio += 100.0;
        }
        return premio;
    }

    @Override
    public String validarCobertura() {
        if (internacional) {
            if (coberturaMedicaUsd < 30000) {
                return "viagem internacional exige cobertura medica de, no minimo, US$ 30.000,00";
            }
            if (!temPassaporte) {
                return "viagem internacional exige apresentacao de passaporte";
            }
        }
        return null;
    }

    @Override
    public List<String> getDocumentosExigidos() {
        List<String> documentos = new ArrayList<>();
        documentos.add("itinerario de viagem");
        if (internacional) {
            documentos.add("passaporte");
        }
        return documentos;
    }
}
