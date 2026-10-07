$ErrorActionPreference = "Stop"

$logFile = ".\output\incident_job.log"

Write-Host "Starting AI Incident Intelligence Job..."
Write-Host ""

try {
    $startTime = Get-Date

    Add-Content $logFile "[$startTime] Job started."

    Write-Host "Running incident analysis..."
    python .\incident_analysis.py

    if ($LASTEXITCODE -ne 0) {
        throw "Python incident analysis failed with exit code $LASTEXITCODE."
    }

    Write-Host ""
    Write-Host "Generating dashboard..."
    python .\dashboard_generator.py

    if ($LASTEXITCODE -ne 0) {
        throw "Dashboard generation failed with exit code $LASTEXITCODE."
    }

    $endTime = Get-Date

    Add-Content $logFile "[$endTime] Job completed successfully."

    Write-Host ""
    Write-Host "AI Incident Intelligence Job Completed."
    Write-Host "Report: .\output\incident_report.json"
    Write-Host "Dashboard: .\output\incident_dashboard.html"
    Write-Host "Log: $logFile"
}
catch {
    $errorTime = Get-Date

    Add-Content $logFile "[$errorTime] Job FAILED: $($_.Exception.Message)"

    Write-Host ""
    Write-Host "AI Incident Intelligence Job Failed."
    Write-Host "Check the log file: $logFile"

    exit 1
}