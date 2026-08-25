fun main() {
    for (i in 10 downTo 1) {
        println(i)
    }
    println("Lançado!")

    val numero = 7
    for (i in 1..10) {
        println("$numero x $i = ${numero * i}")
    }

    println("Pares com step:")
    for (i in 2..20 step 2) {
        print("$i ")
    }
    println()

    println("Pares com if e %:")
    for (i in 1..20) {
        if (i % 2 == 0) {
            print("$i ")
        }
    }
    println()
}
