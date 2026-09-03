/**
 * Interface de produto: documento fiscal gerado no pedido.
 * Cada pais implementa o seu formato.
 */
public interface DocumentoFiscal {
    String gerar();
}
