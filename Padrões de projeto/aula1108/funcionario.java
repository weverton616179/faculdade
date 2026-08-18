public abstract class funcionario{
    protected String nome;
    protected String cpf;
    protected double salario;
    protected String senha;

    public abstract double getBonifacao();

    public boolean autentica(String senha){
        return this.senha.equals(senha);
    }
}