while True:
    deck1, deck2 = list(map(int, input().split()))
    if deck1 + deck2 == 0:
        break
    cards1 = [int(i) for i in input().split()]
    cards2 = [int(i) for i in input().split()]

    if deck1 + deck2 == 2:
        if cards1[0] == cards2[0]:
            print(0)
    

		