public interface PaisFactory {

    String getMoeda();

    ComprovanteFiscal criarComprovanteFiscal(String hospede, double valorDiarias);

    Pagamento criarPagamento(String hospede, double valorDiarias);

    Voucher criarVoucher(String hospede, String documentoHospede, String periodo);
}
