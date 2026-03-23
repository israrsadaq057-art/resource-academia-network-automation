<#
.SYNOPSIS
    Export AD data to JSON for dashboard
    Resource Academia - Network/IT Administrator: Israr Sadaq
#>

$OutputFile = "C:\Users\sadaq\Resource-Academia-Network-Automation\docs\ad_data.json"
$ADDataFile = "C:\Users\sadaq\Resource-Academia-Network-Automation\ad_simulator\resource_academia_ad.json"

if (Test-Path $ADDataFile) {
    $adData = Get-Content $ADDataFile | ConvertFrom-Json
    
    # Transform data for dashboard
    $dashboardData = @{
        statistics = @{
            total_users = $adData.users.PSObject.Properties.Name.Count
            total_groups = $adData.groups.PSObject.Properties.Name.Count
            total_ous = $adData.ous.PSObject.Properties.Name.Count
            enabled_users = 0
            disabled_users = 0
        }
        departments = @{}
        groups = @()
        last_updated = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    }
    
    # Count enabled/disabled users
    foreach ($user in $adData.users.PSObject.Properties.Value) {
        if ($user.enabled) {
            $dashboardData.statistics.enabled_users++
        } else {
            $dashboardData.statistics.disabled_users++
        }
    }
    
    # Get departments
    $depts = @("IT", "Finance", "Marketing", "Teachers", "Students", "Admin")
    foreach ($dept in $depts) {
        $deptUsers = @()
        foreach ($user in $adData.users.PSObject.Properties.Value) {
            if ($user.department -eq $dept) {
                $deptUsers += @{
                    name = $user.full_name
                    title = $user.title
                    enabled = $user.enabled
                }
            }
        }
        $dashboardData.departments[$dept] = @{
            users_count = $deptUsers.Count
            users = $deptUsers
        }
    }
    
    # Get groups
    foreach ($group in $adData.groups.PSObject.Properties.Value) {
        $dashboardData.groups += @{
            name = $group.name
            members = $group.members.Count
            description = $group.description
        }
    }
    
    # Save to JSON
    $dashboardData | ConvertTo-Json -Depth 10 | Out-File $OutputFile
    Write-Host "[OK] Dashboard data exported to: $OutputFile" -ForegroundColor Green
    Write-Host "  Total Users: $($dashboardData.statistics.total_users)" -ForegroundColor Gray
    Write-Host "  Total Groups: $($dashboardData.statistics.total_groups)" -ForegroundColor Gray
} else {
    Write-Host "[ERROR] AD data file not found: $ADDataFile" -ForegroundColor Red
    Write-Host "Run the Python AD Simulator first: python ad_simulator\resource_academia_ad.py" -ForegroundColor Yellow
}