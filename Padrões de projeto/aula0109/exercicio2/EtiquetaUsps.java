/**
 * Produto concreto - Estados Unidos (RF02): etiqueta de envio gerada pela
 * USPS, no formato ZIP+4.
 */
public class EtiquetaUsps implements EtiquetaEnvio {

    private final String zip;

    public EtiquetaUsps(String zip) {
        this.zip = zip;
    }

    @Override
    public String gerar() {
        return "Etiqueta de envio - USPS (Estados Unidos)\n"
             + "  ZIP+4: " + zip;
    }
}
