# =====================================================================
#  compilar_tudo.ps1
#  Compila e executa TODOS os exercícios de Padrões de Projeto.
#  Uso:  pwsh -File .\compilar_tudo.ps1
#        (ou botão direito > Executar com PowerShell)
# =====================================================================

$ErrorActionPreference = 'Continue'
$ws = Split-Path -Parent $MyInvocation.MyCommand.Path
$build = Join-Path $ws '_build'

# Descobre o JDK (PATH, JAVA_HOME ou instalações padrão do Windows)
function Find-JdkBin {
    $cands = @()
    if ($env:JAVA_HOME) { $cands += (Join-Path $env:JAVA_HOME 'bin') }
    $javacCmd = Get-Command javac -ErrorAction SilentlyContinue
    if ($javacCmd) { $cands += (Split-Path $javacCmd.Source -Parent) }
    foreach ($root in 'C:\Program Files\Java','C:\Program Files\Eclipse Adoptium','C:\Program Files\Microsoft','C:\Program Files\Amazon Corretto','C:\Program Files\Zulu') {
        if (Test-Path $root) {
            $cands += (Get-ChildItem $root -Directory -ErrorAction SilentlyContinue |
                       Sort-Object Name -Descending |
                       ForEach-Object { Join-Path $_.FullName 'bin' })
        }
    }
    foreach ($c in $cands) { if (Test-Path (Join-Path $c 'javac.exe')) { return $c } }
    return $null
}

$jdkBin = Find-JdkBin
if (-not $jdkBin) { Write-Host 'ERRO: JDK (javac) nao encontrado. Instale o JDK ou ajuste o PATH.' -ForegroundColor Red; exit 1 }
$javac = Join-Path $jdkBin 'javac.exe'
$java  = Join-Path $jdkBin 'java.exe'
Write-Host "JDK: $jdkBin" -ForegroundColor Cyan
& $javac -version
Write-Host ''

# id = nome da pasta em _build | src = pasta dos fontes | main = classe com main()
$exercicios = @(
    @{ id='ex1_apolices_factory_method';   src='aula0109\exercicio1';                                                     main='MainApolice'  },
    @{ id='ex2_checkout_abstract_factory'; src='aula0109\exercicio2';                                                     main='MainCheckout' },
    @{ id='ex3_funcionario_diretor';       src='exercicios_professor\heranca_polimorfismo\exemplo_funcionario';            main='Main'         },
    @{ id='ex4_remessas_coisas_e_coisas';  src='exercicios_professor\heranca_polimorfismo\remessas_coisas_e_coisas';       main='MainRemessa'  },
    @{ id='ex5_unile_disciplinas_aluno';   src='exercicios_professor\heranca_polimorfismo\unile';                          main='MainUniLE'    },
    @{ id='ex6_aula1808_unile_v1';         src='aula1808';                                                                 main='Main'         }
)

$resultado = @()
foreach ($ex in $exercicios) {
    $srcDir = Join-Path $ws $ex.src
    $outDir = Join-Path $build $ex.id
    if (-not (Test-Path $srcDir)) { Write-Host "IGNORADO (pasta ausente): $($ex.src)" -ForegroundColor Yellow; continue }

    Remove-Item $outDir -Recurse -Force -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Force -Path $outDir | Out-Null

    $fontes = (Get-ChildItem (Join-Path $srcDir '*.java')).FullName
    Write-Host "== $($ex.id) ==" -ForegroundColor Green
    & $javac -encoding UTF-8 -d $outDir $fontes
    $compilou = ($LASTEXITCODE -eq 0)

    $runExit = $null
    if ($compilou) {
        # Garante que acentos (ex.: "João") nao virem "?" na saida do console.
        # Usamos a variavel de ambiente porque o PowerShell quebra "-Dchave=valor".
        $env:JAVA_TOOL_OPTIONS = '-Dfile.encoding=UTF-8 -Dstdout.encoding=UTF-8 -Dstderr.encoding=UTF-8'
        $saida = & $java -cp $outDir $ex.main 2>&1 | ForEach-Object { $_.ToString() }
        $runExit = $LASTEXITCODE
        Remove-Item Env:\JAVA_TOOL_OPTIONS -ErrorAction SilentlyContinue
        # O JVM imprime "Picked up JAVA_TOOL_OPTIONS" no stderr: descartamos essa linha.
        $saida = $saida | Where-Object { $_ -notmatch 'Picked up JAVA_TOOL_OPTIONS' }
        $log = Join-Path $build "saida_$($ex.id).txt"
        [System.IO.File]::WriteAllLines($log, $saida, (New-Object System.Text.UTF8Encoding($false)))
        Write-Host "   compilou: SIM | execucao exit: $runExit | saida: _build\saida_$($ex.id).txt" -ForegroundColor Gray
    } else {
        Write-Host "   compilou: NAO" -ForegroundColor Red
    }

    $resultado += [pscustomobject]@{
        Exercicio = $ex.id
        Compilou  = $compilou
        Execucao  = $runExit
        ClasseMain= $ex.main
    }
}

Write-Host ''
Write-Host '================= RESUMO =================' -ForegroundColor Cyan
$resultado | Format-Table -AutoSize
$falhas = ($resultado | Where-Object { -not $_.Compilou -or $_.Execucao -ne 0 }).Count
if ($falhas -eq 0) {
    Write-Host 'TODOS OS EXERCICIOS COMPILARAM E EXECUTARAM COM SUCESSO.' -ForegroundColor Green
} else {
    Write-Host "$falhas exercicio(s) com problema." -ForegroundColor Red
    exit 1
}
