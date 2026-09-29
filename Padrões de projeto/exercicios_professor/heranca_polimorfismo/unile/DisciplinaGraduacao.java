import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Disciplina de GRADUAÇÃO.
 *
 * Regra: notas de 0 a 10; média >= 7 -> aprovado; média < 7 -> reprovado.
 *
 * Note o construtor protegido que recebe o nome: ele evita repetir a
 * validação/atribuição de nome em cada subclasse (reaproveitamento).
 */
public class DisciplinaGraduacao implements Disciplina {

    public static final double MEDIA_APROVACAO = 7.0;
    private static final double NOTA_MINIMA = 0.0;
    private static final double NOTA_MAXIMA = 10.0;

    private final String nome;
    private final List<Double> notas = new ArrayList<>();

    public DisciplinaGraduacao(String nome) {
        this.nome = nome;
    }

    /** Registra uma nota. Valores fora de 0..10 são rejeitados. */
    public void registrarNota(double nota) {
        if (nota < NOTA_MINIMA || nota > NOTA_MAXIMA) {
            throw new IllegalArgumentException(
                    "Nota invalida para a graduacao (0 a 10): " + nota);
        }
        this.notas.add(nota);
    }

    public List<Double> getNotas() {
        return Collections.unmodifiableList(notas);
    }

    /**
     * Média aritmética simples.
     * Disciplina sem notas registradas => média 0 => reprovado,
     * evitando divisão por zero.
     */
    public double getMedia() {
        if (notas.isEmpty()) {
            return 0.0;
        }
        double soma = 0.0;
        for (double nota : notas) {
            soma += nota;
        }
        return soma / notas.size();
    }

    @Override
    public String getNome() { return nome; }

    @Override
    public String getNivel() { return "Graduacao"; }

    @Override
    public boolean isAprovado() {
        return getMedia() >= MEDIA_APROVACAO;
    }

    @Override
    public String getDetalhamento() {
        StringBuilder sb = new StringBuilder();
        sb.append("Media ").append(String.format("%.2f", getMedia()));
        sb.append(" (notas: ");
        for (int i = 0; i < notas.size(); i++) {
            if (i > 0) sb.append("; ");
            sb.append(String.format("%.1f", notas.get(i)));
        }
        if (notas.isEmpty()) sb.append("nenhuma nota registrada");
        sb.append(") - criterio: media >= ").append(String.format("%.1f", MEDIA_APROVACAO));
        return sb.toString();
    }
}
