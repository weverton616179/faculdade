/**
 * Interface de produto: processamento do pagamento.
 * Cada pais implementa o seu meio de pagamento.
 */
public interface Pagamento {
    String processar();
}
