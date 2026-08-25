fun main() {
    val nome = "Ana"
    val letra = 'a'

    var contador = 0
    for (c in nome.lowercase()) {
        if (c == letra) {
            contador++
        }
    }
    println("A letra '$letra' aparece $contador vezes no nome $nome")

    val ocorrencias = nome.lowercase().count { it == letra }
    println("Com count { }: $ocorrencias")
}
