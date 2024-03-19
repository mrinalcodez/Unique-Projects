# You are playing Dota2 and are currently in the middle lane, which has n
# heroes. Each hero has the following attributes:
# • Position: Given as a 0-indexed integer array. All integers are unique. The index
# in the array refers to a particular hero, and the value at that index indicates the
# position.
# • Health: Given as a 0-indexed integer array. The index in the array refers to a
# particular hero, and the value at that index indicates the health.
# • Team: Given a string (R for radiant, D for Dire).
# All heroes move simultaneously at the same speed on the lane, each going in its given
# direction. Radiant moves up, and Dire moves down the middle lane. If two heroes ever
# meet in the same position, they have a battle. When this happens, the hero with less
# health is removed from the lane, and the health of the other hero drops by one. If both
# heroes have the same health, they both get removed.
# Return an array containing the health of the remaining heroes (in the order they were
# given in the input), after no further battle can occur.
# Constraint :
# • 1 ≤ positions.length, healths.length ≤ 105
# • 1 ≤ healths[i], positions[i] ≤ 109

# Input: positions = [5,4,3,2,1], healths = [2,17,9,15,10], Team = "RRRRR"
# Output: [2,17,9,15,10]
# Explanation: No fight occurs in this example since all heroes move in the
# same direction.
# So, all the heroes’ health is returned in initial order [2, 17, 9, 15, 10].
# Input: positions = [3,5,2,6], healths = [10,10,15,12], Team = "RDRD"
# Output: [14]
# Explanation: There are 2 battles in this example. Firstly, hero 0 and hero 1
# will fight, and since both have the same health, they will be removed.
# Next, Hero 2 and Hero 3 will fight, and since Hero 3’s health is less
# it gets removed, and Hero 3’s health becomes 15 - 1 = 14.
# Only Hero 3 remains, so we return [14].

# Input: positions = [1,2,5,6], healths = [10,10,11,11], Team = "RDRD"
# Output: []
# Explanation: hero 0 and Hero 1 will fight, and since they
# have the same health, they are removed.
# Hero 3 and 4 will fight, and since they have the same health, they are removed.
# So, we return an empty array [].

# Extra test cases :
# Input: positions = [2,19,46], healths = [42,45,2], Team = "DRD"
# Output: [42,44]
# Input: positions = [2,3,21,22,24,25,38,31], healths =[24,33,31,37,19,16,11,50],
# Team = "DDRDDRDR"
# Output: [24,33,36,19,16,49]



positions = eval(input())

team = list(input())

healths = eval(input())

output = []
i = 0
while i < len(team)-1 or i < len(team)-2:
  if i == len(team)-1:
    output.append(healths[i])
    i += 1
    continue
  elif i == len(team)-2:
    if team[i]+team[i+1] == 'DD' or team[i]+team[i+1] == 'RR':
      output.append(healths[i])
      output.append(healths[i+1])
      i += 2
    elif team[i]+team[i+1] == 'DR' or team[i]+team[i+1] == 'RD':
      if healths[i] > healths[i+1]:
        output.append(healths[i]-1)
        i += 2
      elif healths[i+1] > healths[i]:
        output.append(healths[i+1]-1)
        i += 2
      elif healths[i] == healths[i+1]:
        i += 2
  elif team[i]+team[i+1] == 'DD' or team[i]+team[i+1] == 'RR':
    output.append(healths[i])
    i += 1
    continue
  elif team[i]+team[i+1] == 'DR':
    if positions[i] < positions[i+1]:
      output.append(healths[i])
      i += 1
      continue
    elif positions[i] > positions[i+1]:
      if team[i+2] == team[i]:
        if positions[i+2] > positions[i+1] and abs(positions[i+2]-positions[i+1]) < abs(positions[i+1]-positions[i]):
          output.append(healths[i])
          i += 1
          continue
      if healths[i+1] > healths[i]:
        output.append(healths[i+1]-1)
        i += 2
      elif healths[i+1] < healths[i]:
        output.append(healths[i]-1)
        i += 2
      elif healths[i] == healths[i+1]:
        i += 2
      continue
  elif team[i]+team[i+1] =='RD':
    if positions[i] > positions[i+1]:
      output.append(healths[i])
      i += 1
      continue
    elif positions[i] < positions[i+1]:
      if team[i+2] == team[i]:
        if positions[i+2] < positions[i+1] and abs(positions[i+2]-positions[i+1]) < abs(positions[i+1]-positions[i]):
          output.append(healths[i])
          i += 1
          continue
      if healths[i+1] > healths[i]:
        output.append(healths[i+1]-1)
        i += 2
      elif healths[i] > healths[i+1]:
        output.append(healths[i]-1)
        i += 2
      elif healths[i] == healths[i+1]:
        i += 2
      continue
print(output)
