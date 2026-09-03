/**
 * Criador concreto (Factory Method) da linha de produto Vida.
 */
public class ApoliceVidaFactory extends ApoliceFactory {

    private final String segurado;
    private final int idade;
    private final double capitalSegurado;
    private final boolean fumante;
    private final boolean temAtestadoMedico;

    public ApoliceVidaFactory(String segurado, int idade, double capitalSegurado,
                              boolean fumante, boolean temAtestadoMedico) {
        this.segurado = segurado;
        this.idade = idade;
        this.capitalSegurado = capitalSegurado;
        this.fumante = fumante;
        this.temAtestadoMedico = temAtestadoMedico;
    }

    @Override
    public Apolice criarApolice() {
        return new ApoliceVida(segurado, idade, capitalSegurado,
                               fumante, temAtestadoMedico);
    }
}
