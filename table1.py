from forms import pat

tab1 = open('E.OPT')
ven1 = pat.parse(tab1)
tab1.close()

start = (201785, 207810)
result = []

ven2 = pat.rotate(ven1, 900, start)
ven3 = pat.rotate(ven1, -900, start)
ven4 = pat.rotate(ven1, -1800, start)

# result.append(pat.add(start[0], start[1], 100, 100))
result.extend(ven1)
result.extend(pat.move(ven1, (144567, 146162), start))
result.extend(pat.move(ven1, (263433, 146162), start))
result.extend(pat.move(ven2, (200190, 206215), start))
result.extend(pat.move(ven2, (261838, 263433), start))
result.extend(pat.move(ven2, (261838, 144567), start))
result.extend(pat.move(ven3, (207810, 201785), start))
result.extend(pat.move(ven3, (146162, 263433), start))
result.extend(pat.move(ven3, (146162, 144567), start))
result.extend(pat.move(ven4, (206215, 200190), start))
result.extend(pat.move(ven4, (144567, 261838), start))
result.extend(pat.move(ven4, (263433, 261838), start))

result2 = pat.mult(result, 1.25, (204000, 204000))

tab1 = open('EN.PAT', 'w')
tab1.write(pat.build(result))
tab1.close()

tab2 = open('EN2.PAT', 'w')
tab2.write(pat.build(result2))
tab2.close()

dxf1 = open('EN.dxf', 'w')
dxf1.write(pat.dxf(result))
dxf1.close()

dxf2 = open('EN2.dxf', 'w')
dxf2.write(pat.dxf(result2))
dxf2.close()
