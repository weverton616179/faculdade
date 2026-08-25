data class Produto(val nome: String, val preco: Double)

fun main() {
    val produtos = listOf(
        Produto("Notebook", 3500.0),
        Produto("Mouse", 50.0),
        Produto("Teclado", 120.0),
        Produto("Monitor", 900.0),
        Produto("Cabo USB", 25.0)
    )

    println("Acima de 100 reais: ${produtos.filter { it.preco > 100 }}")
    println("Nomes: ${produtos.map { it.nome }}")
    println("Preço total: ${produtos.sumOf { it.preco }}")
    println("Mais caro: ${produtos.maxByOrNull { it.preco }}")
    println("Ordenados por preço: ${produtos.sortedBy { it.preco }}")
}
