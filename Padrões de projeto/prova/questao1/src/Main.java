public class Main {

    public static void main(String[] args) {
        System.out.println("- cooperativa de credito e consessão de emprestimos -");
        System.out.println("\n");

        ConcessaoCredito pessoal = new ConcessaoCreditoPessoal("Batatilson Mandioca", 12000.00);
        System.out.println(pessoal.concessaoCompleta());

        ConcessaoCredito consignado = new ConcessaoCreditoConsignado("Bananilson Farofa", 12000.00);
        System.out.println(consignado.concessaoCompleta());

        ConcessaoCredito imobiliario = new ConcessaoCreditoImobiliario("Wilsonson Filhofa", 12000.00);
        System.out.println(imobiliario.concessaoCompleta());

        ConcessaoCredito veicular = new ConcessaoCredito("Frangilson Grelhilson", 12000.00) {
            @Override
            public OperacaoCredito criarOperacaoCredito() {
                return new OperacaoCredito(cliente, valorSolicitado) {
                    @Override
                    public String getModalidade() {
                        return "Credito Veicular";
                    }

                    @Override
                    public double getPercentualJurosPrimeiroMes() {
                        return 0.9;
                    }

                    @Override
                    public String[] getDocumentosExigidos() {
                        return new String[] { "documento do veiculo", "comprovante de renda" };
                    }
                };
            }
        };

        System.out.println("- nova modalidade acrescentada -\n");
        System.out.println(veicular.concessaoCompleta());
    }
}
