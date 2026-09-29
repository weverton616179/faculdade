/**
 * ATIVIDADE DOS SLIDES — Sistema de remessas da indústria Coisas & Coisas
 *
 * Enunciado:
 *   "O sistema de remessas da indústria Coisas & Coisas possui um método que
 *    recebe vários e diferentes produtos e retorna a estimativa de custos de
 *    transporte de acordo com o que foi recebido.
 *    Todos os produtos têm atributos peso (massa do produto embalado em
 *    gramas), volume da embalagem (em cm³) e um preço de comercialização.
 *    Todos os produtos têm um método que calcula frete com base em:
 *        R$ 0,80 por quilo de massa
 *        R$ 1,00 por metro cúbico de volume
 *    Produtos atuais:
 *        MiniPC        {peso: 500,   volume: 200,    preço: 5000}
 *        SoundBar      {peso: 670,   volume: 8000,   preço: 1800}
 *        SuperServidor {peso: 3800,  volume: 120000, preço: 30000}
 *          -> para este produto, o frete inclui uma taxa de seguro
 *             equivalente a 30% do seu preço
 *    Implemente com o máximo de reaproveitamento de código."
 *
 * DECISÕES DE PROJETO (reaproveitamento máximo):
 *  - A classe Produto NÃO é abstrata e já implementa calcularFrete() com a
 *    regra geral (R$ 0,80/kg + R$ 1,00/m³). Todo produto herda esse cálculo.
 *  - Apenas o SuperServidor sobrescreve o método, reaproveitando o cálculo
 *    da classe base com super.calcularFrete() e somando o seguro.
 *  - Constantes de tarifa ficam na classe base (SRP + sem números mágicos).
 *
 * CONVERSÕES DE UNIDADE (o ponto crítico do exercício):
 *    peso está em GRAMAS   -> quilos: dividir por 1000
 *    volume está em cm³    -> m³    : dividir por 1.000.000
 */
public class Produto {

    /** Tarifa por quilo de massa (R$). */
    public static final double TARIFA_POR_KG = 0.80;
    /** Tarifa por metro cúbico de volume (R$). */
    public static final double TARIFA_POR_M3 = 1.00;

    protected final String nome;
    protected final double pesoGramas;
    protected final double volumeCm3;
    protected final double preco;

    public Produto(String nome, double pesoGramas, double volumeCm3, double preco) {
        this.nome = nome;
        this.pesoGramas = pesoGramas;
        this.volumeCm3 = volumeCm3;
        this.preco = preco;
    }

    public String getNome()        { return nome; }
    public double getPesoGramas()  { return pesoGramas; }
    public double getVolumeCm3()   { return volumeCm3; }
    public double getPreco()       { return preco; }

    /** peso em quilos (gramas / 1000). */
    public double getPesoKg() {
        return pesoGramas / 1000.0;
    }

    /** volume em metros cúbicos (cm³ / 1.000.000). */
    public double getVolumeM3() {
        return volumeCm3 / 1_000_000.0;
    }

    /**
     * Cálculo do frete segundo a regra geral do enunciado.
     * Subclasses podem reaproveitar este resultado via super.calcularFrete().
     */
    public double calcularFrete() {
        return (getPesoKg() * TARIFA_POR_KG) + (getVolumeM3() * TARIFA_POR_M3);
    }

    @Override
    public String toString() {
        return String.format("%-14s peso=%7.0f g (%6.3f kg)  volume=%8.0f cm3 (%6.4f m3)  preco=R$ %10.2f",
                nome, pesoGramas, getPesoKg(), volumeCm3, getVolumeM3(), preco);
    }
}
