class Aluno(val nome: String) {
    val notas = mutableListOf<Double>()

    fun adicionarNota(nota: Double) {
        notas.add(nota)
    }

    fun calcularMedia(): Double =
        if (notas.isEmpty()) 0.0 else notas.average()

    fun estaAprovado(): Boolean = calcularMedia() >= MEDIA_APROVACAO

    companion object {
        const val MEDIA_APROVACAO = 6.0
    }
}

class Turma {
    private val alunos = mutableListOf<Aluno>()

    fun adicionarAluno(aluno: Aluno) {
        alunos.add(aluno)
    }

    fun mediaGeral(): Double =
        if (alunos.isEmpty()) 0.0 else alunos.map { it.calcularMedia() }.average()

    fun aprovados(): List<Aluno> = alunos.filter { it.estaAprovado() }

    fun melhorAluno(): Aluno? = alunos.maxByOrNull { it.calcularMedia() }
}

fun main() {
    val turma = Turma()

    val ana = Aluno("Ana")
    ana.adicionarNota(8.0)
    ana.adicionarNota(7.5)
    turma.adicionarAluno(ana)

    val bruno = Aluno("Bruno")
    bruno.adicionarNota(5.0)
    bruno.adicionarNota(4.5)
    turma.adicionarAluno(bruno)

    val carla = Aluno("Carla")
    carla.adicionarNota(9.0)
    carla.adicionarNota(10.0)
    turma.adicionarAluno(carla)

    println("Média geral: ${turma.mediaGeral()}")
    println("Aprovados: ${turma.aprovados().map { it.nome }}")
    println("Melhor aluno: ${turma.melhorAluno()?.nome}")
}
