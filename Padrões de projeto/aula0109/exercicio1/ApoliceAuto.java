import java.util.List;

/**
 * Produto concreto: Apolice Auto (RF01).
 * Premio mensal = 8% do valor FIPE ao ano, dividido por 12.
 * Acrescimos: condutor < 25 anos (+30%) e habilitacao < 2 anos (+20%),
 * aplicados sobre o premio anual.
 * Exige cobertura contra terceiros de, no minimo, R$ 50.000,00.
 */
public class ApoliceAuto extends Apolice {

    private final double valorFipe;
    private final int idadeCondutor;
    private final int anosHabilitacao;
    private final double coberturaTerceiros;

    public ApoliceAuto(String segurado, double valorFipe, int idadeCondutor,
                       int anosHabilitacao, double coberturaTerceiros) {
        this.segurado = segurado;
        this.valorFipe = valorFipe;
        this.idadeCondutor = idadeCondutor;
        this.anosHabilitacao = anosHabilitacao;
        this.coberturaTerceiros = coberturaTerceiros;
    }

    @Override
    public String getPrefixo() {
        return "AUTO-";
    }

    @Override
    public double calcularPremio() {
        double premioAnual = 0.08 * valorFipe; // 8% ao ano
        if (idadeCondutor < 25) {
            premioAnual *= 1.30; // acrescimo de 30%
        }
        if (anosHabilitacao < 2) {
            premioAnual *= 1.20; // acrescimo adicional de 20%
        }
        return premioAnual / 12.0; // premio mensal
    }

    @Override
    public String validarCobertura() {
        if (coberturaTerceiros < 50000) {
            return "cobertura contra terceiros deve ser de, no minimo, R$ 50.000,00";
        }
        return null;
    }

    @Override
    public List<String> getDocumentosExigidos() {
        return List.of("CNH", "CRLV", "comprovante de residencia");
    }
}
