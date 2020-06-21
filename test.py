service_line = {
    'change_oil': [1, 2],
    'inflate_tires': [3, 4],
    'diagnostic': [5, 6]
}

if len(service_line['change_oil']) > 0:
    service_line['change_oil'].pop(0)

# if len(service_line['change_oil']) > 1:
next = service_line.get('change_oil')[0]
print(next)
next = service_line.get('change_oil')[0]
print(next)