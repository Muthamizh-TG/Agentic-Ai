"""
Data module containing all mock data and static information
for Technology-Garage Multi-Agent System
"""

MOCK_TICKETS = [
    {
        "ticket_id": "TKT-001",
        "raised_by": "Muthamizh (Coach)",
        "category": "IT Support",
        "subject": "Laptop not connecting to WiFi",
        "description": "Unable to connect to office WiFi network. Getting authentication error.",
        "status": "Open",
        "priority": "High",
        "created_at": "2025-12-05 10:30:00"
    },
    {
        "ticket_id": "TKT-002",
        "raised_by": "Sarah (Parent)",
        "category": "Admission Query",
        "subject": "Admission process for Grade 5",
        "description": "Need information about admission requirements and deadlines for Grade 5.",
        "status": "In Progress",
        "priority": "Medium",
        "created_at": "2025-12-04 14:20:00"
    },
    {
        "ticket_id": "TKT-003",
        "raised_by": "Praneeth (Player)",
        "category": "Training Schedule",
        "subject": "Schedule conflict with training",
        "description": "Training schedule conflicts with school exams. Request for rescheduling.",
        "status": "Open",
        "priority": "High",
        "created_at": "2025-12-05 09:15:00"
    },
    {
        "ticket_id": "TKT-004",
        "raised_by": "Prince (Coach)",
        "category": "HR Request",
        "subject": "Leave application for next week",
        "description": "Requesting leave from Dec 10-12 for personal reasons.",
        "status": "Resolved",
        "priority": "Low",
        "created_at": "2025-12-03 11:00:00"
    },
    {
        "ticket_id": "TKT-005",
        "raised_by": "Tamizh (Coach)",
        "category": "Facility Management",
        "subject": "Laptop battery not charging",
        "description": "Laptop battery is not charging properly and drains quickly.",
        "status": "Open",
        "priority": "High",
        "created_at": "2025-12-05 12:10:00"
    },
    {
        "ticket_id": "TKT-006",
        "raised_by": "Tamizh (Coach)",
        "category": "Software Access",
        "subject": "Cannot access MongoDB Atlas",
        "description": "Login showing unauthorized even after password reset.",
        "status": "In Progress",
        "priority": "Medium",
        "created_at": "2025-12-04 17:45:00"
    },
    {
        "ticket_id": "TKT-007",
        "raised_by": "Keerthana (Coach)",
        "category": "Network Issue",
        "subject": "VPN connection drops frequently",
        "description": "VPN disconnects every 10 minutes, affecting remote work.",
        "status": "Open",
        "priority": "High",
        "created_at": "2025-12-05 08:50:00"
    },
    {
        "ticket_id": "TKT-008",
        "raised_by": "Priya (Coach)",
        "category": "Account Issue",
        "subject": "Unable to reset password",
        "description": "Password reset link not working, cannot access account.",
        "status": "Resolved",
        "priority": "Medium",
        "created_at": "2025-12-03 15:30:00"
    },
    {
        "ticket_id": "TKT-009",
        "raised_by": "Anitha (Parent)",
        "category": "Billing Query",
        "subject": "Clarification on invoice charges",
        "description": "Need explanation for additional charges on last invoice.",
        "status": "In Progress",
        "priority": "Low",
        "created_at": "2025-12-04 10:05:00"
    },
    {
        "ticket_id": "TKT-010",
        "raised_by": "Karithikeyan (Player)",
        "category": "Equipment Request",
        "subject": "Request for new headphones",
        "description": "Current headphones are damaged, need replacement for training sessions.",
        "status": "Open",
        "priority": "Medium",
        "created_at": "2025-12-05 13:25:00"
    }
]


