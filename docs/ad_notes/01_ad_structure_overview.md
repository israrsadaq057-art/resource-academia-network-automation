\# Resource Academia - Active Directory Structure

\## Network/IT Administrator: Israr Sadaq

\## Created: March 2021



\---



\## 1. DOMAIN INFORMATION



| Attribute | Value |

|-----------|-------|

| Domain Name | resourceacademia.local |

| NetBIOS Name | RESOURCE |

| Functional Level | Windows Server 2022 |

| Domain Controllers | DC01.resourceacademia.local (Primary) |

| | DC02.resourceacademia.local (Backup) |

| Site | Islamabad (Default-First-Site) |



\---



\## 2. ORGANIZATIONAL UNIT (OU) STRUCTURE



\### 2.1 Root Level OUs

DC=resourceacademia,DC=local

│

├── OU=Departments

│ ├── OU=IT

│ ├── OU=Finance

│ ├── OU=Marketing

│ ├── OU=Teachers

│ ├── OU=Students

│ └── OU=Admin

│

├── OU=Servers

│ ├── OU=Domain Controllers

│ ├── OU=File Servers

│ ├── OU=Application Servers

│ └── OU=Backup Servers

│

├── OU=Workstations

│ ├── OU=IT\_Workstations

│ ├── OU=Finance\_Workstations

│ ├── OU=Marketing\_Workstations

│ ├── OU=Teachers\_Workstations

│ ├── OU=Student\_Labs

│ └── OU=Admin\_Workstations

│

├── OU=Groups

│ ├── OU=Security\_Groups

│ ├── OU=Distribution\_Groups

│ └── OU=Service\_Accounts

│

└── OU=Service\_Accounts

├── OU=Backup\_Accounts

├── OU=Monitoring\_Accounts

└── OU=Application\_Accounts



\### 2.2 Department OU Details



\#### IT Department (OU=IT)

OU=IT

│

├── Users

│ ├── Network\_Engineers

│ ├── System\_Admins

│ └── Help\_Desk

│

├── Groups

│ ├── IT\_Admins (Full admin rights)

│ ├── Network\_Admins (Network device access)

│ ├── Help\_Desk (User support only)

│ └── IT\_Interns (Limited access)

│

└── Computers

├── IT\_Workstations (Engineering PCs)

├── Network\_Management\_Stations (Console access)

└── Monitoring\_Stations (NMS access)

\#### Finance Department (OU=Finance)

OU=Finance

│

├── Users

│ ├── Accountants

│ ├── Payroll\_Staff

│ └── Auditors

│

├── Groups

│ ├── Finance\_Managers (Full finance access)

│ ├── Finance\_Staff (Standard access)

│ └── Finance\_ReadOnly (Audit access)

│

└── Computers

├── Finance\_Workstations

└── Accounting\_Terminals

\#### Marketing Department (OU=Marketing)

OU=Marketing

│

├── Users

│ ├── Digital\_Marketers

│ ├── Content\_Creators

│ └── Social\_Media\_Managers

│

├── Groups

│ ├── Marketing\_Managers

│ ├── Marketing\_Staff

│ └── Creative\_Team

│

└── Computers

├── Marketing\_Workstations

└── Design\_Workstations

\#### Teachers Department (OU=Teachers)

OU=Teachers

│

├── Users

│ ├── Senior\_Teachers

│ ├── Junior\_Teachers

│ └── Visiting\_Faculty

│

├── Groups

│ ├── Faculty (All teachers)

│ ├── Department\_Heads

│ └── Advisors

│

└── Computers

├── Faculty\_Laptops

└── Classroom\_PCs

\#### Students Department (OU=Students)

OU=Students

│

├── Users

│ ├── Undergraduate (Year 1,2,3,4)

│ ├── Graduate (Masters, PhD)

│ └── Research\_Students

│

├── Groups

│ ├── All\_Students

│ ├── Lab\_Access (Computer lab access)

│ ├── Library\_Access

│ └── WiFi\_Access

│

└── Computers

├── Student\_Lab\_1 (Room 101)

├── Student\_Lab\_2 (Room 102)

└── Research\_Lab

\#### Admin Department (OU=Admin)

OU=Admin

│

├── Users

│ ├── HR\_Staff

│ ├── Admin\_Officers

│ └── Reception\_Staff

│

├── Groups

│ ├── HR\_Managers

│ ├── Admin\_Staff

│ └── Reception

│

└── Computers

├── Admin\_Workstations

└── Reception\_PCs



\---



\## 3. USER ACCOUNT NAMING CONVENTIONS



\### 3.1 Format

| User Type | Format | Example |

|-----------|--------|---------|

| Staff | firstname.lastname | israr.sadaq |

| Teachers | title.firstname.lastname | mr.ahmed.khan |

| Students | studentid.firstname.lastname | 2024001.ali.raza |

| IT Admin | admin.firstname.lastname | admin.israr |

