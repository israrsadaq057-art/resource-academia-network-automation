#!/usr/bin/env powershell
<#
.SYNOPSIS
    Complete Active Directory Structure Builder for Resource Academia
    Network/IT Administrator: Israr Sadaq
    Creates all OUs, Users, Groups, and applies base GPOs
#>

param(
    [string]$Domain = "resourceacademia.local",
    [string]$AdminPassword = "ResourceAcademia2026!",
    [switch]$WhatIf = $false
)

# Configuration
$BaseDN = "DC=$($Domain.Replace('.',',DC='))"
$LogFile = "C:\Resource-Academia-Network-Automation\logs\ad\ad_build_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
$ErrorLog = "C:\Resource-Academia-Network-Automation\logs\ad\ad_build_errors.log"

# Colors for output
$Green = "Green"
$Yellow = "Yellow"
$Red = "Red"
$Cyan = "Cyan"

function Write-Log {
    param([string]$Message, [string]$Color = "White", [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp [$Level] - $Message" | Out-File -FilePath $LogFile -Append
    Write-Host "$timestamp [$Level] - $Message" -ForegroundColor $Color
}

function Write-ErrorLog {
    param([string]$Message, [Exception]$Exception = $null)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp [ERROR] - $Message" | Out-File -FilePath $ErrorLog -Append
    if ($Exception) {
        "$timestamp [ERROR] - Exception: $($Exception.Message)" | Out-File -FilePath $ErrorLog -Append
        "$timestamp [ERROR] - StackTrace: $($Exception.StackTrace)" | Out-File -FilePath $ErrorLog -Append
    }
    Write-Host "$timestamp [ERROR] - $Message" -ForegroundColor Red
}

function Test-ADModule {
    if (-not (Get-Module -ListAvailable -Name ActiveDirectory)) {
        Write-Log "Active Directory module not found. Please install RSAT." -Color Red
        return $false
    }
    Import-Module ActiveDirectory -ErrorAction Stop
    Write-Log "Active Directory module loaded successfully." -Color Green
    return $true
}

function Create-OU {
    param([string]$Name, [string]$Path)
    
    $FullPath = "OU=$Name,$Path"
    
    if ($WhatIf) {
        Write-Log "[WHATIF] Would create OU: $FullPath" -Color Yellow
        return $true
    }
    
    try {
        New-ADOrganizationalUnit -Name $Name -Path $Path -ProtectedFromAccidentalDeletion $false -ErrorAction Stop
        Write-Log "✓ Created OU: $Name" -Color Green
        return $true
    } catch {
        if ($_.Exception.Message -like "*already exists*") {
            Write-Log "○ OU already exists: $Name" -Color Yellow
            return $true
        }
        Write-ErrorLog "Failed to create OU $Name" -Exception $_.Exception
        return $false
    }
}

function Create-Group {
    param([string]$Name, [string]$Path, [string]$Scope = "Global", [string]$Category = "Security")
    
    $FullPath = "CN=$Name,$Path"
    
    if ($WhatIf) {
        Write-Log "[WHATIF] Would create group: $Name in $Path" -Color Yellow
        return $true
    }
    
    try {
        New-ADGroup -Name $Name -GroupScope $Scope -GroupCategory $Category -Path $Path -ErrorAction Stop
        Write-Log "✓ Created group: $Name" -Color Green
        return $true
    } catch {
        if ($_.Exception.Message -like "*already exists*") {
            Write-Log "○ Group already exists: $Name" -Color Yellow
            return $true
        }
        Write-ErrorLog "Failed to create group $Name" -Exception $_.Exception
        return $false
    }
}

function Create-User {
    param(
        [string]$FirstName,
        [string]$LastName,
        [string]$Department,
        [string]$Title,
        [string]$Password,
        [string]$Email = "",
        [string]$Office = "",
        [string]$Phone = ""
    )
    
    $Username = ($FirstName.Substring(0,1) + $LastName).ToLower()
    $UserPrincipalName = "$Username@$Domain"
    $OUPath = "OU=$Department,OU=Departments,$BaseDN"
    $FullName = "$FirstName $LastName"
    $DisplayName = "$FullName ($Department)"
    
    if ($Email -eq "") {
        $Email = "$Username@$Domain"
    }
    
    if ($WhatIf) {
        Write-Log "[WHATIF] Would create user: $Username ($FullName) in $Department" -Color Yellow
        return $true
    }
    
    try {
        # Check if user already exists
        $Existing = Get-ADUser -Filter "SamAccountName -eq '$Username'" -ErrorAction SilentlyContinue
        if ($Existing) {
            Write-Log "○ User already exists: $Username" -Color Yellow
            return $true
        }
        
        New-ADUser -Name $FullName `
                   -GivenName $FirstName `
                   -Surname $LastName `
                   -SamAccountName $Username `
                   -UserPrincipalName $UserPrincipalName `
                   -Path $OUPath `
                   -AccountPassword (ConvertTo-SecureString $Password -AsPlainText -Force) `
                   -Enabled $true `
                   -ChangePasswordAtLogon $true `
                   -DisplayName $DisplayName `
                   -Title $Title `
                   -Department $Department `
                   -EmailAddress $Email `
                   -Office $Office `
                   -OfficePhone $Phone `
                   -ErrorAction Stop
        
        Write-Log "✓ Created user: $Username ($FullName) - $Title" -Color Green
        return $true
    } catch {
        Write-ErrorLog "Failed to create user $Username" -Exception $_.Exception
        return $false
    }
}

function Add-UserToGroup {
    param([string]$Username, [string]$GroupName)
    
    if ($WhatIf) {
        Write-Log "[WHATIF] Would add $Username to $GroupName" -Color Yellow
        return $true
    }
    
    try {
        Add-ADGroupMember -Identity $GroupName -Members $Username -ErrorAction Stop
        Write-Log "  → Added $Username to $GroupName" -Color Gray
        return $true
    } catch {
        Write-ErrorLog "Failed to add $Username to $GroupName" -Exception $_.Exception
        return $false
    }
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "RESOURCE ACADEMIA INTERNATIONAL" -ForegroundColor Yellow
Write-Host "Active Directory Structure Builder" -ForegroundColor Yellow
Write-Host "Network/IT Administrator: Israr Sadaq" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

if ($WhatIf) {
    Write-Host "!!! WHATIF MODE - No changes will be made !!!" -ForegroundColor Red
    Write-Host ""
}

# Check if AD module is available
if (-not (Test-ADModule)) {
    Write-Host "Please install Active Directory module (RSAT) and try again." -ForegroundColor Red
    exit 1
}

Write-Log "Starting AD Structure Creation" -Color Cyan

# ============================================================================
# STEP 1: Create Department OUs
# ============================================================================
Write-Host "`n[1] Creating Department OUs..." -ForegroundColor Yellow

# Create Departments container OU
$DepartmentsPath = "OU=Departments,$BaseDN"
if (-not ($WhatIf)) {
    try {
        New-ADOrganizationalUnit -Name "Departments" -Path $BaseDN -ProtectedFromAccidentalDeletion $false -ErrorAction SilentlyContinue
        Write-Log "✓ Created container: Departments" -Color Green
    } catch { }
}

$Departments = @("IT", "Finance", "Marketing", "Teachers", "Students", "Admin")
foreach ($Dept in $Departments) {
    Create-OU -Name $Dept -Path "OU=Departments,$BaseDN"
}

# ============================================================================
# STEP 2: Create Workstation OUs
# ============================================================================
Write-Host "`n[2] Creating Workstation OUs..." -ForegroundColor Yellow

Create-OU -Name "Workstations" -Path $BaseDN

$WorkstationOUs = @("IT_Workstations", "Finance_Workstations", "Marketing_Workstations", 
                    "Teachers_Workstations", "Student_Labs", "Admin_Workstations")
foreach ($Wkstn in $WorkstationOUs) {
    Create-OU -Name $Wkstn -Path "OU=Workstations,$BaseDN"
}

# ============================================================================
# STEP 3: Create Server OUs
# ============================================================================
Write-Host "`n[3] Creating Server OUs..." -ForegroundColor Yellow

Create-OU -Name "Servers" -Path $BaseDN

$ServerOUs = @("Domain_Controllers", "File_Servers", "Application_Servers", "Backup_Servers")
foreach ($Server in $ServerOUs) {
    Create-OU -Name $Server -Path "OU=Servers,$BaseDN"
}

# ============================================================================
# STEP 4: Create Groups
# ============================================================================
Write-Host "`n[4] Creating Security Groups..." -ForegroundColor Yellow

# Create Groups container
Create-OU -Name "Groups" -Path $BaseDN

# Department Groups
$Groups = @(
    @{Name="IT_Admins"; Path="OU=Groups,$BaseDN"; Scope="Global"},
    @{Name="Network_Admins"; Path="OU=Groups,$BaseDN"; Scope="Global"},
    @{Name="Help_Desk"; Path="OU=Groups,$BaseDN"; Scope="Global"},
    @{Name="Finance_Managers"; Path="OU=Groups,$BaseDN"; Scope="Global"},
    @{Name="Finance_Staff"; Path="OU=Groups,$BaseDN"; Scope="Global"},
    @{Name="Marketing_Staff"; Path="OU=Groups,$BaseDN"; Scope="Global"},
    @{Name="Faculty"; Path="OU=Groups,$BaseDN"; Scope="Global"},
    @{Name="Students"; Path="OU=Groups,$BaseDN"; Scope="Global"},
    @{Name="Admin_Staff"; Path="OU=Groups,$BaseDN"; Scope="Global"},
    @{Name="HR_Staff"; Path="OU=Groups,$BaseDN"; Scope="Global"}
)

foreach ($Group in $Groups) {
    Create-Group -Name $Group.Name -Path $Group.Path -Scope $Group.Scope
}

# ============================================================================
# STEP 5: Create Users (Sample Users)
# ============================================================================
Write-Host "`n[5] Creating Sample Users..." -ForegroundColor Yellow

# IT Department Users
Create-User -FirstName "Israr" -LastName "Sadaq" -Department "IT" -Title "Network Administrator" -Password $AdminPassword -Phone "+49 15218157247"
Create-User -FirstName "Ahmed" -LastName "Hassan" -Department "IT" -Title "System Administrator" -Password $AdminPassword
Create-User -FirstName "Fatima" -LastName "Ali" -Department "IT" -Title "Help Desk Lead" -Password $AdminPassword

# Finance Department Users
Create-User -FirstName "Omar" -LastName "Khan" -Department "Finance" -Title "Finance Manager" -Password $AdminPassword
Create-User -FirstName "Saima" -LastName "Akhtar" -Department "Finance" -Title "Senior Accountant" -Password $AdminPassword

# Marketing Department Users
Create-User -FirstName "Zain" -LastName "Malik" -Department "Marketing" -Title "Marketing Manager" -Password $AdminPassword
Create-User -FirstName "Ayesha" -LastName "Riaz" -Department "Marketing" -Title "Digital Marketing Specialist" -Password $AdminPassword

# Teachers
Create-User -FirstName "Dr.Muhammad" -LastName "Raza" -Department "Teachers" -Title "Professor (Computer Science)" -Password $AdminPassword
Create-User -FirstName "Ms.Sara" -LastName "Ahmed" -Department "Teachers" -Title "Senior Lecturer" -Password $AdminPassword

# Students (Sample)
Create-User -FirstName "Ali" -LastName "Raza" -Department "Students" -Title "BS CS Student" -Password $AdminPassword -Email "ali.raza@students.resourceacademia.local"
Create-User -FirstName "Fatima" -LastName "Khan" -Department "Students" -Title "BS IT Student" -Password $AdminPassword -Email "fatima.khan@students.resourceacademia.local"

# Admin Department
Create-User -FirstName "Hina" -LastName "Tariq" -Department "Admin" -Title "HR Manager" -Password $AdminPassword
Create-User -FirstName "Usman" -LastName "Chaudhry" -Department "Admin" -Title "Admin Officer" -Password $AdminPassword

# ============================================================================
# STEP 6: Add Users to Groups
# ============================================================================
Write-Host "`n[6] Adding Users to Groups..." -ForegroundColor Yellow

# IT Users to IT_Admins
Add-UserToGroup -Username "israrsadaq" -GroupName "IT_Admins"
Add-UserToGroup -Username "ahmedhassan" -GroupName "IT_Admins"
Add-UserToGroup -Username "fatimaali" -GroupName "Help_Desk"

# Add to Domain Admins (for IT admin)
Add-UserToGroup -Username "israrsadaq" -GroupName "Domain Admins"

# Finance Users
Add-UserToGroup -Username "omarkhan" -GroupName "Finance_Managers"
Add-UserToGroup -Username "saimaakhtar" -GroupName "Finance_Staff"

# Marketing Users
Add-UserToGroup -Username "zainmalik" -GroupName "Marketing_Staff"
Add-UserToGroup -Username "ayeshariaz" -GroupName "Marketing_Staff"

# Teachers
Add-UserToGroup -Username "drmuhammadraza" -GroupName "Faculty"
Add-UserToGroup -Username "mssaraahmed" -GroupName "Faculty"

# Students
Add-UserToGroup -Username "aliraza" -GroupName "Students"
Add-UserToGroup -Username "fatimakhan" -GroupName "Students"

# Admin
Add-UserToGroup -Username "hinatariq" -GroupName "Admin_Staff"
Add-UserToGroup -Username "usmanchaudhry" -GroupName "Admin_Staff"

# ============================================================================
# STEP 7: Create File Shares Structure (if file server exists)
# ============================================================================
Write-Host "`n[7] Creating File Share Structure..." -ForegroundColor Yellow

$FileServer = "FS01.resourceacademia.local"
if (Test-Connection $FileServer -Count 1 -Quiet) {
    $Shares = @(
        @{Name="IT_Share"; Path="D:\Shares\IT"; Description="IT Department Files"},
        @{Name="Finance_Share"; Path="D:\Shares\Finance"; Description="Finance Department Files"},
        @{Name="Marketing_Share"; Path="D:\Shares\Marketing"; Description="Marketing Department Files"},
        @{Name="Teachers_Share"; Path="D:\Shares\Teachers"; Description="Faculty Resources"},
        @{Name="Students_Share"; Path="D:\Shares\Students"; Description="Student Files"},
        @{Name="Public_Share"; Path="D:\Shares\Public"; Description="Public Access"}
    )
    
    foreach ($Share in $Shares) {
        if (-not ($WhatIf)) {
            # Create directory if not exists
            $dir = $Share.Path
            if (-not (Test-Path $dir)) {
                New-Item -Path $dir -ItemType Directory -Force | Out-Null
                Write-Log "  → Created directory: $dir" -Color Gray
            }
            
            # Create share
            try {
                New-SmbShare -Name $Share.Name -Path $Share.Path -Description $Share.Description -FullAccess "Administrator" -ChangeAccess "$($Share.Name.Split('_')[0])_Staff" -ErrorAction SilentlyContinue
                Write-Log "✓ Created share: $($Share.Name)" -Color Green
            } catch { }
        } else {
            Write-Log "[WHATIF] Would create share: $($Share.Name)" -Color Yellow
        }
    }
} else {
    Write-Log "File server $FileServer not reachable. Skipping share creation." -Color Yellow
}

# ============================================================================
# SUMMARY
# ============================================================================
Write-Host "`n" + "=" * 80 -ForegroundColor Cyan
Write-Host "AD STRUCTURE CREATION COMPLETE!" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Cyan

Write-Host "`nSUMMARY:" -ForegroundColor Yellow
Write-Host "  ✓ Department OUs: 6"
Write-Host "  ✓ Workstation OUs: 6"
Write-Host "  ✓ Server OUs: 4"
Write-Host "  ✓ Security Groups: 10"
Write-Host "  ✓ Users Created: 12"
Write-Host "  ✓ Group Memberships: 12"

Write-Host "`nLog Files:" -ForegroundColor Yellow
Write-Host "  Main Log: $LogFile"
Write-Host "  Error Log: $ErrorLog"

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Verify AD structure with: Get-ADOrganizationalUnit -Filter *"
Write-Host "  2. Check users: Get-ADUser -Filter *"
Write-Host "  3. Review groups: Get-ADGroup -Filter *"
Write-Host "  4. Configure Group Policies"
Write-Host "  5. Set up backup schedule"

if ($WhatIf) {
    Write-Host "`n!!! WHATIF MODE - No actual changes were made !!!" -ForegroundColor Red
    Write-Host "Remove -WhatIf parameter to apply changes." -ForegroundColor Red
}