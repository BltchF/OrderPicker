function Get-Tree {
    param (
        [string]$Path = "..\..\..\2_order_picker",
        [string]$Indent = ""
    )

    $children = Get-ChildItem -Path $Path
    $children | ForEach-Object {
        if ($_.Name -ne "__pycache__" -and $_.Name -ne ".git") {
            if ($_ -eq $children[-1]) {
                # Last item
                if ($_.PSIsContainer) {
                    Write-Host ("{0}{1} {2}{3}" -f $Indent, [char]::ConvertFromUtf32(0x2514), [char]::ConvertFromUtf32(0x1F4C1), $_.Name)
                    Get-Tree -Path $_.FullName -Indent ("$Indent    ")
                } else {
                    Write-Host ("{0}{1} {2}{3}" -f $Indent, [char]::ConvertFromUtf32(0x2514), [char]::ConvertFromUtf32(0x1F4C4), $_.Name)
                }
            } else {
                # Not last item
                if ($_.PSIsContainer) {
                    Write-Host ("{0}{1} {2}{3}" -f $Indent, [char]::ConvertFromUtf32(0x251C), [char]::ConvertFromUtf32(0x1F4C1), $_.Name)
                    Get-Tree -Path $_.FullName -Indent ("$Indent" + [char]::ConvertFromUtf32(0x2502) + "   ")
                } else {
                    Write-Host ("{0}{1} {2}{3}" -f $Indent, [char]::ConvertFromUtf32(0x251C), [char]::ConvertFromUtf32(0x1F4C4), $_.Name)
                }
            }
        }
    }
}

Get-Tree