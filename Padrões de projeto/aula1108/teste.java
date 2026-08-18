public class teste {
    public static void main(String[] args) {
        financeiro fin = new financeiro();
        
        gerente coord = new gerente();
        coord.nome = "Araci de Almeida";
        coord.salario = 10000;
        coord.numeroDeFuncionariosGerenciados = 10;

        gerente coord1 = new gerente();
        coord1.nome = "Pedro de Lara";
        coord1.salario = 8000;
        coord1.numeroDeFuncionariosGerenciados = 5;
        
        operador porteiro = new operador();
        porteiro.nome = "Escobar";
        porteiro.salario = 1500;
        fin.computa_bonus(coord);
        fin.computa_bonus(coord1);
        fin.computa_bonus(porteiro);

        funcionario func = new gerente();
        func.nome = "Silvio Santos";
        func.salario = 20000;
    
        System.out.println(func.getBonifacao());
    }
}
