import soil

data_ref = soil.data([i for i in range(50)])

soil.alias('my_data2', data_ref)

data_ref2 = soil.data('my_data2')
for i in data_ref2.data:
    print(i)
