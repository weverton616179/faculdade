/**
 * Fabrica abstrata (Abstract Factory).
 * Declara um metodo para criar cada artefato do pedido (documento fiscal,
 * pagamento e etiqueta de envio). Cada pais implementa os tres juntos,
 * garantindo que os artefatos de um pedido pertencam sempre ao mesmo pais.
 */
public interface CheckoutFactory {

    DocumentoFiscal criarDocumentoFiscal();

    Pagamento criarPagamento();

    EtiquetaEnvio criarEtiqueta();
}
