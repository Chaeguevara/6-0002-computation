from lecture2 import Food


class Fodd(obejct):
    def __init__(self, n, v, w) -> None:
        self.name = n
        self.value = v
        self.calories = w
    def getValue(self):
        return self.value
    def getCost(self):
        return self.calories
    def density(self):
        return self.getValue()/self.getCost()
    def __str__(self):
        return self.name + ": <" + str(self.value) \
                + ', ' + str(self.calories) + '>'

def buildMenu(names, values, calories):
    menu = []
    # Food class를 만들어서 menu에 넣음
    for i in range(len(values)):
        menu.append(Food(names[i],values[i],calories[i]))
    return menu

def greedy(items, maxCost, keyFunction):
    """items = List, maxCost >= 0,
    KeyFunction은 아이템을 number로 mapping 함"""
    """ Key Idea: maxCost(여기선 calories)를 넘지 않는 한에서특정 값을 기준으로 큰것부터 작은 순서로 Result에 더해나감"""
    #내림차순으로 정렬함.
    itemsCopy = sorted(items, key= keyFunction, reverse= True)
    result = []
    totalValue, totalCost = 0.0, 0.0
    for i in range(len(itemsCopy)):
        # 만약 다음 아이템의 칼로리를 더했을때,  maxCost보다 적다면
        if totalCost+itemsCopy[i].getCost() <= maxCost:
            #list에 더하고
            result.append(itemsCopy[i])
            maxCost += itemsCopy[i].getCost()
            totalValue += itemsCopy[i].getValue()
    return (result, totalValue)

def testGreedy(items, constraint, keyFunction):
    taken, val = greedy(items,constraint, keyFunction)
    print('취한 아이템의 Value 합 = ', val)
    #아이템들 보여주기
    for item in taken:
        print('    ', item)

def testGreedys(foods, maxUnits):
    """ 여러 조건에 대해 한번에 testGreedy를 실행시킴"""
    print('Greedy Algorithm에 사용할 Constraint value', maxUnits, '칼로리')
    #Value를 기준으로 최적값 찾음
    testGreedy(foods,maxUnits,Food.getValue)
    print('\nGreedy Algorithm에 사용할 Constraint value', maxUnits, '칼로리')
    #칼로리가 낮은것 부터
    testGreedy(foods,maxUnits,lambda x: 1/Food.getCost(x))
    print('\nGreedy Algorithm에 사용할 Constraint value', maxUnits, '칼로리')
    #Density가 높은것 부터. 칼로리 대비 Value가 높은것
    testGreedy(foods,maxUnits,Food.density)

def maxVal(toConsider, avail):
    """
    toConsider는 list, avail은 무게
    0/1 Kanpsack문제의 전체 value와 item들을 Return함.
    """
    #Base case
    if toConsider == [] or avail == 0:
        result = (0, ())
    elif toConsider[0].getCost() > avail:
        #오른쪽 브랜치만 탐색함
        result = maxVal(toConsider[1:],avail) 
    else:
        #양쪽다 탐색해야하는 경우
        nextItem = toConsider[0]
        # 왼쪽 브랜치 탐색. 아이템을 하나 고른다
        withVal, withToTake = maxVal(toConsider[1:],avail - nextItem.getCost())
        withVal += nextItem.getValue()
        # 오른쪽 브랜치 탐색
        withoutVal, withoutToTake = maxVal(toConsider[1:],avail)
        #더 나은걸 선택한다
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    return result
