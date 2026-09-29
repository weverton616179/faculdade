/**
 * ATIVIDADE DOS SLIDES — UniLE
 *
 * Enunciado:
 *   "A UniLE é uma famosa instituição de ensino superior onde há cursos de
 *    diferentes níveis com diferentes regras de determinação de resultados
 *    para as disciplinas.
 *      - Disciplinas da graduação possuem notas que variam de 0 a 10 e o
 *        resultado é determinado por: se a média das notas é maior ou igual
 *        a 7, o aluno é aprovado; se a média for menor que 7, reprovado.
 *      - Disciplinas da especialização possuem conceitos {A, B, C ou D} e o
 *        aluno é reprovado sempre que houver conceito 'D'.
 *    Com atenção aos princípios SOLID, desenhe e implemente as classes
 *    disciplina e aluno, de maneira a determinar se o aluno será aprovado
 *    ou reprovado."
 *
 * POR QUE UMA INTERFACE (e não herança de classe abstrata)?
 *  - O conceito comum às disciplinas de níveis diferentes é apenas o
 *    CONTRATO: "tenho nome" e "sei dizer se o aluno foi aprovado".
 *  - As especializações não compartilham estado nem algoritmo comum: a
 *    graduação trabalha com lista de notas e a especialização com lista de
 *    conceitos. Não há código comum para herdar.
 *  - Interfaces determinam um contrato mínimo (slides "Interfaces") e são
 *    mais flexíveis: a classe Aluno depende apenas desta abstração.
 *
 * PRINCÍPIOS SOLID APLICADOS:
 *  - S (SRP) : Disciplina cuida do resultado; Aluno cuida de se apresentar
 *              e de exibir o resultado. Ninguém acumula responsabilidades.
 *  - O (OCP) : um novo nível (ex.: mestrado) entra por uma NOVA classe que
 *              implementa Disciplina. Nada já existente é alterado.
 *  - L (LSP) : qualquer implementação pode substituir Disciplina sem
 *              quebrar Aluno.exibirResultado().
 *  - I (ISP) : a interface é enxuta — só o que todo consumidor precisa.
 *  - D (DIP) : Aluno depende da ABSTRAÇÃO Disciplina, nunca de
 *              DisciplinaGraduacao ou DisciplinaEspecializacao.
 */
public interface Disciplina {

    String getNome();

    /** Nome do nível/categoria (usado apenas para exibição do resultado). */
    String getNivel();

    /**
     * @return true se o aluno está aprovado nesta disciplina,
     *         false caso contrário.
     */
    boolean isAprovado();

    /**
     * Descrição textual do critério adotado e da situação atual.
     * Ex.: "Media 7,50 (notas: 8,0; 7,0) - criterio: media >= 7,0".
     */
    String getDetalhamento();
}
