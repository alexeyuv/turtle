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
confData = []
itemsData = []

supportValue = 2 

def RunTest(support, confidence):
  startTime = time.perf_counter()

  apriori = Apriori(support=support, confidence=confidence, orderType=OrderType.supportDesc)
  calculatedCombinations, calculatedRules = apriori.Calculate(filePath)

  endTime = time.perf_counter()
  executionTime = endTime - startTime

  timeData.append(executionTime)
  suppData.append(support)
  confData.append(confidence)
  itemsData.append(len(calculatedRules))

  return executionTime

supp1Exec = RunTest(supportValue, 1)
supp1Exec = RunTest(supportValue, 3)
supp1Exec = RunTest(supportValue, 5)
supp1Exec = RunTest(supportValue, 10)
supp1Exec = RunTest(supportValue, 15)
supp1Exec = RunTest(supportValue, 30)
supp1Exec = RunTest(supportValue, 50)
supp1Exec = RunTest(supportValue, 80)
supp1Exec = RunTest(supportValue, 100)

plt.plot(confData, timeData, linestyle='-', marker='o')
plt.title(f"Быстродействие на фиксированном наборе данных - {totalCells} наборов", fontsize=12)
plt.ylabel("Время обработки (сек)")
plt.xlabel("Достоверность (%)")
plt.figtext(
    0.6, 0.0001, 
    f"Значение поддержки постоянно и равно {supportValue}%", 
    horizontalalignment='right', 
    fontsize=10, 
    fontstyle='italic',
    color='gray'
)
plt.savefig(f"{filePath}__speed-support.png")

plt.clf()

print(confData, itemsData)

plt.plot(confData, itemsData, linestyle='-', marker='o')
plt.title(f"Частые наборы различной длины на фиксированном наборе данных - {totalCells} наборов", fontsize=10)
plt.ylabel("Частые наборы (шт)")
plt.xlabel("Достоверность (%)")
plt.savefig(f"{filePath}__items-support.png")