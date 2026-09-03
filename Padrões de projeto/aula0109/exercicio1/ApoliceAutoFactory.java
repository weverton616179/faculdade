/**
 * Criador concreto (Factory Method) da linha de produto Auto.
 * Sobrescreve o metodo fabrica para retornar a ApoliceAuto correspondente.
 */
public class ApoliceAutoFactory extends ApoliceFactory {

    private final String segurado;
    private final double valorFipe;
    private final int idadeCondutor;
    private final int anosHabilitacao;
    private final double coberturaTerceiros;

    public ApoliceAutoFactory(String segurado, double valorFipe, int idadeCondutor,
                              int anosHabilitacao, double coberturaTerceiros) {
        this.segurado = segurado;
        this.valorFipe = valorFipe;
        this.idadeCondutor = idadeCondutor;
        this.anosHabilitacao = anosHabilitacao;
        this.coberturaTerceiros = coberturaTerceiros;
    }

    @Override
    public Apolice criarApolice() {
        return new ApoliceAuto(segurado, valorFipe, idadeCondutor,
                               anosHabilitacao, coberturaTerceiros);
    }
}
