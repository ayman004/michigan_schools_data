#Import all the required libraries
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
import time
from time import sleep


start = time.time()

browser = webdriver.Firefox()
#browser = webdriver.Chrome()


#read the csv
schools = pd.read_csv('schools.csv')
schools = schools.drop_duplicates()

record = []

print('School Name\t\t\t\t\t\t\tContacts')
checked_school = set()

#Here we get the result of the first search and store in a list
for k in range(len(schools)):
	school_search = schools.loc[k]['school']
	school_search = re.sub("'","",school_search)
	browser.get("https://www.mhsaa.com/Schools")
	sleep(2)
	try:
		search = browser.find_element_by_name("dnn$ctr4469$Dispatch$Default$SchoolSearchControl$txtSearchTerm")
		sleep(2)
		search.send_keys(school_search)
	except Exception:
		continue
	sleep(3)
	try:
		search_result = browser.find_elements_by_class_name("autocomplete")
		
	except Exception as e:
		print("error:", str(e))
		continue
	found_schools = []
	#Here, We loop through the list from the first search
	for value in search_result:
			text = value.text
			data = re.sub('\\n', ',',text)
			found_schools = data.split(',')
	found_schools = set(found_schools)
	found_schools = list(found_schools)
	found_schools = sorted(found_schools)
	if found_schools:
		for i in range(len(found_schools)):
				sc = found_schools[i]
				if sc not in checked_school:
					
					browser.get("https://www.mhsaa.com/Schools")
					sleep(2)
					search = browser.find_element_by_name("dnn$ctr4469$Dispatch$Default$SchoolSearchControl$txtSearchTerm")
					search.send_keys(sc)
					sleep(4)
					loc = found_schools.index(sc)
					for j in range(loc+1):
						search.send_keys(Keys.ARROW_DOWN)
						sleep(1)
					
					search.send_keys(Keys.RETURN)
					sleep(2)
					try:
						sleep(3)
						school_name = browser.find_element_by_xpath("/html/body/form/div[3]/div[2]/div[1]/div[2]/div[1]/div/div/div/div/div[2]/h1")
						school_name = school_name.text
					except Exception as e:
						checked_school.add(sc)
						continue
						
					try:
						sleep(2)
						contacts = browser.find_element_by_xpath("//*[@id='dnn_ctr4477_Dispatch_Default_lblPhone']")
						contacts = contacts.text

					except Exception as e:
						contacts = 'N/A'
					if contacts:
						pass
					else:
						contacts = 'N/A'
					print(school_name,' '*(60 - len(school_name)),contacts)	
					checked_school.add(sc)
				try:
					record.append([school_name,contacts])
				except Exception:
					continue

#Close the browser
browser.quit()

#Create a dataframe
try:
	df = pd.DataFrame(record)
except Exception as e:
	print(str(e))

#Give the data column names
df.columns = ['School Name', 'Contacts']
	
#Drop duplicates
df = df.drop_duplicates()

#Give a filename based on current timestamp
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
now = now.replace(':','-')
now = 'Contacts at '+now+'.csv'
df.to_csv(now, index=False)

#Or you could just do this
#df.to_csv('contacts.csv', index=False)



#Calculates the time that the script takes to run
finish = time.time()	
print("it took:{0} seconds".format(str(finish - start)))
	
	
	
