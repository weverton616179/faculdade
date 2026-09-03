import java.time.LocalDate;

/**
 * Criador abstrato (Factory Method).
 * Declara o metodo fabrica abstrato criarApolice() e um metodo concreto e
 * FINAL (processarContratacao) que processa a contratacao usando apenas a
 * abstracao do produto retornado pelo metodo fabrica.
 */
public abstract class ApoliceFactory {

    // METODO FABRICA: cada subclasse instancia o produto correspondente
    public abstract Apolice criarApolice();

    /**
     * Algoritmo de processamento centralizado na superclasse.
     * Nao decide o tipo de produto em nenhum momento.
     */
    public final String processarContratacao() {
        Apolice apolice = criarApolice();

        // Validacao de cobertura
        String motivo = apolice.validarCobertura();
        if (motivo != null) {
            return "Contratacao REJEITADA - " + motivo;
        }

        // Emissao: numero unico prefixado, data e premio calculado
        apolice.atribuirNumero();
        apolice.setDataEmissao(LocalDate.now());
        apolice.setPremio(apolice.calcularPremio());

        return apolice.gerarResumo();
    }
}