MOCK_ACTIVITIES = [
    {
        "activity_id": "ACT-001",
        "employee": "Priya",
        "task": "Implement user authentication module",
        "status": "In Progress",
        "priority": "High",
        "start_date": "2025-12-01",
        "due_date": "2025-12-08",
        "progress": "70%"
    },
    {
        "activity_id": "ACT-002",
        "employee": "Tamizh",
        "task": "Design new landing page",
        "status": "To Do",
        "priority": "Medium",
        "start_date": "2025-12-06",
        "due_date": "2025-12-15",
        "progress": "0%"
    },
    {
        "activity_id": "ACT-003",
        "employee": "Keerthana",
        "task": "Database optimization",
        "status": "Completed",
        "priority": "High",
        "start_date": "2025-11-28",
        "due_date": "2025-12-05",
        "progress": "100%"
    },
    {
        "activity_id": "ACT-004",
        "employee": "Keerthana",
        "task": "Write API documentation",
        "status": "In Progress",
        "priority": "Medium",
        "start_date": "2025-12-02",
        "due_date": "2025-12-10",
        "progress": "45%"
    },
    {
        "activity_id": "ACT-005",
        "employee": "Priya",
        "task": "Security audit review",
        "status": "To Do",
        "priority": "High",
        "start_date": "2025-12-07",
        "due_date": "2025-12-20",
        "progress": "0%"
    },
    {
        "activity_id": "ACT-006",
        "employee": "Tamizh",
        "task": "Prepare training materials",
        "status": "In Progress",
        "priority": "Low",
        "start_date": "2025-12-03",
        "due_date": "2025-12-18",
        "progress": "25%"
    },
    {
        "activity_id": "ACT-007",
        "employee": "Keerthana",
        "task": "Set up CI/CD pipeline",
        "status": "To Do",
        "priority": "High",
        "start_date": "2025-12-09",
        "due_date": "2025-12-22",
        "progress": "0%"
    },
    {
        "activity_id": "ACT-008",
        "employee": "Priya",
        "task": "Client meeting preparation",
        "status": "Completed",
        "priority": "Medium",
        "start_date": "2025-11-30",
        "due_date": "2025-12-04",
        "progress": "100%"
    },
    {
        "activity_id": "ACT-009",
        "employee": "Tamizh",
        "task": "Code review for new features",
        "status": "In Progress",
        "priority": "High",
        "start_date": "2025-12-04",
        "due_date": "2025-12-12",
        "progress": "60%"
    }
]

COMPANY_INFO = {
    "name": "Technology-Garage",
    "founded": "2023",
    "headquarters": "Dallas, Texas, USA",
    "description": "Technology-Garage is a revolutionary gamified learning and coaching platform that transforms technology education into an engaging, game-like experience. We coach aspiring tech professionals and students through interactive challenges, level-based progression, and real-world project simulations.",
    "services": [
        "Gamified Coding Bootcamps",
        "Interactive Tech Skill Challenges",
        "AI-Powered Personalized Learning Paths",
        "Level-Based Technology Certification Programs",
        "Real-World Project Simulations",
        "One-on-One Tech Coaching",
        "Team-Based Hackathon Training",
        "Achievement & Badge System for Skill Mastery",
        "Career Transition Coaching in Tech",
        "Competitive Programming Leagues"
    ],
    "team_size": "50+ coaches",
    "industries_served": ["Education Technology", "Professional Development", "Career Coaching", "Tech Training", "E-Learning"],
    "vision": "Making technology mastery accessible and fun through gamified learning experiences",
    "mission": "To coach and empower the next generation of tech professionals through engaging, game-based learning that turns skill-building into an adventure",
    "values": ["Playful Learning", "Continuous Growth", "Community Support", "Achievement Recognition", "Real-World Impact"],
    "clients": ["Academy", "University", "Institute", "League", "Training"],
    "learning_approach": {
        "gamification_elements": ["Experience Points (XP)", "Level Progression", "Skill Badges", "Leaderboards", "Daily Quests", "Challenges"],
        "coaching_style": "Personalized Coaching with AI-assisted progress tracking",
        "skill_tracks": ["Full-Stack Development", "Data Science & AI", "Cloud Architecture", "Robotics", "Embedded Systems", "VR"],
        "success_metrics": "1000+ students coached, 100% student satisfaction"
    }
}


