
class MergeSortAlgorithm:
    # merge dwie posortowane listy
    def merge(self, left, right):
        result = []
        li = ri = 0
        while li < len(left) and ri < len(right):
            if left[li] <= right[ri]:
                result.append(left[li])
                li += 1
            else:
                result.append(right[ri])
                ri += 1
        if li == len(left):
            result.extend(right[ri:])
        else:
            result.extend(left[li:])
        return result

    # sortowanie
    def mergesort(self, list):
        if len(list) <= 1:
            return list
        ind = len(list)//2
        return self.merge(self.mergesort(list[:ind]), self.mergesort(list[ind:]))