import os
from apriori import Apriori, OrderType

while True:
  filePath = input("Введите путь к файлу: ").strip()
    
  if os.path.exists(filePath):
    break
  else:
    print("Файл не найден. Попробуйте еще раз")

try:
  support = float(input("Введите значение поддержки (%): "))
except ValueError:
  print("Введено не число. Установлено значение по умолчанию - 15")
  support = 15

print("\nДоступные типы сортировки:")
print("1 — Сортировка по убыванию поддержки")
print("2 — Лексикографическая сортировка")

sortChoice = input("Выберите тип сортировки: ")

if sortChoice == "1" or sortChoice.lower() == "supportdesc":
  orderType = OrderType.supportDesc
elif sortChoice == "2" or sortChoice.lower() == "lexi":
  orderType = OrderType.lexi
else:
  print("Неверный выбор. Установлен тип по умолчанию - supportDesc")
  orderType = OrderType.supportDesc

apriori = Apriori(support=support, orderType=orderType)
apriori.Calculate(filePath)