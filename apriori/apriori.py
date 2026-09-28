import pandas as pd
import numpy as np
import math
import itertools
from enum import Enum

class OrderType(Enum):
  supportDesc = 1     
  lexi = 2   

class Apriori:
  def __init__(self, support, orderType):
    # assuming support is passed in percentages
    self.support = support / 100
    self.orderType = orderType

  def Calculate(self, src):
    self.LoadData(src)
    
    lastData = []
    lastCombinations = self.CombineItems(self.data, 1)
    lastFrequency = self.CountFrequency(self.data, lastCombinations)
    combinationsNumber = 2

    resultingCombinations = {}

    while (True):
      data, frequency, combinations = self.Iterate(lastData, lastCombinations, lastCombinations, combinationsNumber)

      if len(data) == 0:
        break

      lastData = data
      lastFrequency = frequency
      lastCombinations = combinations

      # output frequency since we do not want to change methods to add support to them as well;
      # frequency contains all processed items so have to sort them first
      resultingCombinations.update(frequency)

      combinationsNumber += 1

    outputData = self.SortToOutput(resultingCombinations)
    self.Output(outputData)

    return resultingCombinations

  def SortToOutput(self, data):
    output = dict()

    sortedData = {}

    for item in data:
      itemSupport = self.CalculateSupport(data[item])

      if itemSupport >= self.support:
        sortedData[item] = itemSupport

    if self.orderType == OrderType.lexi:
      output = dict(sorted(sortedData.items(), key=lambda x: x[0]))
    else:
      output = dict(sorted(sortedData.items(), key=lambda x: x[1], reverse=True))

    return output

  def Output(self, data):
    print("Выходные данные:")

    for item in data:
      supportToOutput = data[item] * 100

      print(f"Набор '{', '.join(item)}', поддержка - {supportToOutput:.3f}%")

  def Iterate(self, data, frequency, combinations, combinationsNumber):
    frequency = self.CountFrequency(self.data, combinations)
    newData = self.Prune(frequency, combinations)
    combinations = self.CombineItems(newData, combinationsNumber)

    return newData, frequency, combinations

  def LoadData(self, src):
    sourceData = pd.read_csv(src, sep=r'[;,]', engine='python', header=None, encoding='cp1251')
    self.data = [[item for item in row if pd.notna(item)] for row in sourceData.values.tolist()]

  def CountFrequency(self, data, combinations):
    frequency = {}

    for combination in combinations:
      for row in data:
        if set(combination).issubset(row):
          if combination in frequency:
            frequency[combination] += 1
          else:
            frequency[combination] = 1

    return frequency

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
    uniques = set()

    for row in data:
      for item in row:
        uniques.add(item)
      
    combinations = []

    for combo in itertools.combinations(uniques, level):
      combinations.append(combo)
    
    return combinations

  def CalculateSupport(self, frequency):
    return frequency / len(self.data)
