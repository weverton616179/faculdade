/**
 * Produto concreto - Alemanha (RF03): etiqueta de envio gerada pela
 * Deutsche Post, no formato PLZ de 5 digitos.
 */
public class EtiquetaDeutschePost implements EtiquetaEnvio {

    private final String plz;

    public EtiquetaDeutschePost(String plz) {
        this.plz = plz;
    }

    @Override
    public String gerar() {
        return "Etiqueta de envio - Deutsche Post (Alemanha)\n"
             + "  PLZ: " + plz + " (formato de 5 digitos)";
    }
}
