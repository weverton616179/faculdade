import java.util.List;

/**
 * Produto concreto: Apolice Residencial (RF02).
 * Premio mensal = 1,5% do valor do imovel ao ano, dividido por 12.
 * Imovel de alto padrao recebe acrescimo de 25% sobre o premio anual.
 * Exige escritura ou contrato de locacao.
 */
public class ApoliceResidencial extends Apolice {

    private final double valorImovel;
    private final boolean altoPadrao;
    private final boolean temEscrituraOuContrato;

    public ApoliceResidencial(String segurado, double valorImovel,
                              boolean altoPadrao, boolean temEscrituraOuContrato) {
        this.segurado = segurado;
        this.valorImovel = valorImovel;
        this.altoPadrao = altoPadrao;
        this.temEscrituraOuContrato = temEscrituraOuContrato;
    }

    @Override
    public String getPrefixo() {
        return "RES-";
    }

    @Override
    public double calcularPremio() {
        double premioAnual = 0.015 * valorImovel; // 1,5% ao ano
        if (altoPadrao) {
            premioAnual *= 1.25; // acrescimo de 25%
        }
        return premioAnual / 12.0; // premio mensal
    }

    @Override
    public String validarCobertura() {
        if (!temEscrituraOuContrato) {
            return "e obrigatoria a apresentacao de escritura ou contrato de locacao";
        }
        return null;
    }

    @Override
    public List<String> getDocumentosExigidos() {
        return List.of("escritura ou contrato de locacao", "comprovante de residencia");
    }
}
