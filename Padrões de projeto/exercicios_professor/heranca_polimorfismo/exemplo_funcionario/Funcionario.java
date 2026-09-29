/**
 * Classe base do exemplo de HERANÇA, POLIMORFISMO e CLASSES ABSTRATAS.
 *
 * ATENÇÃO — DETALHE IMPORTANTE DE PROVA:
 *   getBonificacao() é ABSTRATO porque cada especialização tem regra própria.
 *   Em Java NÃO é possível chamar super.metodoAbstrato(). Portanto, para
 *   permitir o reaproveitamento da "bonificação padrão" (10% do salário)
 *   pelas subclasses, a regra padrão fica em um método PROTECTED e CONCRETO
 *   (calcularBonificacaoPadrao()), que as subclasses consomem via super.
 *
 *   Se você tentar escrever "super.getBonificacao()" dentro do Gerente, o
 *   javac acusa:
 *     error: abstract method getBonificacao() in Funcionario
 *            cannot be accessed directly
 *
 * PRINCÍPIOS SOLID:
 *  - SRP: cada classe cuida apenas do próprio cálculo.
 *  - OCP: novas especializações entram por novas classes, sem alterar esta.
 *  - LSP: qualquer subclasse substitui Funcionario sem quebrar Financeiro.
 */
public abstract class Funcionario {

    /** Bonificação padrão da empresa: 10% do salário. */
    public static final double PERCENTUAL_BONIFICACAO_PADRAO = 0.10;

    protected String nome;
    protected String cpf;
    protected double salario;

    public Funcionario(String nome, String cpf, double salario) {
        this.nome = nome;
        this.cpf = cpf;
        this.salario = salario;
    }

    public String getNome()    { return nome; }
    public String getCpf()     { return cpf; }
    public double getSalario() { return salario; }

    /**
     * Regra padrão de bonificação, reaproveitável pelas subclasses
     * (protected + concreto = pode ser chamado com super.).
     */
    protected double calcularBonificacaoPadrao() {
        return PERCENTUAL_BONIFICACAO_PADRAO * this.salario;
    }

    /**
     * MÉTODO ABSTRATO: não há implementação aqui porque cada especialização
     * possui sua regra. Mantê-lo na classe base preserva a assinatura comum
     * e é o que permite o uso polimórfico pela classe Financeiro.
     */
    public abstract double getBonificacao();

    @Override
    public String toString() {
        return String.format("%s (%s) salario=R$ %.2f", nome, getClass().getSimpleName(), salario);
    }
}
