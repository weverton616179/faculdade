/**
 * Classe de teste da atividade UniLE.
 *
 * Demonstra as duas regras de determinação de resultado e exercita o
 * polimorfismo através da abstração Disciplina.
 */
public class MainUniLE {

    public static void main(String[] args) {

        System.out.println("========== UNILE - DETERMINACAO DE RESULTADOS ==========");
        System.out.println();

        // ---------- GRADUAÇÃO ----------
        System.out.println("### DISCIPLINAS DE GRADUACAO (media >= 7,0 aprova) ###");

        Aluno joao = new Aluno("Joao Pereira", "2026001");
        Disciplina graduacaoOk = new DisciplinaGraduacao("Matematica");
        ((DisciplinaGraduacao) graduacaoOk).registrarNota(8.0);
        ((DisciplinaGraduacao) graduacaoOk).registrarNota(7.0);
        ((DisciplinaGraduacao) graduacaoOk).registrarNota(9.5);  // media 8,17
        joao.exibirResultado(graduacaoOk);

        Disciplina graduacaoReprovado = new DisciplinaGraduacao("Fisica");
        ((DisciplinaGraduacao) graduacaoReprovado).registrarNota(5.0);
        ((DisciplinaGraduacao) graduacaoReprovado).registrarNota(6.0);
        ((DisciplinaGraduacao) graduacaoReprovado).registrarNota(7.0); // media 6,00
        joao.exibirResultado(graduacaoReprovado);

        Disciplina graduacaoLimite = new DisciplinaGraduacao("Algoritmos");
        ((DisciplinaGraduacao) graduacaoLimite).registrarNota(7.0);
        ((DisciplinaGraduacao) graduacaoLimite).registrarNota(7.0);   // media exatamente 7,00
        joao.exibirResultado(graduacaoLimite);

        // ---------- ESPECIALIZAÇÃO ----------
        System.out.println();
        System.out.println("### DISCIPLINAS DE ESPECIALIZACAO (reprovado se houver conceito D) ###");

        Aluno maria = new Aluno("Maria Oliveira", "2026002");

        Disciplina espOk = new DisciplinaEspecializacao("Gestao de Projetos");
        ((DisciplinaEspecializacao) espOk).registrarConceito("A");
        ((DisciplinaEspecializacao) espOk).registrarConceito("B");
        maria.exibirResultado(espOk);

        Disciplina espReprovado = new DisciplinaEspecializacao("Arquitetura de Software");
        ((DisciplinaEspecializacao) espReprovado).registrarConceito("A");
        ((DisciplinaEspecializacao) espReprovado).registrarConceito("B");
        ((DisciplinaEspecializacao) espReprovado).registrarConceito("D"); // um D reprova
        maria.exibirResultado(espReprovado);

        // ---------- PROVA DO POLIMORFISMO ----------
        System.out.println();
        System.out.println("### PROVA DO POLIMORFISMO ###");

        // Nenhum if/else por tipo: o mesmo método processa os dois níveis.
        Disciplina[] disciplinas = {
                graduacaoOk,
                graduacaoReprovado,
                espOk,
                espReprovado
        };

        for (Disciplina d : disciplinas) {
            System.out.printf("%-28s (%s) -> %s%n",
                    d.getNome(), d.getNivel(),
                    d.isAprovado() ? "APROVADO" : "REPROVADO");
        }

        System.out.println();
        System.out.println("Extensao (OCP): para criar um novo nivel, basta uma nova classe");
        System.out.println("que implemente Disciplina. Aluno e as classes existentes nao mudam.");
    }
}
