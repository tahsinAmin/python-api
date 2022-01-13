while True:
    deck1, deck2 = list(map(int, input().split()))
    if deck1 + deck2 == 0:
        break
    cards1 = [int(i) for i in input().split()]
    cards2 = [int(i) for i in input().split()]

    cards1 = set(cards1)
    cards2 = set(cards2)

    cards1 = list(cards1)
    cards2 = list(cards2)

    cards1.sort()
    cards2.sort()

    # print(cards1,cards2)

    if len(cards1) < len(cards2):
        smallList = cards1
        bigList = cards2
    else:
        smallList = cards2
        bigList = cards1

    cnt = 0
    for element in smallList:
        cnt+= 1 if element not in bigList else 0
    print(cnt)