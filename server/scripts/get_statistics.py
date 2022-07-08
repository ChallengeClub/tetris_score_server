data = list(map(int, input().split()))

from statistics import mean, median,variance,stdev

m = mean(data)
median = median(data)
variance = variance(data)
stdev = stdev(data)
print('mean: {0:.2f}'.format(m))
print('median: {0:.2f}'.format(median))
print('variance: {0:.2f}'.format(variance))
print('stdev: {0:.2f}'.format(stdev))
print('max: {}'.format(max(data)))
print('min: {}'.format(min(data)))
print('num: {}'.format(len(data)))
