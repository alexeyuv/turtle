import pandas as pd
import numpy as np
import math
import itertools
from enum import Enum

class OrderType(Enum):
  supportDesc = 1     
  lexi = 2   

class Apriori:
  def __init__(self, support, orderType, confidence):
    self.support = support / 100
    self.orderType = orderType
    self.confidence = confidence / 100

  def Calculate(self, src):
    self.LoadData(src)
    
    lastCombinations = self.CombineItems(self.data, 1)
    lastFrequency = self.CountFrequency(self.data, lastCombinations)
    
    lastCombinations = [combo for combo in lastCombinations if combo in lastFrequency and self.CalculateSupport(lastFrequency[combo]) >= self.support]
    combinationsNumber = 2

    resultingCombinations = {}
    rules = {}

    for item in lastCombinations:
      resultingCombinations[item] = self.CalculateSupport(lastFrequency[item])

    while (True):
      data, frequency, combinations = self.Iterate(lastFrequency, lastCombinations, combinationsNumber)

      if len(data) == 0:
        break

      lastFrequency = frequency
      lastCombinations = data

      frequencyToAdd = {}

      for item in frequency:
        itemSupport = self.CalculateSupport(frequency[item])

        if itemSupport >= self.support:
          frequencyToAdd[item] = itemSupport

      resultingCombinations.update(frequencyToAdd)

      for frequencyItem in frequency:
        if len(frequencyItem) <= 1:
          continue

        frequencyItemSupport = self.CalculateSupport(frequency[frequencyItem])

        for combinationSize in range(1, len(frequencyItem)):
          for combination in itertools.combinations(frequencyItem, combinationSize):
    
            antecedentFrequency = self.CountFrequency(self.data, [combination])
            antecedentSupport = self.CalculateSupport(antecedentFrequency[combination])

            confidence = frequencyItemSupport / antecedentSupport

            if confidence < self.confidence:
              continue

            consequent = (set(frequencyItem) - set(combination))
            rules[f"({', '.join(combination)}) => ({', '.join(consequent)})"] = confidence

      combinationsNumber += 1

    outputCombinations = self.SortToOutput(resultingCombinations)
    outputRules = self.SortToOutput(rules)

    return [outputCombinations, outputRules]

  def SortToOutput(self, data):
    output = dict()

    if self.orderType == OrderType.lexi:
      output = dict(sorted(data.items(), key=lambda x: str(x[0])))
    else:
      output = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))

    return output

  def Iterate(self, frequency, combinations, combinationsNumber):
    candidates = self.CombineItems(combinations, combinationsNumber)
    newFrequency = self.CountFrequency(self.data, candidates)
    newData = self.Prune(newFrequency, candidates)

    return newData, newFrequency, newData

  def LoadData(self, src):
    sourceData = pd.read_csv(src, sep=r'[;,]', engine='python', header=None, encoding='cp1251')
    self.data = [[item for item in row if pd.notna(item)] for row in sourceData.values.tolist()]

  def CountFrequency(self, data, combinations):
    frequency = {combo: 0 for combo in combinations}
    comboSets = [(combo, set(combo)) for combo in combinations]
    
    for row in data:
      rowSet = set(row)
      for combo, comboSet in comboSets:
        if comboSet.issubset(rowSet):
          frequency[combo] += 1
          
    return {k: v for k, v in frequency.items() if v > 0}

  def Prune(self, frequency, combinations):
    newData = []

    for combination in combinations:
      if not combination in frequency:
        continue

      itemSupport = self.CalculateSupport(frequency[combination])

      if itemSupport >= self.support:
        newData.append(combination)

    return newData

  def CombineItems(self, data, level):
    if level == 1:
      uniques = set()
      for row in data:
        for item in row:
          uniques.add(item)
      combinations = []
      for combo in itertools.combinations(uniques, level):
        combinations.append(combo)
      return combinations

    candidates = set()
    for i in range(len(data)):
      for j in range(i + 1, len(data)):
        item1 = sorted(data[i])
        item2 = sorted(data[j])
        if item1[:-1] == item2[:-1]:
          candidates.add(tuple(sorted(list(set(item1) | set(item2)))))
    return list(candidates)

  def CalculateSupport(self, frequency):
    return frequency / len(self.data)
