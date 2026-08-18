// 5. Classe de Teste (Consumidor)
public class Main {
    public static void main(String[] args) {
        Aluno aluno1 = new Aluno("João");
        
        // Testando Graduação
        DisciplinaGraduacao mat = new DisciplinaGraduacao("Matemática (Graduação)");
        mat.adicionarNota(8.0);
        mat.adicionarNota(6.0); // Média 7.0 -> Aprovado
        
        // Testando Especialização
        DisciplinaEspecializacao proj = new DisciplinaEspecializacao("Gestão de Projetos (Especialização)");
        proj.adicionarConceito("A");
        proj.adicionarConceito("D"); // Contém D -> Reprovado
        
        // Polimorfismo em ação
        aluno1.exibirResultado(mat);
        aluno1.exibirResultado(proj);
    }
}
