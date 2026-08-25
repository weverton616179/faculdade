fun main() {
    val temperaturas = doubleArrayOf(24.0, 26.5, 23.0, 28.0, 30.5, 22.0, 27.5)

    var maior = temperaturas[0]
    var menor = temperaturas[0]
    var soma = 0.0
    for (temp in temperaturas) {
        if (temp > maior) maior = temp
        if (temp < menor) menor = temp
        soma += temp
    }
    val media = soma / temperaturas.size

    println("Maior: $maior")
    println("Menor: $menor")
    println("Média: $media")

    println("Com funções prontas:")
    println("Maior: ${temperaturas.maxOrNull()}")
    println("Menor: ${temperaturas.minOrNull()}")
    println("Média: ${temperaturas.average()}")
}
