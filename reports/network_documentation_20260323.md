# Resource Academia International - Network Documentation

**Network Engineer:** Israr Sadaq
**Location:** Islamabad, Pakistan
**Date:** March 23, 2026

## Network Overview

**Company:** Resource Academia International
**Total VLANs:** 8
**Total Servers:** 5
**Distribution Switches:** 6

## VLAN Configuration

| VLAN ID | Name | Subnet | Gateway | Security Zone |
|---------|------|--------|---------|---------------|
| 10 | IT_Finance | 10.10.10.0/24 | 10.10.10.1 | internal |
| 20 | Marketing | 10.10.20.0/24 | 10.10.20.1 | internal |
| 30 | Teachers | 10.10.30.0/24 | 10.10.30.1 | internal |
| 40 | Students | 10.10.40.0/24 | 10.10.40.1 | restricted |
| 50 | Servers | 10.10.50.0/24 | 10.10.50.1 | dmz |
| 60 | Management | 10.10.60.0/24 | 10.10.60.1 | management |
| 70 | Admin | 10.10.70.0/24 | 10.10.70.1 | internal |
| 99 | Guest | 172.16.99.0/24 | 172.16.99.1 | guest |

## Server Infrastructure

| Server | Role | IP Address | VLAN | OS |
|--------|------|------------|------|-----|
| DC1 | Active Directory / DNS / DHCP | 10.10.10.10 | 10 | Windows Server 2022 |
| WEB1 | Web Server / LMS | 10.10.50.10 | 50 | Ubuntu 22.04 LTS |
| EMAIL1 | Email Server | 10.10.50.20 | 50 | Ubuntu 22.04 LTS |
| FILE1 | File Server | 10.10.50.30 | 50 | Windows Server 2022 |
| BACKUP1 | Backup Server | 10.10.60.10 | 60 | Ubuntu 22.04 LTS |

## Security Policies

### STUDENT_RESTRICTED
- **Action:** DENY
- **Description:** Students cannot access servers or IT network
- **Source:** VLAN 40
- **Destination:** 10.10.50.0/24, 10.10.10.0/24

### GUEST_ISOLATION
- **Action:** DENY
- **Description:** Guest WiFi isolated from internal networks
- **Source:** VLAN 99
- **Destination:** 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16

### MANAGEMENT_ACCESS
- **Action:** PERMIT
- **Description:** Only IT can access management VLAN

