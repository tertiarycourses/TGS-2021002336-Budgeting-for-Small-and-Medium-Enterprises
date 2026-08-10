"""
SINGLE SOURCE OF TRUTH for the AZ-104 courseware.

Every artifact — the slide deck (PPT), Lesson Plan (LP), Learner Guide (LG)
and the labs/ folder — is generated from (or aligned to) the data in this
module, so titles, topic numbering, activities, learning outcomes and the
schedule can never drift apart.

Edit here, then re-run build_slides.py / build_lesson_plan.py /
build_learner_guide.py.
"""

# ------------------------------------------------------------------ metadata
TITLE       = "Microsoft Certified: Azure Administrator Associate (AZ-104)"
SHORT_TITLE = "Microsoft Azure Administrator (AZ-104)"
COURSE_CODE = "TGS-2023039182"
VERSION     = "v1.0"
VERSION_DATE = "1 July 2026"
ORG         = "Tertiary Infotech Academy Pte Ltd"
UEN         = "UEN: 201200696W"
TRAINER     = "Dr. Alfred Ang"
DAYS        = 3

# ------------------------------------------------------------------ outcomes
LEARNING_OUTCOMES = [
    "LO1: Manage Azure identities and governance — Microsoft Entra users and groups, RBAC, Azure Policy, subscriptions, resource groups, locks, tags and cost.",
    "LO2: Implement and manage Azure storage — storage accounts, redundancy, access control, Blob, Azure Files and data movement.",
    "LO3: Deploy and manage Azure compute resources — ARM/Bicep, virtual machines, scale sets, containers and App Service.",
    "LO4: Implement and manage virtual networking — virtual networks, NSGs, Bastion, endpoints, DNS and load balancing.",
    "LO5: Monitor and maintain Azure resources — Azure Monitor, Network Watcher, Azure Backup and Azure Site Recovery.",
]

# ------------------------------------------------------------------ topics (= exam skill areas)
# num, code, title, subtitle, weighting, concept bullets for the section
TOPICS = [
    dict(num=1, code="01",
         title="Manage Azure Identities and Governance",
         subtitle="Microsoft Entra ID · RBAC · Azure Policy · Subscriptions · Cost",
         weighting="20–25%",
         concepts=[
            "Microsoft Entra ID authenticates identities (users, groups, guests); Azure RBAC authorises what they may do.",
            "An RBAC role assignment = security principal + role definition + scope (management group / subscription / RG / resource).",
            "Governance is applied at a scope and inherited downward: Azure Policy, resource locks, tags, budgets.",
            "The resource hierarchy: management group → subscription → resource group → resource.",
         ]),
    dict(num=2, code="02",
         title="Implement and Manage Storage",
         subtitle="Storage accounts · Redundancy · Access · Blob · Files · AzCopy",
         weighting="15–20%",
         concepts=[
            "A storage account is a globally-unique namespace holding Blobs, Files, Queues and Tables.",
            "Redundancy (LRS / ZRS / GRS / RA-GRS) trades cost against durability and regional failover.",
            "Access is controlled by keys, SAS tokens, Entra RBAC and storage firewalls / VNet rules.",
            "Blob access tiers (hot / cool / cold / archive), versioning, soft delete and lifecycle rules manage cost.",
         ]),
    dict(num=3, code="03",
         title="Deploy and Manage Azure Compute Resources",
         subtitle="ARM & Bicep · VMs · Scale Sets · Containers · App Service",
         weighting="20–25%",
         concepts=[
            "Infrastructure as code with ARM templates and Bicep makes deployments repeatable and reviewable.",
            "Choose the least-effort compute: VM → VM Scale Set → containers (ACI / Container Apps) → App Service.",
            "Availability zones and sets, managed disks and VM sizes determine resilience and performance.",
            "App Service and Container Apps are fully-managed PaaS for web apps, APIs and microservices.",
         ]),
    dict(num=4, code="04",
         title="Implement and Manage Virtual Networking",
         subtitle="VNets · NSGs & ASGs · Bastion · Endpoints · DNS · Load Balancing",
         weighting="15–20%",
         concepts=[
            "A virtual network (VNet) is your private network in Azure, divided into subnets; peering joins VNets.",
            "NSGs and ASGs filter traffic; effective security rules show what actually applies to a NIC.",
            "Azure Bastion gives browser RDP/SSH with no public IP; service/private endpoints lock PaaS to the VNet.",
            "Azure DNS resolves names; load balancers distribute traffic across a backend pool with health probes.",
         ]),
    dict(num=5, code="05",
         title="Monitor and Maintain Azure Resources",
         subtitle="Azure Monitor · Network Watcher · Backup · Site Recovery",
         weighting="10–15%",
         concepts=[
            "Azure Monitor collects metrics and logs (Log Analytics + KQL) and raises alerts via action groups.",
            "Network Watcher diagnoses connectivity (IP flow verify, next hop, connection monitor).",
            "Azure Backup protects data with point-in-time restore from a Recovery Services vault.",
            "Azure Site Recovery replicates workloads to a second region for disaster-recovery failover.",
         ]),
]

# ------------------------------------------------------------------ 3-day schedule (8 training hours/day)
# Each day: list of (start, end, minutes, kind, text). kind: 'admin','topic','activity','break','lunch','assess','recap'
# Day totals must be 480 training minutes (lunch excluded from the 8h).
DAY_THEMES = {
    1: "Identities, Governance & Storage",
    2: "Compute & Virtual Networking",
    3: "Networking, Monitoring, Maintenance & Assessment",
}

# ------------------------------------------------------------------ assessment
ASSESSMENT = dict(
    written="Written Assessment (WA) — Short-Answer Questions (SAQ), 1 hour, open book.",
    practical="Practical Performance (PP) — hands-on Azure tasks, 1 hour, open book.",
    note="A minimum of 75% attendance is required to be eligible for assessment and funding.",
)
