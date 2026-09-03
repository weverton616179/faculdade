import java.util.ArrayList;
import java.util.List;

/**
 * Produto concreto: Apolice Vida (RF03).
 * Premio mensal = (idade do segurado x 12) + (capital segurado x 0,002).
 * Segurado fumante recebe acrescimo de 50% sobre o premio.
 * Capital acima de R$ 500.000,00 exige atestado medico.
 */
public class ApoliceVida extends Apolice {

    private final int idade;
    private final double capitalSegurado;
    private final boolean fumante;
    private final boolean temAtestadoMedico;

    public ApoliceVida(String segurado, int idade, double capitalSegurado,
                       boolean fumante, boolean temAtestadoMedico) {
        this.segurado = segurado;
        this.idade = idade;
        this.capitalSegurado = capitalSegurado;
        this.fumante = fumante;
        this.temAtestadoMedico = temAtestadoMedico;
    }

    @Override
    public String getPrefixo() {
        return "VID-";
    }

    @Override
    public double calcularPremio() {
        double premio = (idade * 12) + (capitalSegurado * 0.002);
        if (fumante) {
            premio *= 1.50; // acrescimo de 50%
        }
        return premio;
    }

    @Override
    public String validarCobertura() {
        if (capitalSegurado > 500000 && !temAtestadoMedico) {
            return "capital segurado acima de R$ 500.000,00 exige atestado medico";
        }
        return null;
    }

    @Override
    public List<String> getDocumentosExigidos() {
        List<String> documentos = new ArrayList<>();
        documentos.add("documento de identidade");
        documentos.add("CPF");
        if (capitalSegurado > 500000) {
            documentos.add("atestado medico");
        }
        return documentos;
    }
}
