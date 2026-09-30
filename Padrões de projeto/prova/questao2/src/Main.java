public class Main {

    public static void main(String[] args) {
        System.out.println("--");
        System.out.println("- rede hoteleria - confirmacao de reservas -");
        System.out.println("--\n");

        ConfirmacaoReserva reservaBrasil = new ConfirmacaoReserva(
                new PaisFactoryBrasil(),
                "Edinaldo pereira",
                "123.456.789-00",
                "10/03/2026 a 14/03/2026",
                2000.00);
        System.out.println(reservaBrasil.confirmar());

        ConfirmacaoReserva reservaPortugal = new ConfirmacaoReserva(
                new PaisFactoryPortugal(),
                "Marcos golveia",
                "245 678 901",
                "22/04/2026 a 26/04/2026",
                1800.00);
        System.out.println(reservaPortugal.confirmar());
    }
}
