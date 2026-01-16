# --- CONFIGURATION ---
$rootPath = "F:\"
$dryRun = $false  # Set to $false to actually rename
# ---------------------

Write-Host "--- Starting Scan (Using LiteralPath) ---" -ForegroundColor Yellow

# Use -Recurse to find all files
$items = Get-ChildItem -LiteralPath $rootPath -Recurse | Where-Object { $_.Name -match '[^\x00-\x7F]' }

foreach ($item in $items) {
    $oldName = $item.Name
    
    # Strip non-ASCII (Emojis)
    $newName = $oldName -replace '[^\x00-\x7F]', ''
    
    # Clean up double spaces or leading/trailing dots/spaces
    $newName = $newName.Replace("  ", " ").Trim(" .")

    if ($newName -ne $oldName -and -not [string]::IsNullOrWhiteSpace($newName)) {
        $oldPath = $item.FullName
        
        if ($dryRun) {
            Write-Host "[DRY RUN] Would rename: '$oldName' -> '$newName'" -ForegroundColor Cyan
        } else {
            try {
                # Use -LiteralPath to handle the "!" and other special characters
                Move-Item -LiteralPath $oldPath -Destination (Join-Path $item.DirectoryName $newName) -ErrorAction Stop
                Write-Host "[SUCCESS] Renamed: $newName" -ForegroundColor Green
            } catch {
                Write-Host "[ERROR] Failed on $($oldName): $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    }
}