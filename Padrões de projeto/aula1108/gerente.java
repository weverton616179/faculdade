public class gerente extends funcionario {
    
    public int numeroDeFuncionariosGerenciados;

    @Override
    public double getBonifacao(){
        super.salario = 5;
        // double bonus_base =  super.getBonifacao();
        double bonus_adicinal = 0.2 * this.numeroDeFuncionariosGerenciados;
        return  bonus_adicinal;
    }
}
