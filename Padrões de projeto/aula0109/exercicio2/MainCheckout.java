/**
 * Cliente (teste) do Exercicio 2 - Abstract Factory.
 * Finaliza um pedido para cada um dos tres paises e imprime o relatorio
 * gerado. A estrutura das classes impede combinar artefatos de paises
 * diferentes em um mesmo pedido: cada pedido recebe a fabrica de um unico
 * pais.
 */
public class MainCheckout {

    public static void main(String[] args) {
        Checkout checkout = new Checkout();

        // RF01 - Brasil: NF-e com CFOP interestadual, pagamento Pix, Correios
        CheckoutFactory brasilPix = new CheckoutBrasilFactory(
                1000.00, true, "01310-100", "pix");
        System.out.println(checkout.finalizarPedido(brasilPix));

        // RF01 - Brasil: mesma NF-e, mas pagamento via boleto
        CheckoutFactory brasilBoleto = new CheckoutBrasilFactory(
                1000.00, false, "01310-100", "boleto");
        System.out.println(checkout.finalizarPedido(brasilBoleto));

        // RF02 - Estados Unidos: sales invoice California, cartao com AVS, USPS
        CheckoutFactory eua = new CheckoutEuaFactory(
                750.00, "California", "90001-1234");
        System.out.println(checkout.finalizarPedido(eua));

        // RF03 - Alemanha: VAT invoice padrao, SEPA Direct Debit, Deutsche Post
        CheckoutFactory alemanha = new CheckoutAlemanhaFactory(
                850.00, false, "10115");
        System.out.println(checkout.finalizarPedido(alemanha));

        // ---- DEMONSTRACAO DE VARIANTES DE TAXA (RF02/RF03) ----

        // RF02 - EUA: sales invoice Texas (sales tax de 6,25%)
        CheckoutFactory euaTexas = new CheckoutEuaFactory(
                750.00, "Texas", "73301-0000");
        System.out.println(checkout.finalizarPedido(euaTexas));

        // RF02 - EUA: sales invoice Oregon (isento de sales tax)
        CheckoutFactory euaOregon = new CheckoutEuaFactory(
                750.00, "Oregon", "97201-0000");
        System.out.println(checkout.finalizarPedido(euaOregon));

        // RF03 - Alemanha: VAT invoice de produto essencial (Umsatzsteuer de 7%)
        CheckoutFactory alemanhaEssencial = new CheckoutAlemanhaFactory(
                850.00, true, "10115");
        System.out.println(checkout.finalizarPedido(alemanhaEssencial));
    }
}
