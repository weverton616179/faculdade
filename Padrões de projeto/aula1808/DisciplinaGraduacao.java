import java.util.ArrayList;
import java.util.List;

// 1. A Interface (Contrato)
interface IDisciplina {
    String getNome();
    boolean isAprovado();
}

// 2. Classe concreta para Graduação
class DisciplinaGraduacao implements IDisciplina {
    private String nome;
    private List<Double> notas;

    public DisciplinaGraduacao(String nome) {
        this.nome = nome;
        this.notas = new ArrayList<>();
    }

    public void adicionarNota(double nota) {
        // Validação simples: notas variam de 0 a 10
        if(nota >= 0 && nota <= 10) {
            this.notas.add(nota);
        }
    }

    @Override
    public String getNome() {
        return this.nome;
    }

    @Override
    public boolean isAprovado() {
        if (notas.isEmpty()) return false;
        
        double soma = 0;
        for (double n : notas) {
            soma += n;
        }
        double media = soma / notas.size();
        
        // Se a média das notas é maior ou igual a 7, o aluno é aprovado
        return media >= 7.0; 
    }
}

// 3. Classe concreta para Especialização
class DisciplinaEspecializacao implements IDisciplina {
    private String nome;
    private List<String> conceitos;

    public DisciplinaEspecializacao(String nome) {
        this.nome = nome;
        this.conceitos = new ArrayList<>();
    }

    public void adicionarConceito(String conceito) {
        String c = conceito.toUpperCase();
        // Conceitos válidos: A, B, C ou D (conforme enunciado)
        if (c.equals("A") || c.equals("B") || c.equals("C") || c.equals("D")) {
            this.conceitos.add(c);
        }
    }

    @Override
    public String getNome() {
        return this.nome;
    }

    @Override
    public boolean isAprovado() {
        // O aluno é reprovado sempre que houver conceito "D"
        return !this.conceitos.contains("D");
    }
}

// 4. Classe Aluno
class Aluno {
    private String nome;

    public Aluno(String nome) {
        this.nome = nome;
    }

    public String getNome() {
        return this.nome;
    }

    // O método recebe a interface (Polimorfismo). 
    // O Aluno não precisa saber como a disciplina calcula a aprovação.
    public void exibirResultado(IDisciplina disciplina) {
        if (disciplina.isAprovado()) {
            System.out.println("O aluno " + this.nome + " foi APROVADO na disciplina " + disciplina.getNome());
        } else {
            System.out.println("O aluno " + this.nome + " foi REPROVADO na disciplina " + disciplina.getNome());
        }
    }
}