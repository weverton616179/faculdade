import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Disciplina de ESPECIALIZAÇÃO.
 *
 * Regra: conceitos {A, B, C, D}; o aluno é REPROVADO sempre que houver
 * conceito "D" (basta um único D).
 *
 * A classe NÃO tem "notas" nem média: sua estrutura é diferente da
 * graduação, o que justifica o uso de interface (contrato) em vez de
 * herança de uma classe base com algoritmo comum.
 */
public class DisciplinaEspecializacao implements Disciplina {

    private static final List<String> CONCEITOS_VALIDOS = List.of("A", "B", "C", "D");
    private static final String CONCEITO_REPROVACAO = "D";

    private final String nome;
    private final List<String> conceitos = new ArrayList<>();

    public DisciplinaEspecializacao(String nome) {
        this.nome = nome;
    }

    /** Registra um conceito; aceita apenas A, B, C ou D (case-insensitive). */
    public void registrarConceito(String conceito) {
        String normalizado = (conceito == null) ? "" : conceito.trim().toUpperCase();
        if (!CONCEITOS_VALIDOS.contains(normalizado)) {
            throw new IllegalArgumentException(
                    "Conceito invalido para a especializacao (A, B, C ou D): " + conceito);
        }
        this.conceitos.add(normalizado);
    }

    public List<String> getConceitos() {
        return Collections.unmodifiableList(conceitos);
    }

    @Override
    public String getNome() { return nome; }

    @Override
    public String getNivel() { return "Especializacao"; }

    @Override
    public boolean isAprovado() {
        // Reprovado sempre que houver conceito "D"
        return !conceitos.contains(CONCEITO_REPROVACAO);
    }

    @Override
    public String getDetalhamento() {
        StringBuilder sb = new StringBuilder();
        sb.append("Conceitos: ");
        if (conceitos.isEmpty()) {
            sb.append("nenhum conceito registrado");
        } else {
            sb.append(String.join(", ", conceitos));
        }
        sb.append(" - criterio: reprovado se houver conceito \"")
          .append(CONCEITO_REPROVACAO).append("\"");
        return sb.toString();
    }
}
