 #!/usr/bin/env python3
"""
Resource Academia - Enhanced Active Directory Simulator
Network/IT Administrator: Israr Sadaq
"""

import json
import os
from datetime import datetime, timedelta

class ResourceAcademiaAD:
    def __init__(self):
        self.domain = "resourceacademia.local"
        self.data = self.create_structure()
        self.logged_in_user = None
    
    def create_structure(self):
        """Create AD structure"""
        return {
            "domain": self.domain,
            "created": datetime.now().isoformat(),
            "departments": {
                "IT": {"users": [
                    "Israr Sadaq (Network Administrator)",
                    "Ahmed Hassan (System Administrator)", 
                    "Fatima Ali (Help Desk Lead)",
                    "Usman Malik (Network Engineer)",
                    "Sara Khan (System Engineer)"
                ]},
                "Finance": {"users": [
                    "Omar Khan (Finance Manager)",
                    "Saima Akhtar (Senior Accountant)",
                    "Ali Raza (Accountant)",
                    "Nadia Shah (Payroll Specialist)"
                ]},
                "Marketing": {"users": [
                    "Zain Malik (Marketing Manager)",
                    "Ayesha Riaz (Digital Marketing Specialist)",
                    "Hamza Ali (Content Creator)",
                    "Sana Khan (Social Media Manager)"
                ]},
                "Teachers": {"users": [
                    "Dr. Muhammad Raza (Professor CS)",
                    "Ms. Sara Ahmed (Senior Lecturer IT)",
                    "Dr. Ali Hassan (Professor Mathematics)",
                    "Mr. Khalid Malik (Lecturer Networking)",
                    "Ms. Fatima Zahra (Lecturer Programming)"
                ]},
                "Students": {"users": [
                    "Ali Raza (BS CS Student)",
                    "Fatima Khan (BS IT Student)",
                    "Omar Malik (BS CS Student)",
                    "Sara Ahmed (BS IT Student)",
                    "Hamza Ali (BS SE Student)",
                    "Ayesha Riaz (BS CS Student)",
                    "Bilal Hassan (BS IT Student)",
                    "Zara Khan (BS CS Student)",
                    "Usman Shah (BS SE Student)",
                    "Hina Malik (BS IT Student)"
                ]},
                "Admin": {"users": [
                    "Hina Tariq (HR Manager)",
                    "Usman Chaudhry (Admin Officer)",
                    "Rabia Khan (Receptionist)",
                    "Imran Ali (Facility Manager)"
                ]}
            },
            "groups": {
                "IT_Admins": ["israr.sadaq", "ahmed.hassan"],
                "Network_Admins": ["usman.malik"],
                "Help_Desk": ["fatima.ali"],
                "Finance_Managers": ["omar.khan"],
                "Finance_Staff": ["omar.khan", "saima.akhtar", "ali.raza", "nadia.shah"],
                "Marketing_Staff": ["zain.malik", "ayesha.riaz", "hamza.ali", "sana.khan"],
                "Faculty": ["dr.muhammad.raza", "ms.sara.ahmed", "dr.ali.hassan", "mr.khalid.malik", "ms.fatima.zahra"],
                "Students": ["ali.raza", "fatima.khan", "omar.malik", "sara.ahmed", "hamza.ali", "ayesha.riaz", "bilal.hassan", "zara.khan", "usman.shah", "hina.malik"],
                "Admin_Staff": ["hina.tariq", "usman.chaudhry", "rabia.khan", "imran.ali"]
            },
            "user_details": {
                "israr.sadaq": {"password": "Network@2026", "last_login": None, "locked": False},
                "ahmed.hassan": {"password": "System@2026", "last_login": None, "locked": False},
                "fatima.ali": {"password": "Help@2026", "last_login": None, "locked": False}
            }
        }
    
    def print_summary(self):
        """Print AD structure summary"""
        print("\n" + "="*70)
        print(f"RESOURCE ACADEMIA - ACTIVE DIRECTORY SUMMARY")
        print("="*70)
        print(f"Domain: {self.domain}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n" + "-"*50)
        print("📁 DEPARTMENTS")
        print("-"*50)
        total_users = 0
        for dept, info in self.data["departments"].items():
            count = len(info["users"])
            total_users += count
            print(f"\n  📂 {dept.upper()} Department ({count} users)")
            for i, user in enumerate(info["users"]):
                prefix = "    ├── " if i < len(info["users"])-1 else "    └── "
                print(f"{prefix}{user}")
        
        print("\n" + "-"*50)
        print("🔐 SECURITY GROUPS")
        print("-"*50)
        for group, members in self.data["groups"].items():
            print(f"\n  👥 {group} ({len(members)} members)")
            for i, member in enumerate(members):
                prefix = "    ├── " if i < len(members)-1 else "    └── "
                print(f"{prefix}{member}")
        
        print("\n" + "="*70)
        print(f"📊 STATISTICS")
        print("="*70)
        print(f"  Total Users:     {total_users}")
        print(f"  Total Groups:    {len(self.data['groups'])}")
        print(f"  Total Depts:     {len(self.data['departments'])}")
        print(f"  Domain:          {self.domain}")
        print("="*70)
    
    def list_users_by_department(self, department):
        """List users in specific department"""
        if department in self.data["departments"]:
            count = len(self.data["departments"][department]["users"])
            print(f"\n📂 {department.upper()} Department ({count} users)")
            print("-"*40)
            for user in self.data["departments"][department]["users"]:
                print(f"  👤 {user}")
        else:
            print(f"\n❌ Department '{department}' not found")
            print("Available departments: IT, Finance, Marketing, Teachers, Students, Admin")
    
    def show_group_members(self, group):
        """Show members of a group"""
        if group in self.data["groups"]:
            count = len(self.data["groups"][group])
            print(f"\n👥 Group: {group}")
            print(f"📊 Members: {count}")
            print("-"*40)
            for member in self.data["groups"][group]:
                print(f"  👤 {member}")
        else:
            print(f"\n❌ Group '{group}' not found")
            print("Available groups:")
            for g in self.data["groups"].keys():
                print(f"  - {g}")
    
    def search_user(self, search_term):
        """Search for users across all departments"""
        results = []
        for dept, info in self.data["departments"].items():
            for user in info["users"]:
                if search_term.lower() in user.lower():
                    results.append((dept, user))
        
        if results:
            print(f"\n🔍 Search Results for '{search_term}': {len(results)} found")
            print("-"*50)
            for dept, user in results:
                print(f"  📂 {dept:10} | 👤 {user}")
        else:
            print(f"\n🔍 No users found matching '{search_term}'")
    
    def get_statistics(self):
        """Get detailed statistics"""
        total_users = sum(len(info["users"]) for info in self.data["departments"].values())
        total_groups = len(self.data["groups"])
        
        # Count users by department
        dept_stats = {}
        for dept, info in self.data["departments"].items():
            dept_stats[dept] = len(info["users"])
        
        # Count group memberships
        group_sizes = {}
        for group, members in self.data["groups"].items():
            group_sizes[group] = len(members)
        
        print("\n" + "="*70)
        print("📊 ACTIVE DIRECTORY STATISTICS")
        print("="*70)
        print(f"\n📈 Overall:")
        print(f"  Total Users:  {total_users}")
        print(f"  Total Groups: {total_groups}")
        print(f"  Total Depts:  {len(self.data['departments'])}")
        
        print(f"\n📂 By Department:")
        for dept, count in sorted(dept_stats.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * (count // 2)
            print(f"  {dept:10} : {count:2} users {bar}")
        
        print(f"\n👥 Largest Groups:")
        for group, size in sorted(group_sizes.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {group:15} : {size:2} members")
    
    def simulate_login(self):
        """Simulate user login"""
        print("\n" + "="*50)
        print("🔐 SIMULATED LOGIN")
        print("="*50)
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        if username in self.data["user_details"]:
            user = self.data["user_details"][username]
            if user["locked"]:
                print("❌ Account is locked. Contact IT administrator.")
                return False
            if password == user["password"]:
                user["last_login"] = datetime.now().isoformat()
                self.logged_in_user = username
                print(f"✅ Welcome {username}! Last login: {user['last_login']}")
                return True
            else:
                print("❌ Invalid password")
                return False
        else:
            print("❌ User not found")
            return False


def main():
    ad = ResourceAcademiaAD()
    
    while True:
        print("\n" + "="*70)
        print("🏢 RESOURCE ACADEMIA - ACTIVE DIRECTORY MANAGEMENT SYSTEM")
        print(f"👨‍💼 Network/IT Administrator: Israr Sadaq")
        print("="*70)
        print("\n📋 MAIN MENU")
        print("-"*50)
        print("1.  Show AD Summary (Complete Structure)")
        print("2.  List Users by Department")
        print("3.  Show Group Members")
        print("4.  Search Users")
        print("5.  View Statistics")
        print("6.  Simulate Login")
        print("7.  Export AD Data (JSON)")
        print("8.  Exit")
        
        choice = input("\n👉 Enter choice (1-8): ").strip()
        
        if choice == "1":
            ad.print_summary()
        elif choice == "2":
            print("\n📂 Available Departments: IT, Finance, Marketing, Teachers, Students, Admin")
            dept = input("Enter department name: ").strip()
            ad.list_users_by_department(dept)
        elif choice == "3":
            print("\n👥 Available Groups:")
            for g in ad.data["groups"].keys():
                print(f"  - {g}")
            group = input("\nEnter group name: ").strip()
            ad.show_group_members(group)
        elif choice == "4":
            search = input("Enter name or keyword to search: ").strip()
            ad.search_user(search)
        elif choice == "5":
            ad.get_statistics()
        elif choice == "6":
            ad.simulate_login()
        elif choice == "7":
            with open("ad_export.json", "w") as f:
                json.dump(ad.data, f, indent=2)
            print("✅ AD data exported to ad_export.json")
        elif choice == "8":
            print("\n👋 Goodbye! Keep learning Active Directory!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-8")

if __name__ == "__main__":
    main()
