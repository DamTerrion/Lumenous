from forms import lum, dxf, pat
from base import confirm, local

conf_data = open('lum.conf')
config = dict(
    (line.partition('=')[0].strip(),
     line.partition('=')[2].strip() )
    for line in conf_data)
conf_data.close()
