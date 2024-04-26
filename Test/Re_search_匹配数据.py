import re

s = '201黄22忠（266PCS）'
# Find the number of pieces using a regular expression
pcs = re.search(r'(\d+)PCS', s)
pcs_num = pcs.group(1) if pcs else 'No PCS found'
print('\n',pcs_num)