import os		
from multiprocessing.dummy import Pool as ThreadPool


def process(domain):
	global count
	cmd = 'swaks  --from no_reply@test.com --to admin@' + domain +' -ehlo test.com --header \"Subject: This is a mail for testing.\" --body  \"This is a test mail. If you receive this mail, it means your email server lack the authentication for SPF and DMARC. We strongly recommend you to initiate these two authentication protocols.\" > ./log_re/' + domain + '.log'
	#print(cmd)
	os.system(cmd)
	count += 1
	print(count)
	
	

l = open('./mx.txt', 'r').readlines()
items = []
for i in l:
    if ' yes' in i:
        items.append(i.split(' ')[0].replace(' ', ''))
print(len(items))
pool = ThreadPool()
pool.map(process, items)
pool.close()
pool.join()