my_role="pmo"
print(my_role)
print("house is clean")


balance=5000
budget=6000
if balance > budget:
    overbuget=True
    over= balance - budget
    print(f"the project is overbuget by {over}")
else:
    print("fine")

projet="p"
manager="c"
status="late"
dad="friday"

print(f"the prject {projet} is managed by {manager} and is {status}, it has a deadline on {dad}")

name="ed"
time="8am"
day= "monday"
print(f"{name} satarts On {day}, at {time}.")

status= "Aproved"
Project="BBVA"
Budjet= 50000 
spent= 1000
print(f"the {Project} poject is {status} with a bujet of {Budjet}")
def overbudget(budget,spent):
    budget = 5000
    spent = 2450.50
    balance = budget - spent
    is_over_budget = balance < 0
    return balance, is_over_budget

balance, is_over_budjet=overbudget(budget,spent)
def calculo_temp(temp):
    temp= 10
    calc= temp * 9/5+32
    return calc

#list
pmo_list= ["work","clean","eat"]

print(f"my firt priority is {pmo_list[0]}")
# new task
pmo_list.append("sleep")
print(f"my firt priority is {pmo_list}")
#new list
cleaned_rooms=["kitchen"]
cleaned_rooms.append("bathroom")
cleaned_rooms.append("bedroom")
print (cleaned_rooms)
cleaned_rooms.remove("bedroom")
cleaned_rooms.pop(1)
print (cleaned_rooms)
room = "kitchen" in cleaned_rooms or "bathroom" in cleaned_rooms
"bedroom" not in cleaned_rooms
   
    
# 1. Setup your project list
project_list = ["Digital Transformation", "Quarterly Audit", "Staff Training"]

# 2. Add a new high-priority project
project_list.append("AI Implementation")

# 3. Create a status variable
status = "On Track"

# 4. Print the automated update
print("--- WEEKLY STATUS REPORT ---")
print(f"Active Projects: {project_list}")
print(f"The priority project '{project_list[3]}' is currently {status}.")