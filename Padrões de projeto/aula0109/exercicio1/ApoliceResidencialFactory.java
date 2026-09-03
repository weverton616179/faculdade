/**
 * Criador concreto (Factory Method) da linha de produto Residencial.
 */
public class ApoliceResidencialFactory extends ApoliceFactory {

    private final String segurado;
    private final double valorImovel;
    private final boolean altoPadrao;
    private final boolean temEscrituraOuContrato;

    public ApoliceResidencialFactory(String segurado, double valorImovel,
                                     boolean altoPadrao, boolean temEscrituraOuContrato) {
        this.segurado = segurado;
        this.valorImovel = valorImovel;
        this.altoPadrao = altoPadrao;
        this.temEscrituraOuContrato = temEscrituraOuContrato;
    }

    @Override
    public Apolice criarApolice() {
        return new ApoliceResidencial(segurado, valorImovel, altoPadrao,
                                      temEscrituraOuContrato);
    }
}
