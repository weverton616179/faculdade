/**
 * Classe de teste do sistema de remessas da Coisas & Coisas.
 *
 * Os três produtos são enviados para a MESMA remessa, comprovando que o
 * método aceita "vários e diferentes produtos".
 */
public class MainRemessa {

    public static void main(String[] args) {

        Remessa remessa = new Remessa();
        remessa.adicionarProduto(new MiniPC());
        remessa.adicionarProduto(new SoundBar());
        remessa.adicionarProduto(new SuperServidor());

        remessa.imprimirDetalhamento();

        System.out.println();
        System.out.println("=== MEMORIA DE CALCULO (regra geral: R$ 0,80/kg + R$ 1,00/m3) ===");
        System.out.println("MiniPC        500 g  = 0,500 kg  |  200 cm3    = 0,000200 m3");
        System.out.println("  0,500 x 0,80 = 0,40    +  0,000200 x 1,00 = 0,0002   => R$ 0,40");
        System.out.println("SoundBar      670 g  = 0,670 kg  |  8000 cm3   = 0,008000 m3");
        System.out.println("  0,670 x 0,80 = 0,536   +  0,008000 x 1,00 = 0,008    => R$ 0,54");
        System.out.println("SuperServidor 3800 g = 3,800 kg  |  120000 cm3 = 0,120000 m3");
        System.out.println("  3,800 x 0,80 = 3,04    +  0,120000 x 1,00 = 0,12     => R$ 3,16");
        System.out.println("  + seguro de 30% do preco: 0,30 x 30000,00 = 9000,00  => R$ 9.003,16");
        System.out.println();
        System.out.println("TOTAL DA REMESSA = 0,40 + 0,54 + 9003,16 = R$ 9.004,10");

        System.out.println();
        System.out.println("=== PROVA DO REAPROVEITAMENTO (polimorfismo) ===");
        System.out.println("A classe Remessa nunca pergunta 'que produto e este?'.");
        System.out.println("Ela apenas chama calcularFrete(). O SuperServidor responde");
        System.out.println("diferente porque sobrescreveu o metodo com @Override.");

        Produto p = new SuperServidor();   // referencia da classe base
        System.out.printf("%nReferencia Produto -> SuperServidor: frete = R$ %.2f%n", p.calcularFrete());
    }
}
