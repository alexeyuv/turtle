from apriori import Apriori, OrderType
import matplotlib.pyplot as plt
import time
import csv
import numpy as np

filePath = "baskets.csv"

with open(filePath, mode='r', encoding='cp1251') as f:
  reader = csv.reader(f)
  totalCells = sum(1 for row in reader)

timeData = []
suppData = []
itemsData = []

def RunTest(support):
  startTime = time.perf_counter()

  apriori = Apriori(support=support, orderType=OrderType.supportDesc)
  aprioriData = apriori.Calculate(filePath)

  endTime = time.perf_counter()
  executionTime = endTime - startTime

  timeData.append(executionTime)
  suppData.append(support)
  itemsData.append(len(aprioriData))

  return executionTime

supp1Exec = RunTest(1)
supp1Exec = RunTest(3)
supp1Exec = RunTest(5)
supp1Exec = RunTest(10)
supp1Exec = RunTest(15)
supp1Exec = RunTest(30)
supp1Exec = RunTest(50)
supp1Exec = RunTest(80)
supp1Exec = RunTest(100)

plt.plot(suppData, timeData, linestyle='-', marker='o')
plt.title(f"Быстродействие на фиксированном наборе данных - {totalCells} наборов")
plt.ylabel("Время обработки (сек)")
plt.xlabel("Поддержка (%)")
plt.savefig(f"{filePath}__speed-support.png")

plt.clf()

plt.plot(suppData, itemsData, linestyle='-', marker='o')
plt.title(f"Частые наборы различной длины на фиксированном наборе данных - {totalCells} наборов")
plt.ylabel("Частые наборы (шт)")
plt.xlabel("Поддержка (%)")
plt.savefig(f"{filePath}__items-support.png")