| Service Accounts | svc\_servicename | svc\_backup |



\### 3.2 Sample Users



\#### IT Department

| Username | Full Name | Title | Email |

|----------|-----------|-------|-------|

| israr.sadaq | Israr Sadaq | Network Administrator | israr.sadaq@resourceacademia.local |

| ahmed.hassan | Ahmed Hassan | System Administrator | ahmed.hassan@resourceacademia.local |

| fatima.ali | Fatima Ali | Help Desk Lead | fatima.ali@resourceacademia.local |



\#### Finance Department

| Username | Full Name | Title | Email |

|----------|-----------|-------|-------|

| omar.khan | Omar Khan | Finance Manager | omar.khan@resourceacademia.local |

| saima.akhtar | Saima Akhtar | Senior Accountant | saima.akhtar@resourceacademia.local |



\#### Teachers

| Username | Full Name | Title | Email |

|----------|-----------|-------|-------|

| dr.muhammad.raza | Dr. Muhammad Raza | Professor | dr.muhammad.raza@resourceacademia.local |

| ms.sara.ahmed | Ms. Sara Ahmed | Senior Lecturer | ms.sara.ahmed@resourceacademia.local |



\#### Students

| Username | Full Name | Program | Email |

|----------|-----------|---------|-------|

| 2024001.ali.raza | Ali Raza | BS CS | ali.raza@students.resourceacademia.local |

| 2024002.fatima.khan | Fatima Khan | BS IT | fatima.khan@students.resourceacademia.local |



\---



\## 4. SECURITY GROUPS



\### 4.1 Department Groups

| Group Name | Scope | Members | Permissions |

|------------|-------|---------|-------------|

| IT\_Admins | Global | IT Staff | Full domain admin |

| Network\_Admins | Global | Network Engineers | Network device access |

| Finance\_Managers | Global | Finance Managers | Finance share full access |

| Faculty | Global | All Teachers | Teacher resources |

| Students | Global | All Students | Lab and library access |

| Admin\_Staff | Global | Admin Staff | Admin resources |



\### 4.2 Special Purpose Groups

| Group Name | Scope | Purpose |

|------------|-------|---------|

| Domain\_Admins | Universal | Full domain control (IT only) |

| Enterprise\_Admins | Universal | Forest-wide admin (IT only) |

| Remote\_Desktop\_Users | Domain Local | RDP access to servers |

| VPN\_Users | Domain Local | VPN access |

| WiFi\_Users | Domain Local | WiFi authentication |



\---



\## 5. GROUP POLICY OBJECTS (GPOs)



\### 5.1 GPO Structure

| GPO Name | Linked OU | Purpose |

|----------|-----------|---------|

| Default Domain Policy | Domain | Password policy, account lockout |

| IT\_Security\_Policy | IT | Security settings for IT |

| Finance\_Security\_Policy | Finance | Restricted finance access |

| Student\_Restrictions | Students | Lab restrictions, internet filtering |

| Faculty\_Resources | Teachers | Network drives, software |

| Workstation\_Security | Workstations | Firewall, updates, antivirus |



\### 5.2 Password Policy

| Setting | Value |

|---------|-------|

| Minimum Password Length | 12 characters |

| Complexity | Enabled (Upper, Lower, Number, Symbol) |

| Password History | 24 remembered |

| Maximum Password Age | 90 days |

| Minimum Password Age | 1 day |

| Account Lockout Threshold | 5 attempts |

| Lockout Duration | 30 minutes |



\---



\## 6. FILE SERVER STRUCTURE



\### 6.1 Department Shares

D:\\Shares

│

├── IT

│ ├── Projects

│ ├── Documentation

│ └── Tools

│

├── Finance

│ ├── Payroll\\ (Restricted)

│ ├── Budgets

│ └── Reports

│

├── Marketing

│ ├── Campaigns

│ ├── Assets

│ └── Analytics

│

├── Teachers

│ ├── Course\_Materials

│ ├── Grades\\ (Restricted)

│ └── Research

│

├── Students

│ ├── Assignments

│ ├── Projects

│ └── Resources

│

└── Shared

├── Public

└── Training\\



\---



\## 7. AUTOMATION SCRIPTS INDEX



| Script | Purpose | Location |

|--------|---------|----------|

| 01\_create\_ous.ps1 | Create OU structure | scripts/ad\_automation/ |

| 02\_create\_users.ps1 | Create user accounts | scripts/ad\_automation/ |

| 03\_create\_groups.ps1 | Create security groups | scripts/ad\_automation/ |

| 04\_assign\_permissions.ps1 | Set folder permissions | scripts/ad\_automation/ |

| 05\_daily\_audit.ps1 | Daily AD health check | scripts/ad\_automation/ |

| 06\_inactive\_users.ps1 | Find/disable inactive users | scripts/ad\_automation/ |

| ad\_manager.py | Python AD management | scripts/ad\_automation/ |



