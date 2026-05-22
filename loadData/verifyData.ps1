Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
$csvFile = ".csv"

if (-not (Test-Path $csvFile)) {
    Write-Host "Error: $csvFile not found!" -ForegroundColor Red
    exit
}

$studies = Import-Csv $csvFile

foreach ($row in $studies) {
    $id = $row.Accession
    $name = $row.Name

    # This is staging https://url/fhir/ResearchStudy/$id
    $url = ""

    try {
        $response = Invoke-WebRequest -Uri $url -Method Get -UseBasicParsing -ErrorAction Stop
        $status = $response.StatusCode
    }
    catch {
        # If the server returns 404 or other errors, it falls into this block
        $status = $_.Exception.Response.StatusCode.Value__
        if (-not $status) { $status = "Error/Offline" }
    }

    # Output results to the console
    if ($status -eq 200) {
        Write-Host "[FOUND]   ID: $id ($name)" -ForegroundColor Green
    } elseif ($status -eq 404) {
        Write-Host "[MISSING] ID: $id ($name)" -ForegroundColor Yellow
    } else {
        Write-Host "[STATUS $status] ID: $id ($name)" -ForegroundColor Red
    }
}
