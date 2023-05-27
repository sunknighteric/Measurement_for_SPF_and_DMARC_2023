import os


def spf_sub():
	f = open("./top-1m-spf-no.csv", "r")
	count_1 = 0
	count_2 = 0
	l = f.readlines()
	f.close()
	print(len(l))
	f = open("./spf_sub.txt", "w+")
	for k in l:
		var = os.popen("dig +short TXT *." + k).readlines()
		if  len(var) == 0:
			f.write(k + ";no" +"\n")
			count_1 = count_1 + 1
			print(count_1+count_2)
		else:
			spf = ""
			for i in var:
				if i.find("\"v=spf1") >= 0 or i.find("\"=spf") >= 0:
					spf = i
					break
			if spf == "":
				f.write(k + ";no" +"\n")
				count_1 = count_1 + 1
			else:	
				f.write(k + ";" + spf.replace("\n","") + "\n")
				count_2 = count_2 + 1
				print("sub")
	
	print(count_1)
	f.close()



def dmarc():
	f = open("./top-1m-no.csv", "r")
	count_1 = 0
	count_2 = 0
	l = f.readlines()
	f.close()
	print(len(l))
	f_d = open("./dmarc.txt", "a")    
	print(len(l))
	for k in l:
		var = os.popen("dig +short TXT _dmarc." + k).readline()
		if  var == "":
			f_d.write(k.replace("\n", "") + ";no" +"\n")
			count_1 = count_1 + 1
			print(count_1+count_2)
			print("no")
		else:
			d = var.replace("\n","").replace("\"", "") 
			#for j in var:	
			#	d += j.replace("\n","").replace("\"", "") + ";"
			f_d.write(k.replace("\n", "") + ";" + d + "\n")
			count_2 = count_2 + 1
			print(count_1+count_2)
			print(d)
	f_d.close()


def mx():
	f = open("./top-1m-no.csv", "r")
	count_1 = 0
	count_2 = 0
	#l = f.readlines()[55000:133000]
	l = f.readlines()#[50000:60000]
	f.close()
	print(len(l))
	f_spf = open("./spf.txt", "w")
	f_mx = open("./mx.txt", "w")
    
	print(len(l))
	for k in l:
		if os.popen("dig +short MX " + k).readline() == "":
			f_mx.write(k.replace("\n", "") + " no" +"\n")
			count_1 = count_1 + 1
			#print(11)
			print(count_1+count_2)
		else:
			f_mx.write(k.replace("\n", "") + " yes" +"\n")
			count_2 = count_2 + 1
			#print(22)
			print(count_1+count_2)
	f_mx.close()
	


def spf():
    f = open("./top-1m-no.csv", "r")
	count_1 = 0
	count_2 = 0
	l = f.readlines()
	f.close()
	print(len(l))
	f_spf = open("./spf.txt", "w")

	for k in l:
		var = os.popen("dig +short TXT " + k).readlines()
		if  len(var) == 0:
			f_spf.write(k.replace("\n", "") + ";null" +"\n")
			count_1 = count_1 + 1
			print(count_1+count_2)
		else:
			spf = ""
			for i in var:
				if i.find("\"v=spf1") >= 0 or i.find("\"=spf") >= 0:
					spf = i
					break
			if spf == "":
				f_spf.write(k.replace("\n", "") + ";null" +"\n")
				count_1 = count_1 + 1
			else:	
				f_spf.write(k.replace("\n", "") + ";" + spf.replace("\n","") + "\n")
				count_2 = count_2 + 1
				print("sub")
	
	print(count_1)
	print(count_2)
	f_spf.close()