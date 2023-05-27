import spf
import dmarc
import dns.resolver
import os
import re


#void lookup校验
#return value:
#0:ok; 1:have void lookup
def void_lookup_check(domain, record, q):
	#q = spf.query(s='test@sjtu.edu.cn', h='mx.sjtu.edu.cn', i='202.112.26.0')
	if "%{" in record:
		return 0	
	if 'No valid SPF record' in q.check(record)[2]:
		return 1
	return 0

	if 0:
		pattern = r'(include|exists)[:=]?([\w\.\-]+)'
		match = re.findall(pattern, record)
		domains = [m[1] for m in match]
		if len(domains) > 0:
			for i in domains:
				#bypass macro
				if "%{" not in i:	
					try:	
						spf_records = os.popen("dig +short TXT " + i).readlines()
						flag = 1
						for spf_record in spf_records:
							if 'v=spf' in spf_record:
								flag = void_lookup_check(i, spf_record)
						if flag == 1:
							return 1
					except:
						continue
		return 0

#lookup数量校验
#return lookup count value: 
def lookup_count(domain, record, q):
	#q = spf.query(s='test@sjtu.edu.cn', h='mx.sjtu.edu.cn', i='202.112.26.0')
	if 'Too many DNS lookups' in q.check(record)[2]:
		return False
	return True


#检查SPF记录是否包含已经废弃的机制
def check_deprecated(domain):
	try:
		records = os.popen("dig +short SPF " + domain).readlines()
		for r in records:
			if 'v=spf1' in r:
				return False
		return True
	except:
		return True

# 检查SPF记录是否存在语法问题
def spf_syntax_check(spf_record, q):	
	if 'permerror' in q.check(record):
		return False
	return True	
	
	
# 校验SPF记录
#0:valid, 1:systax error, 2:Too Many Included Lookups, 3:Void Lookup, 4:SPF Record Deprecated, 5:Multiple SPF Records
def validate_spf_record(domain, record, q):
	spf_record_count = 0
	# 检查是否存在多个SPF记录
	spf_records = os.popen("dig +short TXT " + domain).readlines()
	for spf_record in spf_records:
		if 'v=spf' in spf_record:
			spf_record_count += 1
	if spf_record_count > 1:
		return '5'
	
	# 空lookup校验
	if void_lookup_check(domain, record, q) == 1:
		return '3'
	
	# lookup数量校验
	#if lookup_count(domain, record) > 10:
	if lookup_count(domain, record, q) == False:
		return '2'	
	
	#检查SPF记录是否包含已经废弃的机制
	if check_deprecated(domain) == False:
		return '4'

	if spf_syntax_check(record, q) == False:
		return '1'
	
	return '0'


def get_spf_all_prefix(domain, record):
	#parsed_spf = spf.parse(record)

	if 'all' in record:
    		prefix = record.split('all')[0][-1]
    		if prefix == '-':
    			return 'hard fail'
    		elif prefix == '~':
    			return 'soft fail'
    		elif prefix == '?':
    			return 'neutral'
    		elif prefix == '+':
    			return 'pass'
    		else:
    			return 'null'
	elif 'redirect=' in record:
		re_domain = record.split("redirect=")[1].split('\\')[0].replace('\n', '')
		if ' ' in re_domain:
			re_domain = re_domain.split(' ')[0]
		spf_records = os.popen("dig +short TXT " + re_domain).readlines()
		#spf_records = spf.query(domain, 'txt')
		for spf_record in spf_records:
			if 'v=spf' in spf_record:
				return get_spf_all_prefix(re_domain, spf_record.replace('\"', '').replace('\n', ''))
		return "null" 			
	else:
		return "null"



# 检查SPF记录是否存在语法问题
def dmarc_syntax_check(domain_, record_):	
	d = dmarc.DMARC()
	try:
		p = d.parse_record(record=record_, domain = domain_)
	except:
		return False	
	return True


#dmarc validation check
#return result:
#0:ok, 1:syntax error, 2:multiple dmarc records, 3:using none policy, 10:no dmarc record found
def validate_dmarc_record(domain, record):
	#multiple dmarc records checking
	try:
		dmarc_records = os.popen("dig +short TXT _dmarc." + domain).readlines()
		count = 0
		for dmarc_record in dmarc_records:
			if 'v=DMARC' in dmarc_record or 'v=dmarc' in dmarc_record:
				count += 1
		if count > 1:
			return '2'
	except:
		pass
	
	#syntax checking
	if dmarc_syntax_check(domain, record) == False:
		return '1'	
	
	#none policy checking
	#if ' p=none' in record:
	#	return '3'


	return '0'


def get_dmarc_result(domain, record):
	result = ''
	
	#dmarc validation check
	result += validate_dmarc_record(domain, record) + ','
	
	
	#get policy
	if ';p=reject' in record or ' p=reject' in record:
		result += 'reject,'
	elif ' p=none' in record or ';p=none' in record:
		result += 'none,'
	elif ' p=quarantine' in record or ';p=quarantine' in record:
		result += 'quarantine,'
	else:
		result += 'null,'
	
	#get subdomain policy
	if ' sp=reject' in record or ';sp=reject' in record:
		result += 'reject,'
	elif ' sp=none' in record or ';sp=none' in record:
		result += 'none,'
	elif ' sp=quarantine' in record or ';sp=quarantine' in record:
		result += 'quarantine,'
	else:
		result += 'null,'
	
	#get rua info
	if ' rua=mailto:' in record or ';rua=mailto:' in record:
		result += 'True,'
	else:
		result += 'False,'
		
	#get ruf info
	if ' ruf=mailto:' in record or ';ruf=mailto:' in record:
		result += 'True'
	else:
		result += 'False'	
		
	return result
