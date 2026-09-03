/**
 * Cliente / Finalizador de pedido (RNF02).
 * Depende apenas da abstracao CheckoutFactory: nao contem nenhuma estrutura
 * condicional que decida, pais a pais, qual documento fiscal, processador de
 * pagamento ou etiqueta utilizar. Gera o relatorio padronizado (RNF03).
 */
public class Checkout {

    public String finalizarPedido(CheckoutFactory factory) {
        DocumentoFiscal documento = factory.criarDocumentoFiscal();
        Pagamento pagamento = factory.criarPagamento();
        EtiquetaEnvio etiqueta = factory.criarEtiqueta();

        StringBuilder sb = new StringBuilder();
        sb.append("========== RELATORIO DO PEDIDO ==========\n");
        sb.append("[DOCUMENTO FISCAL]\n");
        sb.append(documento.gerar()).append("\n\n");
        sb.append("[PAGAMENTO]\n");
        sb.append(pagamento.processar()).append("\n\n");
        sb.append("[ETIQUETA DE ENVIO]\n");
        sb.append(etiqueta.gerar()).append("\n");
        sb.append("=========================================\n");
        return sb.toString();
    }
}
