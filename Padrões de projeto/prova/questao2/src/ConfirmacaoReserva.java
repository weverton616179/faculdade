public class ConfirmacaoReserva {

    private final PaisFactory pais;

    private final String hospede;

    private final String documentoHospede;

    private final String periodo;

    private final double valorDiarias;

    public ConfirmacaoReserva(PaisFactory pais, String hospede, String documentoHospede,
                              String periodo, double valorDiarias) {
        if (pais == null) {
            throw new IllegalArgumentException("A fabrica do pais e obrigatoria.");
        }
        this.pais = pais;
        this.hospede = hospede;
        this.documentoHospede = documentoHospede;
        this.periodo = periodo;
        this.valorDiarias = valorDiarias;
    }

    public String confirmar() {
        ComprovanteFiscal comprovante = pais.criarComprovanteFiscal(hospede, valorDiarias);
        Pagamento pagamento = pais.criarPagamento(hospede, valorDiarias);
        Voucher voucher = pais.criarVoucher(hospede, documentoHospede, periodo);

        StringBuilder sb = new StringBuilder();
        sb.append("- relatorio de reserva -\n");
        sb.append("hospede: ").append(hospede).append("\n");
        sb.append("periodo: ").append(periodo).append("\n");
        sb.append("valor das diarias: ").append(pais.getMoeda()).append(" ")
          .append(String.format("%.2f", valorDiarias)).append("\n");
        sb.append("------------------------------------------\n");
        sb.append("1 ").append(comprovante.gerar()).append("\n");
        sb.append("------------------------------------------\n");
        sb.append("2 ").append(pagamento.processar()).append("\n");
        sb.append("------------------------------------------\n");
        sb.append("3 ").append(voucher.gerar()).append("\n");
        sb.append("---------------\n");
        return sb.toString();
    }
}
