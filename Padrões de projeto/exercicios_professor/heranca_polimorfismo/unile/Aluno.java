/**
 * ATIVIDADE DOS SLIDES — classe Aluno (UniLE).
 *
 * O Aluno NÃO conhece as classes concretas de disciplina: recebe a
 * ABSTRAÇÃO Disciplina (Dependency Inversion). Assim, quando um novo nível
 * de curso for criado, esta classe permanece intacta (Open/Closed).
 */
public class Aluno {

    private final String nome;
    private final String matricula;

    public Aluno(String nome, String matricula) {
        this.nome = nome;
        this.matricula = matricula;
    }

    public String getNome() { return nome; }
    public String getMatricula() { return matricula; }

    /**
     * Determina e exibe o resultado do aluno na disciplina recebida.
     *
     * POLIMORFISMO: a mesma chamada disciplina.isAprovado() executa lógicas
     * totalmente diferentes conforme o objeto real (graduação ou
     * especialização), sem nenhum if/else por tipo de disciplina.
     */
    public void exibirResultado(Disciplina disciplina) {
        String situacao = disciplina.isAprovado() ? "APROVADO" : "REPROVADO";

        System.out.println("--------------------------------------------------------------");
        System.out.printf("Aluno......: %s (matricula %s)%n", nome, matricula);
        System.out.printf("Disciplina.: %s%n", disciplina.getNome());
        System.out.printf("Nivel......: %s%n", disciplina.getNivel());
        System.out.printf("Detalhe....: %s%n", disciplina.getDetalhamento());
        System.out.printf("RESULTADO..: %s%n", situacao);
        System.out.println("--------------------------------------------------------------");
    }
}
