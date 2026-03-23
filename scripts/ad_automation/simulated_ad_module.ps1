# Simulated Active Directory Module
# Resource Academia - Network/IT Administrator: Israr Sadaq

function Get-ADUser {
    param([string]$Identity, [string]$Filter)
    
    $users = @(
        [PSCustomObject]@{SamAccountName="israr.sadaq"; Name="Israr Sadaq"; Department="IT"; Title="Network Administrator"; Enabled=$true},
        [PSCustomObject]@{SamAccountName="ahmed.hassan"; Name="Ahmed Hassan"; Department="IT"; Title="System Administrator"; Enabled=$true},
        [PSCustomObject]@{SamAccountName="fatima.ali"; Name="Fatima Ali"; Department="IT"; Title="Help Desk Lead"; Enabled=$true},
        [PSCustomObject]@{SamAccountName="usman.malik"; Name="Usman Malik"; Department="IT"; Title="Network Engineer"; Enabled=$true},
        [PSCustomObject]@{SamAccountName="sara.khan"; Name="Sara Khan"; Department="IT"; Title="System Engineer"; Enabled=$true},
        [PSCustomObject]@{SamAccountName="omar.khan"; Name="Omar Khan"; Department="Finance"; Title="Finance Manager"; Enabled=$true},
        [PSCustomObject]@{SamAccountName="saima.akhtar"; Name="Saima Akhtar"; Department="Finance"; Title="Senior Accountant"; Enabled=$true},
        [PSCustomObject]@{SamAccountName="zain.malik"; Name="Zain Malik"; Department="Marketing"; Title="Marketing Manager"; Enabled=$true},
        [PSCustomObject]@{SamAccountName="ayesha.riaz"; Name="Ayesha Riaz"; Department="Marketing"; Title="Digital Marketing Specialist"; Enabled=$true}
    )
    
    if ($Identity) {
        return $users | Where-Object { $_.SamAccountName -like "*$Identity*" -or $_.Name -like "*$Identity*" }
    }
    elseif ($Filter -like "*IT*") {
        return $users | Where-Object { $_.Department -eq "IT" }
    }
    else {
        return $users
    }
}

function Get-ADGroupMember {
    param([string]$Identity)
    
    $groups = @{
        "IT_Admins" = @("israr.sadaq", "ahmed.hassan")
        "Network_Admins" = @("usman.malik")
        "Help_Desk" = @("fatima.ali")
        "Finance_Staff" = @("omar.khan", "saima.akhtar")
        "Marketing_Staff" = @("zain.malik", "ayesha.riaz")
    }
    
    if ($groups.ContainsKey($Identity)) {
        $members = @()
        foreach ($member in $groups[$Identity]) {
            $members += [PSCustomObject]@{
                SamAccountName = $member
                Name = $member -replace "\.", " " -replace "-", " " | ForEach-Object { (Get-Culture).TextInfo.ToTitleCase($_) }
                Department = "Unknown"
            }
        }
        return $members
    }
    return @()
}

Write-Host "="*60 -ForegroundColor Cyan
Write-Host "SIMULATED ACTIVE DIRECTORY MODULE LOADED" -ForegroundColor Yellow
Write-Host "Resource Academia - Network/IT Administrator: Israr Sadaq" -ForegroundColor Green
Write-Host "="*60 -ForegroundColor Cyan
Write-Host ""
Write-Host "Try these commands:" -ForegroundColor White
Write-Host "  Get-ADUser" -ForegroundColor Gray
Write-Host "  Get-ADUser -Identity israr" -ForegroundColor Gray
Write-Host "  Get-ADUser -Filter {Department -eq 'IT'}" -ForegroundColor Gray
Write-Host "  Get-ADGroupMember -Identity IT_Admins" -ForegroundColor Gray
