/**
 * Criador concreto (Factory Method) da linha de produto Viagem.
 */
public class ApoliceViagemFactory extends ApoliceFactory {

    private final String segurado;
    private final int diasViagem;
    private final boolean internacional;
    private final double coberturaMedicaUsd;
    private final boolean temPassaporte;

    public ApoliceViagemFactory(String segurado, int diasViagem, boolean internacional,
                                double coberturaMedicaUsd, boolean temPassaporte) {
        this.segurado = segurado;
        this.diasViagem = diasViagem;
        this.internacional = internacional;
        this.coberturaMedicaUsd = coberturaMedicaUsd;
        this.temPassaporte = temPassaporte;
    }

    @Override
    public Apolice criarApolice() {
        return new ApoliceViagem(segurado, diasViagem, internacional,
                                 coberturaMedicaUsd, temPassaporte);
    }
}
