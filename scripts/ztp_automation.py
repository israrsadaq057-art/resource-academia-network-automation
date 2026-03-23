#!/usr/bin/env python3
"""
============================================================================
RESOURCE ACADEMIA INTERNATIONAL - ZERO-TOUCH PROVISIONING SYSTEM
============================================================================
Network Engineer: Israr Sadaq
Company: Resource Academia International, Islamabad
Project: Automated Network Device Configuration

This script automates the deployment of network configurations for:
- Core Switch (Cisco Catalyst 9500)
- Distribution Switches (Cisco Catalyst 9300/9200)
- Firewall policies (Cisco Firepower)
- DHCP and DNS configurations
============================================================================
"""

import os
import sys
import yaml
import json
import logging
import ipaddress
from datetime import datetime
from pathlib import Path

# Set up project paths
PROJECT_ROOT = Path(__file__).parent.parent
INVENTORY_DIR = PROJECT_ROOT / "inventory"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
CONFIGS_DIR = PROJECT_ROOT / "configs"
LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Create directories if they don't exist
for dir_path in [CONFIGS_DIR, LOGS_DIR, REPORTS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / f"ztp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class ResourceAcademiaZTP:
    """Zero-Touch Provisioning System for Resource Academia"""
    
    def __init__(self, inventory_file):
        """Initialize ZTP system with inventory"""
        self.inventory_file = Path(inventory_file)
        self.data = None
        self.company = None
        self.vlans = None
        self.servers = None
        self.network_devices = None
        self.security_policies = None
        self.dhcp_scopes = None
        
        self.load_inventory()
        
    def load_inventory(self):
        """Load and validate inventory data"""
        try:
            with open(self.inventory_file, 'r') as f:
                self.data = yaml.safe_load(f)
            
            self.company = self.data.get('company', {})
            self.vlans = self.data.get('vlans', [])
            self.servers = self.data.get('servers', [])
            self.network_devices = self.data.get('network_devices', {})
            self.security_policies = self.data.get('security_policies', [])
            self.dhcp_scopes = self.data.get('dhcp_scopes', [])
            
            logger.info(f"✓ Loaded inventory: {self.inventory_file}")
            logger.info(f"  - Company: {self.company.get('name')}")
            logger.info(f"  - Engineer: {self.company.get('engineer')}")
            logger.info(f"  - VLANs: {len(self.vlans)}")
            logger.info(f"  - Servers: {len(self.servers)}")
            logger.info(f"  - Distribution Switches: {len(self.network_devices.get('distribution_switches', []))}")
            
            return True
            
        except FileNotFoundError:
            logger.error(f"Inventory file not found: {self.inventory_file}")
            sys.exit(1)
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error loading inventory: {e}")
            sys.exit(1)
    
    def validate_ip_scheme(self):
        """Validate all IP addresses and subnets"""
        logger.info("\n" + "="*60)
        logger.info("VALIDATING IP ADDRESS SCHEME")
        logger.info("="*60)
        
        errors = []
        
        # Validate VLAN subnets and gateways
        for vlan in self.vlans:
            try:
                subnet = ipaddress.ip_network(vlan['subnet'])
                gateway = ipaddress.ip_address(vlan['gateway'])
                
                if gateway not in subnet:
                    errors.append(f"VLAN {vlan['id']}: Gateway {gateway} not in subnet {subnet}")
                else:
                    logger.info(f"✓ VLAN {vlan['id']}: {vlan['name']} - {vlan['subnet']} (Gateway: {vlan['gateway']})")
            except ValueError as e:
                errors.append(f"VLAN {vlan['id']}: Invalid IP configuration - {e}")
        
        # Validate server IPs
        for server in self.servers:
            try:
                ip = ipaddress.ip_address(server['ip'])
                # Check if IP is in correct VLAN subnet
                for vlan in self.vlans:
                    if vlan['id'] == server['vlan']:
                        subnet = ipaddress.ip_network(vlan['subnet'])
                        if ip in subnet:
                            logger.info(f"✓ Server {server['name']}: {server['ip']} (VLAN {server['vlan']})")
                        else:
                            errors.append(f"Server {server['name']}: IP {server['ip']} not in VLAN {server['vlan']} subnet {vlan['subnet']}")
            except ValueError as e:
                errors.append(f"Server {server['name']}: Invalid IP - {e}")
        
        if errors:
            logger.error("\nValidation Errors Found:")
            for error in errors:
                logger.error(f"  ✗ {error}")
            return False
        
        logger.info("\n✓ All IP addresses validated successfully")
        return True
    
    def generate_core_switch_config(self):
        """Generate core switch configuration"""
        core = self.network_devices.get('core_switch', {})
        if not core:
            logger.warning("No core switch configuration found")
            return None
        
        logger.info(f"\nGenerating configuration for {core['name']}...")
        
        config = f"""
! ============================================================================
! RESOURCE ACADEMIA INTERNATIONAL - CORE SWITCH CONFIGURATION
! ============================================================================
! Device: {core['name']} ({core['model']})
! Management IP: {core['mgmt_ip']}
! Network Engineer: {self.company.get('engineer', 'Israr Sadaq')}
! Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
! ============================================================================

hostname {core['name']}

! Enable password
enable secret ResourceAcademia2026!

! ============================================================================
! VLAN CONFIGURATION
! ============================================================================
"""
        
        for vlan in self.vlans:
            config += f"""
vlan {vlan['id']}
 name {vlan['name']}
!"""
        
        config += """
! ============================================================================
! INTERFACE VLAN (SVI) - Gateway Configuration
! ============================================================================
"""
        
        for vlan in self.vlans:
            config += f"""
interface Vlan{vlan['id']}
 description {vlan['name']} Gateway - {vlan['subnet']}
 ip address {vlan['gateway']} 255.255.255.0
 no shutdown
!"""
        
        config += """
! ============================================================================
! UPLINK TO FIREWALL
! ============================================================================
interface GigabitEthernet1/0/1
 description Uplink to Firepower-2130
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,60,70,99
 no shutdown

! ============================================================================
! DISTRIBUTION SWITCH UPLINKS
! ============================================================================
"""
        
        # Add distribution switch uplinks
        for i, dist_switch in enumerate(self.network_devices.get('distribution_switches', []), start=1):
            config += f"""
interface GigabitEthernet1/0/{i+1}
 description Uplink to {dist_switch['name']}
 switchport mode trunk
 switchport trunk allowed vlan {','.join(map(str, dist_switch['vlans']))},60
 no shutdown
!"""
        
        config += """
! ============================================================================
! IP ROUTING AND OSPF
! ============================================================================
ip routing

router ospf 1
 router-id 10.10.60.2
 network 10.10.0.0 0.0.255.255 area 0
 default-information originate

! ============================================================================
! DHCP RELAY
! ============================================================================
"""
        
        for vlan in self.vlans:
            if vlan['id'] != 99:  # Guest VLAN uses separate DHCP
                config += f"""
interface Vlan{vlan['id']}
 ip helper-address 10.10.10.20
!"""
        
        config += """
! ============================================================================
! MANAGEMENT CONFIGURATION
! ============================================================================
interface Vlan60
 description Management Network
 ip address 10.10.60.2 255.255.255.0

ip default-gateway 10.10.60.1

! SSH Configuration
ip domain-name resourceacademia.edu.pk
crypto key generate rsa modulus 2048

username admin privilege 15 secret ResourceAcademia2026!

line vty 0 15
 transport input ssh
 login local
 exec-timeout 15 0

! SNMP Monitoring
snmp-server community ResourceAcademia_RO RO
snmp-server location Islamabad, Pakistan
snmp-server contact israrsadaq057@gmail.com

! NTP Configuration
ntp server pool.ntp.org

! Logging
logging buffered 16384
logging host 10.10.60.50

! ============================================================================
! SAVE CONFIGURATION
! ============================================================================
end
write memory
"""
        
        # Save configuration
        config_file = CONFIGS_DIR / f"{core['name']}_config.txt"
        with open(config_file, 'w') as f:
            f.write(config)
        
        logger.info(f"  ✓ Config saved: {config_file}")
        return config_file
    
    def generate_distribution_switch_config(self, switch):
        """Generate configuration for a distribution switch"""
        logger.info(f"\nGenerating configuration for {switch['name']}...")
        
        config = f"""
! ============================================================================
! RESOURCE ACADEMIA INTERNATIONAL - DISTRIBUTION SWITCH CONFIGURATION
! ============================================================================
! Device: {switch['name']} ({switch['model']})
! Management IP: {switch['mgmt_ip']}
! VLANs: {', '.join(map(str, switch['vlans']))}
! Users: {switch.get('users', 'N/A')}
! Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
! ============================================================================

hostname {switch['name']}

enable secret ResourceAcademia2026!

! ============================================================================
! UPLINK TO CORE SWITCH
! ============================================================================
interface GigabitEthernet1/0/1
 description Uplink to Core-SW-9500
 switchport mode trunk
 switchport trunk allowed vlan {','.join(map(str, switch['vlans']))},60
 no shutdown

! ============================================================================
! ACCESS PORTS FOR DEPARTMENT
! ============================================================================
"""
        
        # Add access ports for each VLAN
        for vlan in switch['vlans']:
            vlan_info = next((v for v in self.vlans if v['id'] == vlan), None)
            if vlan_info:
                config += f"""
! VLAN {vlan} - {vlan_info['name']} Access Ports
"""
                for port in range(2, 25):  # Ports 2-24 for access
                    config += f"""
interface GigabitEthernet1/0/{port}
 description Access Port for {vlan_info['name']}
 switchport mode access
 switchport access vlan {vlan}
 spanning-tree portfast
 no shutdown
!"""
        
        # Add ACL if needed
        if switch.get('acl') == 'deny_student_server_access':
            config += """
! ============================================================================
! STUDENT VLAN ACCESS CONTROL
! ============================================================================
ip access-list extended DENY_SERVER_ACCESS
 deny ip any 10.10.50.0 0.0.0.255
 deny ip any 10.10.10.0 0.0.0.255
 permit ip any any

interface Vlan40
 ip access-group DENY_SERVER_ACCESS in
!"""
        
        config += """
! ============================================================================
! MANAGEMENT CONFIGURATION
! ============================================================================
interface Vlan60
 description Management Network
 ip address 10.10.60.13 255.255.255.0

ip default-gateway 10.10.60.1

! SSH Configuration
ip domain-name resourceacademia.edu.pk
crypto key generate rsa modulus 2048

username admin privilege 15 secret ResourceAcademia2026!

line vty 0 15
 transport input ssh
 login local

! ============================================================================
! SAVE CONFIGURATION
! ============================================================================
end
write memory
"""
        
        # Save configuration
        config_file = CONFIGS_DIR / f"{switch['name']}_config.txt"
        with open(config_file, 'w') as f:
            f.write(config)
        
        logger.info(f"  ✓ Config saved: {config_file}")
        return config_file
    
    def generate_firewall_policies(self):
        """Generate Firepower ACL configuration"""
        logger.info("\nGenerating Firepower ACL policies...")
        
        config = f"""
! ============================================================================
! CISCO FIREPOWER 2130 - ACCESS CONTROL POLICIES
! Resource Academia International
! Network Engineer: {self.company.get('engineer', 'Israr Sadaq')}
! Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
! ============================================================================

! ============================================================================
! OBJECT DEFINITIONS
! ============================================================================
object-group network INTERNAL_NETWORKS
 network-object 10.10.0.0 255.255.0.0

object-group network SERVER_NETWORK
 network-object 10.10.50.0 255.255.255.0

object-group network STUDENT_NETWORK
 network-object 10.10.40.0 255.255.255.0

object-group network MANAGEMENT_NETWORK
 network-object 10.10.60.0 255.255.255.0

! ============================================================================
! ACCESS CONTROL LISTS
! ============================================================================
! Allow internet access for all internal networks
access-list INSIDE_OUT extended permit ip object-group INTERNAL_NETWORKS any

! Allow access to web servers
access-list INSIDE_OUT extended permit tcp any host 10.10.50.10 eq 80
access-list INSIDE_OUT extended permit tcp any host 10.10.50.10 eq 443

! Allow email services
access-list INSIDE_OUT extended permit tcp any host 10.10.50.20 eq 25
access-list INSIDE_OUT extended permit tcp any host 10.10.50.20 eq 587
access-list INSIDE_OUT extended permit tcp any host 10.10.50.20 eq 993

! Allow Active Directory services (IT only)
access-list INSIDE_OUT extended permit tcp 10.10.10.0 255.255.255.0 host 10.10.10.10 eq 389
access-list INSIDE_OUT extended permit udp 10.10.10.0 255.255.255.0 host 10.10.10.10 eq 53
access-list INSIDE_OUT extended permit tcp 10.10.10.0 255.255.255.0 host 10.10.10.10 eq 88

! ============================================================================
! STUDENT RESTRICTIONS - No access to servers or IT network
! ============================================================================
access-list STUDENT_IN extended deny ip object-group STUDENT_NETWORK object-group SERVER_NETWORK
access-list STUDENT_IN extended deny ip object-group STUDENT_NETWORK 10.10.10.0 255.255.255.0
access-list STUDENT_IN extended permit ip object-group STUDENT_NETWORK any

! ============================================================================
! GUEST WIFI ISOLATION - Internet only
! ============================================================================
access-list GUEST_IN extended deny ip 172.16.99.0 255.255.255.0 10.0.0.0 255.0.0.0
access-list GUEST_IN extended deny ip 172.16.99.0 255.255.255.0 172.16.0.0 255.240.0.0
access-list GUEST_IN extended deny ip 172.16.99.0 255.255.255.0 192.168.0.0 255.255.0.0
access-list GUEST_IN extended permit ip 172.16.99.0 255.255.255.0 any

! ============================================================================
! MANAGEMENT ACCESS - IT only
! ============================================================================
access-list MGMT_IN extended permit tcp 10.10.10.0 255.255.255.0 object-group MANAGEMENT_NETWORK eq 22
access-list MGMT_IN extended permit tcp 10.10.10.0 255.255.255.0 object-group MANAGEMENT_NETWORK eq 443
access-list MGMT_IN extended permit udp 10.10.10.0 255.255.255.0 object-group MANAGEMENT_NETWORK eq 161

! ============================================================================
! DEFAULT DENY
! ============================================================================
access-list INSIDE_OUT extended deny ip any any log

! Apply ACLs to interfaces
access-group INSIDE_OUT in interface inside
access-group STUDENT_IN in interface student-vlan
access-group GUEST_IN in interface guest-vlan
access-group MGMT_IN in interface management

! ============================================================================
! INTRUSION PREVENTION SYSTEM (IPS)
! ============================================================================
ips policy default-ips-policy
 ips signature-definition default
!
class-map IPS_TRAFFIC
 match any
!
policy-map IPS_POLICY
 class IPS_TRAFFIC
  ips inline fail-open
!
service-policy IPS_POLICY interface inside
"""
        
        # Save firewall policies
        config_file = CONFIGS_DIR / "firepower_acl.txt"
        with open(config_file, 'w') as f:
            f.write(config)
        
        logger.info(f"  ✓ Firewall policies saved: {config_file}")
        return config_file
    
    def generate_network_documentation(self):
        """Generate comprehensive network documentation"""
        logger.info("\nGenerating network documentation...")
        
        doc_file = REPORTS_DIR / f"network_documentation_{datetime.now().strftime('%Y%m%d')}.md"
        
        with open(doc_file, 'w') as f:
            f.write(f"# Resource Academia International - Network Documentation\n\n")
            f.write(f"**Network Engineer:** {self.company.get('engineer')}\n")
            f.write(f"**Location:** {self.company.get('location')}\n")
            f.write(f"**Date:** {datetime.now().strftime('%B %d, %Y')}\n\n")
            
            f.write("## Network Overview\n\n")
            f.write(f"**Company:** {self.company.get('name')}\n")
            f.write(f"**Total VLANs:** {len(self.vlans)}\n")
            f.write(f"**Total Servers:** {len(self.servers)}\n")
            f.write(f"**Distribution Switches:** {len(self.network_devices.get('distribution_switches', []))}\n\n")
            
            f.write("## VLAN Configuration\n\n")
            f.write("| VLAN ID | Name | Subnet | Gateway | Security Zone |\n")
            f.write("|---------|------|--------|---------|---------------|\n")
            for vlan in self.vlans:
                f.write(f"| {vlan['id']} | {vlan['name']} | {vlan['subnet']} | {vlan['gateway']} | {vlan.get('security_zone', 'internal')} |\n")
            
            f.write("\n## Server Infrastructure\n\n")
            f.write("| Server | Role | IP Address | VLAN | OS |\n")
            f.write("|--------|------|------------|------|-----|\n")
            for server in self.servers:
                f.write(f"| {server['name']} | {server['role']} | {server['ip']} | {server['vlan']} | {server['os']} |\n")
            
            f.write("\n## Security Policies\n\n")
            for policy in self.security_policies:
                f.write(f"### {policy['name']}\n")
                f.write(f"- **Action:** {policy['action'].upper()}\n")
                f.write(f"- **Description:** {policy['description']}\n")
                if 'source_vlan' in policy:
                    f.write(f"- **Source:** VLAN {policy['source_vlan']}\n")
                if 'destination_networks' in policy:
                    f.write(f"- **Destination:** {', '.join(policy['destination_networks'])}\n")
                f.write("\n")
        
        logger.info(f"  ✓ Documentation saved: {doc_file}")
        return doc_file
    
    def generate_dhcp_configuration(self):
        """Generate DHCP configuration for Windows Server"""
        logger.info("\nGenerating DHCP configuration...")
        
        dhcp_file = CONFIGS_DIR / "dhcp_configuration.txt"
        
        with open(dhcp_file, 'w') as f:
            f.write("# Windows Server DHCP Configuration\n")
            f.write("# Server: DC1 (10.10.10.10)\n")
            f.write("# Generated by Network Automation System\n\n")
            
            for scope in self.dhcp_scopes:
                vlan_info = next((v for v in self.vlans if v['id'] == scope['vlan']), None)
                f.write(f"# =========================================\n")
                f.write(f"# VLAN {scope['vlan']} - {vlan_info['name'] if vlan_info else 'Unknown'}\n")
                f.write(f"# =========================================\n")
                f.write(f"Add-DhcpServerv4Scope -Name \"VLAN{scope['vlan']}\" -StartRange {scope['range_start']} -EndRange {scope['range_end']} -SubnetMask 255.255.255.0\n")
                f.write(f"Set-DhcpServerv4Scope -ScopeId {scope['subnet']} -LeaseDuration {scope.get('lease_time', 86400)}\n")
                f.write(f"Set-DhcpServerv4OptionValue -ScopeId {scope['subnet']} -DnsServer {scope['dns_servers'][0]} -Router {vlan_info['gateway'] if vlan_info else 'N/A'}\n\n")
        
        logger.info(f"  ✓ DHCP config saved: {dhcp_file}")
        return dhcp_file
    
    def run_deployment(self):
        """Run full deployment"""
        print("\n" + "="*70)
        print("RESOURCE ACADEMIA INTERNATIONAL")
        print("ZERO-TOUCH PROVISIONING SYSTEM")
        print("="*70)
        print(f"Network Engineer: {self.company.get('engineer')}")
        print(f"Company: {self.company.get('name')}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        # Step 1: Validate IP scheme
        if not self.validate_ip_scheme():
            logger.error("IP validation failed. Aborting deployment.")
            return False
        
        # Step 2: Generate core switch config
        core_config = self.generate_core_switch_config()
        
        # Step 3: Generate distribution switch configs
        dist_configs = []
        for switch in self.network_devices.get('distribution_switches', []):
            config = self.generate_distribution_switch_config(switch)
            dist_configs.append(config)
        
        # Step 4: Generate firewall policies
        firewall_config = self.generate_firewall_policies()
        
        # Step 5: Generate DHCP configuration
        dhcp_config = self.generate_dhcp_configuration()
        
        # Step 6: Generate documentation
        documentation = self.generate_network_documentation()
        
        # Summary
        print("\n" + "="*70)
        print("DEPLOYMENT COMPLETE")
        print("="*70)
        print(f"\nGenerated Files:")
        print(f"  Core Switch Config: {core_config}")
        print(f"  Distribution Switch Configs: {len(dist_configs)} files")
        print(f"  Firewall Policies: {firewall_config}")
        print(f"  DHCP Config: {dhcp_config}")
        print(f"  Documentation: {documentation}")
        print(f"  Logs: {LOGS_DIR}")
        
        return True


def main():
    """Main execution"""
    # Initialize ZTP system
    inventory_file = INVENTORY_DIR / "resource_academia.yaml"
    
    if not inventory_file.exists():
        logger.error(f"Inventory file not found: {inventory_file}")
        sys.exit(1)
    
    ztp = ResourceAcademiaZTP(inventory_file)
    
    # Run deployment
    success = ztp.run_deployment()
    
    if success:
        print("\n✓ ZTP System ready for deployment")
        print("\nNext Steps:")
        print("  1. Review generated configurations in 'configs/'")
        print("  2. Stage configs on TFTP server for Zero-Touch Provisioning")
        print("  3. Connect new devices and power them on")
        print("  4. Verify automatic configuration via DHCP option 67")
        print("  5. Test connectivity and security policies")
    else:
        print("\n✗ Deployment failed. Check logs for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()