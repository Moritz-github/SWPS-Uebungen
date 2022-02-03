class Datapoint:
    def __init__(self):
        self.data = None
        self.next = None


class LinkedList:
    def __init__(self):
        self.dp = Datapoint()

    def setValuesFromList(self, values, next_dp=None):
        if next_dp is None:
            next_dp = self.dp

        next_dp.data = values.pop(0)
        if len(values) != 0:
            next_dp.next = Datapoint()
            self.setValuesFromList(values, next_dp.next)

    def getLast(self, next_dp=None):
        next_dp = self.dp if next_dp is None else next_dp

        if next_dp.next is not None:
            return self.getLast(next_dp.next)
        return next_dp


if __name__=="__main__":
    nums = [2, 3, 2, 8, 6, 4]
    linkedList = LinkedList()
    linkedList.setValuesFromList(nums)
    print(linkedList.dp.data)
    print(linkedList.getLast().data)
