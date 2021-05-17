class TestCase:
    def __init__(self, intervals, treshold):
        self.intervals = intervals
        self.threshold = treshold

def merge_intervals(intervals, treshold):
    number_of_intervals = len(intervals)
    if number_of_intervals == 0:
        return []

    intervals.sort(key = lambda interval: interval[0])

    merged_intervals = []
    merged_intervals.append(intervals[0])

    for index in range(number_of_intervals - 1):
        original_interval = intervals[index + 1]

        merged_interval = merged_intervals.pop()

        interval_distance = merged_interval[1] - original_interval[0]
        
        if interval_distance > 0:
            #if one interval contains another
            if original_interval[1] < merged_interval[1]:
                merged_intervals.append(merged_interval)
                continue
            #if one interval overlaps with another
            else:
                merged_interval[1] = original_interval[1]
                merged_intervals.append(merged_interval)
                continue

        #if there is no intersection
        if abs(interval_distance) <= treshold:
            merged_interval[1] = original_interval[1]
            merged_intervals.append(merged_interval)
        else:
            merged_intervals.append(merged_interval)
            merged_intervals.append(original_interval)

    return merged_intervals

if __name__ == "__main__":
    test_cases = list()
    test_cases.append(TestCase([[100, 300], [0, 1200], [3500, 6000]], 400))
    test_cases.append(TestCase([[0, 300], [200, 1200], [3500, 6000]], 100))
    test_cases.append(TestCase([[0, 300], [600, 1200], [3500, 6000]], 2500))
    test_cases.append(TestCase([], 2500))
    for test in test_cases:
        print(merge_intervals(test.intervals, test.threshold))
    print('Program finished')
