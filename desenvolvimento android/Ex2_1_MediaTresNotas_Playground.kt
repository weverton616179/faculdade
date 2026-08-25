fun main() {
    val nota1 = 8.5
    val nota2 = 7.0
    val nota3 = 6.0

    val media = (nota1 + nota2 + nota3) / 3
    val conceito = when {
        media >= 9 -> "A"
        media >= 7 -> "B"
        media >= 5 -> "C"
        else -> "D"
    }

    println("Média: %.2f".format(media))
    println("Conceito: $conceito")
}
