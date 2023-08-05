from calcutils.calcutils import evalall

all_values = ""

for exp in evalall():
    all_values += "%s;\n" % exp


