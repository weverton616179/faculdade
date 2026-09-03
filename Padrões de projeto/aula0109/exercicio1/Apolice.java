import java.time.LocalDate;
import java.util.List;

/**
 * Produto abstrato (Factory Method).
 * Declara os metodos comuns a toda apolice:
 * calculo de premio, validacao de cobertura, listagem de documentos
 * e geracao de resumo padronizado.
 */
public abstract class Apolice {

    protected String numero;
    protected String segurado;
    protected LocalDate dataEmissao;
    protected double premio;

    // Contador estatico: garante numero unico em todo o sistema (RNF02)
    private static int contador = 0;

    // Prefixo do numero conforme o tipo: AUTO-, RES-, VID-, VIA-
    public abstract String getPrefixo();

    // Calcula o premio conforme as regras de cada linha de produto
    public abstract double calcularPremio();

    // Retorna null se a contratacao for valida, ou o motivo da rejeicao
    public abstract String validarCobertura();

    // Lista os documentos exigidos para a contratacao
    public abstract List<String> getDocumentosExigidos();

    // Atribui o numero unico prefixado (usado somente apos a validacao)
    public void atribuirNumero() {
        contador++;
        this.numero = getPrefixo() + contador;
    }

    public void setDataEmissao(LocalDate dataEmissao) {
        this.dataEmissao = dataEmissao;
    }

    public void setPremio(double premio) {
        this.premio = premio;
    }

    /**
     * Resumo textual padronizado (RNF03):
     * numero da apolice, segurado, data de emissao, premio e documentos exigidos.
     */
    public String gerarResumo() {
        StringBuilder sb = new StringBuilder();
        sb.append("=== RESUMO DA APOLICE ===\n");
        sb.append("Numero da apolice: ").append(numero).append("\n");
        sb.append("Segurado: ").append(segurado).append("\n");
        sb.append("Data de emissao: ").append(dataEmissao).append("\n");
        sb.append("Premio: R$ ").append(String.format("%.2f", premio)).append("\n");
        sb.append("Documentos exigidos: ")
          .append(String.join(", ", getDocumentosExigidos()))
          .append("\n");
        return sb.toString();
    }
}
