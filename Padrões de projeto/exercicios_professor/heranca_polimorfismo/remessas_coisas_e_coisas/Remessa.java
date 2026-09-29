import java.util.ArrayList;
import java.util.List;

/**
 * O "método que recebe vários e diferentes produtos e retorna a estimativa
 * de custos de transporte" pedido no enunciado.
 *
 * Polimorfismo: a lista é de Produto (classe base). O método soma o frete
 * chamando produto.calcularFrete() — a JVM decide em tempo de execução qual
 * implementação usar (geral ou a sobrescrita do SuperServidor), sem nenhum
 * if/else por tipo de produto.
 */
public class Remessa {

    private final List<Produto> produtos = new ArrayList<>();

    public void adicionarProduto(Produto produto) {
        this.produtos.add(produto);
    }

    /** Retorna a estimativa de custo total de transporte da remessa. */
    public double estimarCustoTransporte() {
        double total = 0.0;
        for (Produto p : produtos) {
            total += p.calcularFrete();   // chamada polimórfica
        }
        return total;
    }

    public void imprimirDetalhamento() {
        System.out.println("========== COISAS & COISAS - ESTIMATIVA DE TRANSPORTE ==========");
        System.out.printf("%-14s %12s %14s %14s%n", "PRODUTO", "PESO (kg)", "VOLUME (m3)", "FRETE (R$)");
        System.out.println("-".repeat(60));
        for (Produto p : produtos) {
            System.out.printf("%-14s %12.3f %14.4f %14.2f%n",
                    p.getNome(), p.getPesoKg(), p.getVolumeM3(), p.calcularFrete());
        }
        System.out.println("-".repeat(60));
        System.out.printf("%-42s %14.2f%n", "CUSTO TOTAL ESTIMADO", estimarCustoTransporte());
        System.out.println("===============================================================");
    }
}
