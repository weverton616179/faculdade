public class PaisFactoryBrasil implements PaisFactory {

    @Override
    public String getMoeda() {
        return "R$";
    }

    @Override
    public ComprovanteFiscal criarComprovanteFiscal(String hospede, double valorDiarias) {
        return new ComprovanteFiscalBrasil(hospede, valorDiarias);
    }

    @Override
    public Pagamento criarPagamento(String hospede, double valorDiarias) {
        return new PagamentoPix(hospede, "123.456.789-00", valorDiarias);
    }

    @Override
    public Voucher criarVoucher(String hospede, String documentoHospede, String periodo) {
        return new VoucherBrasil(hospede, documentoHospede, periodo);
    }
}
