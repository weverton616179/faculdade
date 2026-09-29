# =====================================================================
#  gerar_pdf_material.ps1
#  Converte os materiais de consulta (.md) em HTML estilizado e PDF.
#  O PDF e util para imprimir ou consultar offline (sem internet na prova).
#
#  Uso:  pwsh -File .\gerar_pdf_material.ps1
# =====================================================================

$ErrorActionPreference = 'Stop'
$ws     = Split-Path -Parent $MyInvocation.MyCommand.Path
$mdDir  = Join-Path $ws 'material_consulta_prova'
$outDir = Join-Path $mdDir 'pdf'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

# ------------------------------------------------------------------ CSS
$css = @'
:root { --fg:#1a1a1a; --muted:#555; --line:#d0d7de; --accent:#0b5394; --code:#f6f8fa; }
* { box-sizing: border-box; }
body { font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
       color: var(--fg); background:#fff; margin:0; padding:32px 40px;
       line-height:1.55; font-size:15px; }
h1 { font-size:1.75em; color:var(--accent); border-bottom:3px solid var(--accent);
     padding-bottom:.3em; margin:0 0 .8em; }
h2 { font-size:1.35em; color:var(--accent); border-bottom:1px solid var(--line);
     padding-bottom:.2em; margin:1.6em 0 .6em; page-break-after:avoid; }
h3 { font-size:1.12em; margin:1.3em 0 .5em; color:#12395f; page-break-after:avoid; }
h4 { font-size:1em; margin:1.1em 0 .4em; color:#12395f; }
p, li { margin:.45em 0; }
ul, ol { padding-left:1.5em; }
code { font-family:Consolas,"Cascadia Mono","Courier New",monospace;
       background:var(--code); padding:.12em .35em; border-radius:3px; font-size:.9em; }
pre { background:var(--code); border:1px solid var(--line); border-left:4px solid var(--accent);
      border-radius:5px; padding:12px 14px; overflow-x:auto; page-break-inside:avoid; }
pre code { background:none; padding:0; font-size:.84em; line-height:1.42; }
table { border-collapse:collapse; width:100%; margin:1em 0; font-size:.92em; page-break-inside:avoid; }
th, td { border:1px solid var(--line); padding:6px 9px; text-align:left; vertical-align:top; }
th { background:#eef3f9; font-weight:600; }
tr:nth-child(even) td { background:#fafbfc; }
blockquote { margin:1em 0; padding:.6em 1em; border-left:4px solid #f0a500;
             background:#fffbf0; color:#333; }
blockquote p { margin:.3em 0; }
hr { border:none; border-top:1px solid var(--line); margin:1.8em 0; }
a { color:var(--accent); text-decoration:none; }
.doc-header { font-size:.8em; color:var(--muted); margin-bottom:1.5em;
              border-bottom:1px dashed var(--line); padding-bottom:.5em; }
@media print {
  body { padding:0; font-size:11.5px; }
  pre { font-size:9.5px; }
  h1 { font-size:1.5em; }
  h2 { font-size:1.2em; }
  @page { margin:14mm 12mm; }
}
'@

# --------------------------------------------------------------- HELPERS
$script:Esc = {
    param([string]$s)
    if ($null -eq $s) { return '' }
    $s = $s -replace '&', '&amp;'
    $s = $s -replace '<', '&lt;'
    $s = $s -replace '>', '&gt;'
    return $s
}

$script:Inline = {
    param([string]$s)
    $s = & $script:Esc $s
    $s = [regex]::Replace($s, '`([^`]+)`', '<code>$1</code>')
    $s = [regex]::Replace($s, '\*\*([^*]+)\*\*', '<strong>$1</strong>')
    $s = [regex]::Replace($s, '(?<!\*)\*([^*\n]+)\*(?!\*)', '<em>$1</em>')
    $s = [regex]::Replace($s, '~~([^~]+)~~', '<del>$1</del>')
    $s = [regex]::Replace($s, '\[([^\]]+)\]\(([^)]+)\)', '<a href="$2">$1</a>')
    return $s
}

# Detecta se a linha terminou com formatacao embutida ABERTA
# (numero impar de ** ou de `), o que significa que o markdown foi
# quebrado no meio do negrito/codigo e a proxima linha deve ser unida.
function Test-InlineAberto {
    param([string]$Texto)
    $negritos = ([regex]::Matches($Texto, '\*\*')).Count
    $barras   = ([regex]::Matches($Texto, '`')).Count
    return (($negritos % 2) -ne 0) -or (($barras % 2) -ne 0)
}

function Convert-MdToHtml {
    param([string]$Markdown, [string]$Titulo)

    # ---- PRE-PROCESSAMENTO 1: unir citacoes (>) multi-linha -----------
    $originais = $Markdown -split "`r?`n"
    $etapa1 = New-Object System.Collections.ArrayList
    $buffer = $null
    foreach ($l in $originais) {
        if ($l -match '^\s*>\s?(.*)$') {
            $conteudo = $Matches[1].Trim()
            if ($null -eq $buffer) { $buffer = $conteudo }
            elseif ($conteudo -eq '') { $buffer += "`n>" }
            else { $buffer += ' ' + $conteudo }
            continue
        }
        if ($null -ne $buffer) { [void]$etapa1.Add('> ' + $buffer); $buffer = $null }
        [void]$etapa1.Add($l)
    }
    if ($null -ne $buffer) { [void]$etapa1.Add('> ' + $buffer) }

    # ---- PRE-PROCESSAMENTO 2: unir linhas de paragrafo/item que foram
    #      QUEBRADAS no meio de **negrito** ou `codigo` embutido.
    #      Sem isto, o negrito que atravessa a quebra de linha nao e
    #      reconhecido e os asteriscos aparecem literais no PDF.
    $linhas = New-Object System.Collections.ArrayList
    $emBloco = $false
    $acumulado = $null
    foreach ($l in $etapa1) {
        $t = $l.TrimEnd()

        if (-not $emBloco -and $t -match '^(`{3,})') { $emBloco = $true }
        elseif ($emBloco -and $t -match '^(`{3,})\s*$') { $emBloco = $false }

        if ($null -ne $acumulado) {
            $acumulado = $acumulado + ' ' + $t.Trim()
            if (-not (Test-InlineAberto $acumulado)) { [void]$linhas.Add($acumulado); $acumulado = $null }
            continue
        }

        # nao iniciar acumulo dentro de bloco de codigo nem em linha vazia
        if ($t.Trim() -eq '' -or $t -match '^(`{3,})') { [void]$linhas.Add($l); continue }

        if ((Test-InlineAberto $t) -and -not $emBloco) { $acumulado = $t; continue }

        [void]$linhas.Add($l)
    }
    if ($null -ne $acumulado) { [void]$linhas.Add($acumulado) }
    # ------------------------------------------------------------------

    $sb      = New-Object System.Text.StringBuilder
    $inCode  = $false
    $fence   = 0
    $inList  = $false
    $inTable = $false

    foreach ($linha in $linhas) {
        $trim = $linha.TrimEnd()

        # --- blocos de codigo (aceita ``` e ```` aninhados) ---
        if ($trim -match '^(`{3,})(.*)$') {
            $n    = $Matches[1].Length
            $lang = $Matches[2].Trim()
            if (-not $inCode) {
                if ($inTable) { [void]$sb.AppendLine('</table>'); $inTable = $false }
                if ($inList)  { [void]$sb.AppendLine('</ul>');    $inList  = $false }
                $cls = if ($lang) { " class=`"lang-$lang`"" } else { '' }
                [void]$sb.AppendLine("<pre$cls><code>")
                $inCode = $true; $fence = $n
            } elseif ($n -ge $fence -and $lang -eq '') {
                [void]$sb.AppendLine('</code></pre>')
                $inCode = $false; $fence = 0
            } else {
                [void]$sb.AppendLine((& $script:Esc $linha))
            }
            continue
        }
        if ($inCode) { [void]$sb.AppendLine((& $script:Esc $linha)); continue }

        # --- linha vazia ---
        if ([string]::IsNullOrWhiteSpace($trim)) {
            if ($inTable) { [void]$sb.AppendLine('</table>'); $inTable = $false }
            if ($inList)  { [void]$sb.AppendLine('</ul>');    $inList  = $false }
            continue
        }

        # --- tabela ---
        if ($trim -match '^\s*\|.*\|\s*$') {
            $cells = @(($trim.Trim().Trim('|') -split '\|') | ForEach-Object { $_.Trim() })
            $isSep = (@($cells | Where-Object { $_ -notmatch '^:?-{2,}:?$' }).Count -eq 0)
            if ($isSep) { continue }
            if (-not $inTable) {
                if ($inList) { [void]$sb.AppendLine('</ul>'); $inList = $false }
                [void]$sb.AppendLine('<table>')
                $inTable = $true
                $tag = 'th'
            } else { $tag = 'td' }
            $linhaHtml = '<tr>' + (($cells | ForEach-Object { "<$tag>$(& $script:Inline $_)</$tag>" }) -join '') + '</tr>'
            [void]$sb.AppendLine($linhaHtml)
            continue
        } elseif ($inTable) { [void]$sb.AppendLine('</table>'); $inTable = $false }

        # --- titulos ---
        if ($trim -match '^(#{1,6})\s+(.*)$') {
            if ($inList) { [void]$sb.AppendLine('</ul>'); $inList = $false }
            $nivel = $Matches[1].Length
            [void]$sb.AppendLine("<h$nivel>$(& $script:Inline $Matches[2])</h$nivel>")
            continue
        }

        # --- linha horizontal ---
        if ($trim -match '^\s*(-{3,}|\*{3,}|_{3,})\s*$') {
            if ($inList) { [void]$sb.AppendLine('</ul>'); $inList = $false }
            [void]$sb.AppendLine('<hr>')
            continue
        }

        # --- citacao ---
        if ($trim -match '^\s*>\s?(.*)$') {
            if ($inList) { [void]$sb.AppendLine('</ul>'); $inList = $false }
            [void]$sb.AppendLine("<blockquote><p>$(& $script:Inline $Matches[1])</p></blockquote>")
            continue
        }

        # --- listas ---
        if ($trim -match '^\s*(?:[-*+]|\d+[.)])\s+(.*)$') {
            if (-not $inList) { [void]$sb.AppendLine('<ul>'); $inList = $true }
            [void]$sb.AppendLine("<li>$(& $script:Inline $Matches[1])</li>")
            continue
        }
        if ($inList) { [void]$sb.AppendLine('</ul>'); $inList = $false }

        # --- paragrafo ---
        [void]$sb.AppendLine("<p>$(& $script:Inline $trim)</p>")
    }

    if ($inCode)  { [void]$sb.AppendLine('</code></pre>') }
    if ($inTable) { [void]$sb.AppendLine('</table>') }
    if ($inList)  { [void]$sb.AppendLine('</ul>') }

    $data = Get-Date -Format 'dd/MM/yyyy HH:mm'
    $html = @"
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>$Titulo</title>
<style>
$css
</style>
</head>
<body>
<div class="doc-header">Padroes de Projeto &mdash; Material de consulta para a prova &nbsp;|&nbsp; Prof. Escobar &nbsp;|&nbsp; gerado em $data</div>
$($sb.ToString())
</body>
</html>
"@
    return $html
}

# --------------------------------------------------------------- CHROME
function Find-Chrome {
    foreach ($p in @(
        "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
        "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
        "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe",
        "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
        "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe")) {
        if ($p -and (Test-Path $p)) { return $p }
    }
    return $null
}
$chrome = Find-Chrome
if ($chrome) { Write-Host "Navegador para PDF: $chrome" -ForegroundColor Cyan } 
else         { Write-Host 'Chrome/Edge nao encontrado: gerando apenas HTML.' -ForegroundColor Yellow }

# ------------------------------------------------------------------ MAIN
$arquivos = Get-ChildItem (Join-Path $mdDir '*.md') | Sort-Object Name
$gerados  = @()

foreach ($f in $arquivos) {
    $md = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    $titulo = (($md -split "`r?`n") | Where-Object { $_ -match '^#\s' } | Select-Object -First 1)
    if ($titulo) { $titulo = $titulo -replace '^#\s*', '' } else { $titulo = $f.BaseName }

    $html = Convert-MdToHtml -Markdown $md -Titulo $titulo
    $htmlPath = Join-Path $outDir ($f.BaseName + '.html')
    [System.IO.File]::WriteAllText($htmlPath, $html, (New-Object System.Text.UTF8Encoding($false)))

    $kbHtml = [math]::Round((Get-Item $htmlPath).Length / 1KB, 1)
    $pdfInfo = 'sem PDF'
    if ($chrome) {
        $pdfPath = Join-Path $outDir ($f.BaseName + '.pdf')
        Remove-Item $pdfPath -Force -ErrorAction SilentlyContinue
        $uri = ([System.Uri]$htmlPath).AbsoluteUri
        # O Chrome escreve o progresso em stderr; silenciamos para nao poluir o console.
        $ErrorActionPreference = 'SilentlyContinue'
        & $chrome --headless --disable-gpu --no-pdf-header-footer --no-sandbox "--print-to-pdf=$pdfPath" $uri 2>&1 | Out-Null
        $ErrorActionPreference = 'Stop'
        for ($i = 0; $i -lt 20 -and -not (Test-Path $pdfPath); $i++) { Start-Sleep -Milliseconds 250 }
        if (Test-Path $pdfPath) {
            $pdfInfo = "PDF $([math]::Round((Get-Item $pdfPath).Length / 1KB, 1)) KB"
        } else { $pdfInfo = 'PDF FALHOU' }
    }
    Write-Host ("  {0,-42} HTML {1,7} KB | {2}" -f $f.BaseName, $kbHtml, $pdfInfo) -ForegroundColor Green
    $gerados += $f.BaseName
}

Write-Host ''
Write-Host "Material gerado em: $outDir" -ForegroundColor Cyan
Write-Host "$($gerados.Count) documento(s) processado(s)."
