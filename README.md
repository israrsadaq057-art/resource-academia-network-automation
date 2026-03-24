 # Resource Academia Network Automation & IT Infrastructure

## Project Purpose

This project demonstrates my **Network Engineering** and **IT Administration** skills through a complete enterprise solution for Resource Academia International - a 300+ user educational institution.

> **Note:** This is a skill demonstration project showcasing real-world implementation of network automation and IT infrastructure management.

---

## Skills Demonstrated

| Category | Skills Shown |
|----------|--------------|
| **Network Engineering** | VLAN design, IP subnetting, OSPF routing, ACLs, Cisco IOS configuration |
| **Network Automation** | Python, Netmiko, Jinja2 templating, YAML inventory, Zero-Touch Provisioning |
| **IT Administration** | Active Directory structure, PowerShell automation, Group Policy design |
| **Security** | Cisco Firepower ACLs, network segmentation, access control policies |
| **DevOps** | Git/GitHub, Infrastructure as Code, automated documentation |

---

## What I Built

### 1. Enterprise Network Design

Designed a complete network for **300+ users** across 6 departments with proper VLAN segmentation:

| VLAN | Department | Subnet | Security Zone |
|------|------------|--------|---------------|
| 10 | IT & Finance | 10.10.10.0/24 | Internal |
| 20 | Marketing | 10.10.20.0/24 | Internal |
| 30 | Teachers | 10.10.30.0/24 | Internal |
| 40 | Students | 10.10.40.0/24 | Restricted |
| 50 | Servers | 10.10.50.0/24 | DMZ |
| 60 | Management | 10.10.60.0/24 | Management |
| 99 | Guest WiFi | 172.16.99.0/24 | Isolated |

**Network Devices:** Cisco Firepower 2130, Catalyst 9500 Core, 6 x Catalyst 9300/9200 Distribution Switches

---

### 2. Zero-Touch Provisioning (ZTP) System

Python automation that generates device configurations automatically:

```python
# Automated config generation from YAML inventory
python scripts/ztp_automation.py
