param(
    [Parameter(Mandatory)] [ValidateSet('wide', 'cutout', 'poster')] [string] $Mode,
    [Parameter(Mandatory)] [string] $Source,
    [Parameter(Mandatory)] [string] $Destination
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$sourcePath = (Resolve-Path -LiteralPath $Source).Path
$destinationPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Destination)
if ($sourcePath -eq $destinationPath -or [IO.File]::Exists($destinationPath)) {
    throw 'Choose a new destination and retain the source.'
}

$sourceImage = [Drawing.Bitmap]::new($sourcePath)
$outputImage = $null
$graphics = $null
try {
    $width = $sourceImage.Width
    $height = $sourceImage.Height
    $sourceBounds = [Drawing.Rectangle]::new(0, 0, $width, $height)
    if ($Mode -eq 'wide') {
        $unit = [Math]::Floor([Math]::Min($width / 16, $height / 9))
        $width = [int]($unit * 16)
        $height = [int]($unit * 9)
        $sourceBounds = [Drawing.Rectangle]::new(
            [int](($sourceImage.Width - $width) / 2), [int](($sourceImage.Height - $height) / 2), $width, $height)
    } elseif ($Mode -eq 'cutout') {
        if ($sourceImage.Width -ne $sourceImage.Height -or ![Drawing.Image]::IsAlphaPixelFormat($sourceImage.PixelFormat)) {
            throw 'The benchmark cutout source must be square and carry alpha.'
        }
        $width = 512
        $height = 512
    } elseif ($width -ge $height) {
        throw 'The poster requires a portrait source with reserved text space.'
    }

    $outputImage = [Drawing.Bitmap]::new($width, $height, [Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $graphics = [Drawing.Graphics]::FromImage($outputImage)
    $graphics.CompositingMode = [Drawing.Drawing2D.CompositingMode]::SourceCopy
    $graphics.InterpolationMode = [Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.DrawImage($sourceImage, [Drawing.Rectangle]::new(0, 0, $width, $height), $sourceBounds, [Drawing.GraphicsUnit]::Pixel)

    if ($Mode -eq 'poster') {
        $graphics.CompositingMode = [Drawing.Drawing2D.CompositingMode]::SourceOver
        $graphics.TextRenderingHint = [Drawing.Text.TextRenderingHint]::AntiAliasGridFit
        $brush = [Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(255, 246, 228))
        $format = [Drawing.StringFormat]::GenericTypographic
        $format.Alignment = [Drawing.StringAlignment]::Center
        $format.LineAlignment = [Drawing.StringAlignment]::Center
        $format.FormatFlags = $format.FormatFlags -bor [Drawing.StringFormatFlags]::NoWrap
        try {
            $lines = @(
                @{ Text = '달 기지에 오신 것을 환영합니다!'; Scale = 0.056; Y = 0.115 },
                @{ Text = '출입 안내 09:30'; Scale = 0.040; Y = 0.895 }
            )
            foreach ($line in $lines) {
                $font = [Drawing.Font]::new('Malgun Gothic', [single]($width * $line.Scale), [Drawing.FontStyle]::Bold, [Drawing.GraphicsUnit]::Pixel)
                try {
                    if ($font.FontFamily.Name -notin @('Malgun Gothic', '맑은 고딕') -or $graphics.MeasureString($line.Text, $font).Width -gt $width * 0.90) {
                        throw 'The poster lettering must fit on one line in Malgun Gothic.'
                    }
                    $graphics.DrawString($line.Text, $font, $brush, [Drawing.PointF]::new($width / 2, $height * $line.Y), $format)
                } finally {
                    $font.Dispose()
                }
            }
        } finally {
            $format.Dispose()
            $brush.Dispose()
        }
    }
    $graphics.Dispose()
    $graphics = $null
    $outputImage.Save($destinationPath, [Drawing.Imaging.ImageFormat]::Png)
} finally {
    if ($graphics) { $graphics.Dispose() }
    if ($outputImage) { $outputImage.Dispose() }
    $sourceImage.Dispose()
}
