public class PaisFactoryPortugal implements PaisFactory {

    @Override
    public String getMoeda() {
        return "EUR";
    }

    @Override
    public ComprovanteFiscal criarComprovanteFiscal(String hospede, double valorDiarias) {
        return new ComprovanteFiscalPortugal(hospede, valorDiarias);
    }

    @Override
    public Pagamento criarPagamento(String hospede, double valorDiarias) {
        return new PagamentoMbWay(hospede, "245 678 901", valorDiarias);
    }

    @Override
    public Voucher criarVoucher(String hospede, String documentoHospede, String periodo) {
        return new VoucherPortugal(hospede, documentoHospede, periodo);
    }
}