INFRASTRUCTURE_COSTS = {
    "AWS": {
        "services": [
            {"name": "EC2 t3.medium", "category": "Compute", "price_per_hour": "$0.0416", "price_per_month": "$30.40", "specs": "2 vCPU, 4 GB RAM", "region": "us-east-1"},
            {"name": "RDS MySQL db.t3.small", "category": "Database", "price_per_hour": "$0.034", "price_per_month": "$24.82", "specs": "2 vCPU, 2 GB RAM", "region": "us-east-1"},
            {"name": "S3 Standard Storage", "category": "Storage", "price_per_gb_month": "$0.023", "price_for_100gb": "$2.30", "specs": "First 50 TB / month", "region": "us-east-1"},
            {"name": "Lambda", "category": "Serverless", "price_per_million_requests": "$0.20", "price_per_gb_second": "$0.0000166667", "specs": "First 1M requests free", "region": "us-east-1"},
            {"name": "CloudFront", "category": "CDN", "price_per_gb": "$0.085", "price_for_1tb": "$87.00", "specs": "Data Transfer Out", "region": "Global"},
            {"name": "Elasticache Redis", "category": "Cache", "price_per_month": "$18.00", "specs": "cache.t2.micro", "region": "us-east-1"},
            {"name": "Route 53", "category": "DNS", "price_per_month": "$0.50", "specs": "Hosted zone", "region": "Global"},
            {"name": "Elastic Load Balancer", "category": "Networking", "price_per_hour": "$0.0225", "price_per_gb_data_processed": "$0.008", "specs": "Classic Load Balancer", "region": "us-east-1"},
            {"name": "EBS General Purpose SSD", "category": "Storage", "price_per_gb_month": "$0.10", "price_for_100gb": "$10.00", "specs": "gp2 volume", "region": "us-east-1"}
        ],
        "total_monthly_estimate": "$200-300"
    },
    "Azure": {
        "services": [
            {"name": "Virtual Machine B2s", "category": "Compute", "price_per_hour": "$0.0416", "price_per_month": "$30.37", "specs": "2 vCPU, 4 GB RAM", "region": "East US"},
            {"name": "Azure SQL Database", "category": "Database", "price_per_month": "$54.77", "specs": "Standard S1: 20 DTUs", "region": "East US"},
            {"name": "Blob Storage", "category": "Storage", "price_per_gb_month": "$0.018", "price_for_100gb": "$1.80", "specs": "Hot tier, LRS", "region": "East US"},
            {"name": "Functions", "category": "Serverless", "price_per_million_executions": "$0.20", "specs": "First 1M free", "region": "East US"},
            {"name": "CDN Standard", "category": "CDN", "price_per_gb": "$0.081", "price_for_1tb": "$83.00", "specs": "Standard tier", "region": "Global"},
            {"name": "Redis Cache C1", "category": "Cache", "price_per_month": "$16.00", "specs": "250 MB", "region": "East US"},
            {"name": "DNS Zone", "category": "DNS", "price_per_month": "$0.50", "specs": "First 25 zones", "region": "Global"},
            {"name": "Load Balancer Basic", "category": "Networking", "price_per_hour": "$0.025", "price_per_gb_data_processed": "$0.008", "specs": "Basic Load Balancer", "region": "East US"},
            {"name": "Managed Disks Standard SSD", "category": "Storage", "price_per_gb_month": "$0.10", "price_for_100gb": "$10.00", "specs": "Standard SSD", "region": "East US"}
        ],
        "total_monthly_estimate": "$230-320"
    },
    "Google Cloud": {
        "services": [
            {"name": "Compute Engine n1-standard-1", "category": "Compute", "price_per_hour": "$0.0475", "price_per_month": "$34.67", "specs": "1 vCPU, 3.75 GB RAM", "region": "us-central1"},
            {"name": "Cloud SQL MySQL", "category": "Database", "price_per_month": "$46.55", "specs": "db-n1-standard-1", "region": "us-central1"},
            {"name": "Cloud Storage Standard", "category": "Storage", "price_per_gb_month": "$0.020", "price_for_100gb": "$2.00", "specs": "Standard storage", "region": "us-central1"},
            {"name": "Cloud Functions", "category": "Serverless", "price_per_million_invocations": "$0.40", "specs": "First 2M free", "region": "us-central1"},
            {"name": "Cloud CDN", "category": "CDN", "price_per_gb": "$0.08", "price_for_1tb": "$82.00", "specs": "Cache egress", "region": "Global"},
            {"name": "Memorystore Redis Basic", "category": "Cache", "price_per_month": "$12.50", "specs": "1 GB", "region": "us-central1"},
            {"name": "Cloud DNS", "category": "DNS", "price_per_month": "$0.50", "specs": "Hosted zone", "region": "Global"},
            {"name": "Load Balancing", "category": "Networking", "price_per_hour": "$0.025", "price_per_gb_data_processed": "$0.008", "specs": "Global Load Balancer", "region": "us-central1"},
            {"name": "Persistent Disk Standard", "category": "Storage", "price_per_gb_month": "$0.04", "price_for_100gb": "$4.00", "specs": "Standard PD", "region": "us-central1"}
        ],
        "total_monthly_estimate": "$210-300"
    },
    "Firebase": {
        "services": [
            {"name": "Firestore", "category": "Database", "price_per_read": "$0.06 per 100K", "price_per_write": "$0.18 per 100K", "price_per_gb_storage": "$0.18/GB", "specs": "NoSQL database"},
            {"name": "Firebase Hosting", "category": "Hosting", "price_per_gb": "$0.15", "price_for_10gb": "$1.50", "specs": "10 GB free per month", "region": "Global"},
            {"name": "Cloud Functions", "category": "Serverless", "price_per_million_invocations": "$0.40", "specs": "First 2M free", "region": "us-central1"},
            {"name": "Firebase Storage", "category": "Storage", "price_per_gb_month": "$0.026", "price_for_100gb": "$2.60", "specs": "5 GB free", "region": "us-central1"},
            {"name": "Firebase Authentication", "category": "Authentication", "price": "Free", "specs": "Unlimited users", "region": "Global"},
            {"name": "Firebase Realtime Database", "category": "Database", "price_per_gb_month": "$5.00", "specs": "1 GB free", "region": "us-central1"},
            {"name": "Firebase Cloud Messaging", "category": "Messaging", "price": "Free", "specs": "Unlimited messages", "region": "Global"},
            {"name": "Firebase Remote Config", "category": "Configuration", "price": "Free", "specs": "Unlimited parameters", "region": "Global"}        
            ],
        "total_monthly_estimate": "$25-150 (based on usage)"
    },
    "DigitalOcean": {
        "services": [
            {"name": "Droplet Basic", "category": "Compute", "price_per_month": "$18.00", "specs": "2 GB RAM, 1 vCPU, 50 GB SSD", "region": "NYC1"},
            {"name": "Managed Database MySQL", "category": "Database", "price_per_month": "$15.00", "specs": "1 GB RAM, 1 vCPU, 10 GB disk", "region": "NYC1"},
            {"name": "Spaces Object Storage", "category": "Storage", "price_per_month": "$5.00", "specs": "250 GB storage, 1 TB transfer", "region": "NYC3"},
            {"name": "Load Balancer", "category": "Networking", "price_per_month": "$12.00", "specs": "Load balancing", "region": "NYC1"},
            {"name": "CDN", "category": "CDN", "price_per_gb": "$0.01", "price_for_1tb": "$10.00", "specs": "Beyond 1 TB free", "region": "Global"}
        ],
        "total_monthly_estimate": "$50-150"
    },
    "Vercel": {
        "services": [
            {"name": "Pro Plan", "category": "Hosting", "price_per_month": "$20.00", "specs": "Unlimited websites, 100 GB bandwidth", "region": "Global"},
            {"name": "Serverless Functions", "category": "Serverless", "price": "Included in Pro", "specs": "1000 GB-hours", "region": "Global"},
            {"name": "Edge Network", "category": "CDN", "price": "Included", "specs": "Global CDN", "region": "Global"}
        ],
        "total_monthly_estimate": "$20-80"
    },
    "Heroku": {
        "services": [
            {"name": "Eco Dyno", "category": "Compute", "price_per_month": "$5.00", "specs": "512 MB RAM, sleeps after 30 min", "region": "US"},
            {"name": "Basic Dyno", "category": "Compute", "price_per_month": "$7.00", "specs": "512 MB RAM, never sleeps", "region": "US"},
            {"name": "Postgres Mini", "category": "Database", "price_per_month": "$5.00", "specs": "1 GB storage, 20 connections", "region": "US"},
            {"name": "Redis Mini", "category": "Cache", "price_per_month": "$3.00", "specs": "25 MB RAM", "region": "US"}
        ],
        "total_monthly_estimate": "$20-50"
    }
}

