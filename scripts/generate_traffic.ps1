Write-Host "Generating synthetic traffic to API Gateway (http://localhost:3000) for 1 minute..."
$endTime = (Get-Date).AddMinutes(1)

while ((Get-Date) -lt $endTime) {
    try {
        Invoke-RestMethod -Uri "http://localhost:3000/api/orders" -Method Get -ErrorAction SilentlyContinue | Out-Null
        Invoke-RestMethod -Uri "http://localhost:3000/api/payments" -Method Get -ErrorAction SilentlyContinue | Out-Null
    } catch {
        # Ignore errors if services are still booting
    }
    Start-Sleep -Seconds 1
}

Write-Host "Traffic generation complete!"
