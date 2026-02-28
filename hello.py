
print ("hello pmo")
nome = input("Qual é o seu nome? ")
print(f"Bem-vindo ao time de automação, {nome}!")

quantidade = int(input("Digite o valor do produto: "))
valor= float(input("Digite o valor da venda: "))
total= quantidade* valor
print(f"para  {quantidade}  produtos a {valor} tem de pagar {total:.2f}:.2f")
