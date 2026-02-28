
# Project: Automated PMO Risk Tracker
# Goal: Automate the formatting of project risks for stakeholder reporting.
project_name = "risk automation"
budget_utilization = 85.5  # Float (percentage)
is_on_track = True         # Boolean
risks = ["Resource shortage", "price changes", "Budget Overrun"] # List
# Adding a new risk found during the week
risks.append("deploy delay")
# Generating the report
report = f"""
--- EXECUTIVE SUMMARY: {project_name} ---
Status: {"GREEN" if is_on_track else "RED"}
Budget Used: {budget_utilization}%

TOP RISKS TO MITIGATE:
1. {risks[0]}
2. {risks[1]}
3. {risks[-2]} 
3. {risks[-1]} 
---------------------------------------
"""
print(report)


#AI Integration Plan
#In V2, I will use an LLM API to automatically categorize these risks into 'High/Medium/Low' priority
#I will use Prompt Engineering to turn this raw data into a professional email notification.