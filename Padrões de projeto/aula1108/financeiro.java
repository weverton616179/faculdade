public class financeiro {
    private double total_bonus =0.0;

    public void computa_bonus(funcionario funcionario){
        this.total_bonus += funcionario.getBonifacao();
    }

    

    public double get_total_bonus(){
        return this.total_bonus;
    }
}
