# __title__ = “ENG655 Password Cracking Coursework Team Code”
# __author__ = “UP619480”. “UP636396”, “UP617249”,
# __version__ = "1.0”
# __email__ = “up619480@myport.ac.uk”, “up636396@myport.ac.uk”, “617249@myport.ac.uk”,
# __status__ = Complete

from crypt import *
import datetime
import os
import string

def cls():
	os.system('clear')

def main():
	cls()
	hashlist, userlist, resultsTable, numOfTestsRan = initialiseProgram()
	while True:
		choice = 1
		printMenu()
		choice = raw_input("Please choose an option: ")
		# Choice validation; if choice is a digit and between 1 and 7, continue...
		if choice.isdigit() == False or 1 > eval(choice) > 6:
			print("Please enter valid choice.")
		else:
			# carry out selected command
			choice = eval(choice)
			if choice == 1:
				dictionary = getDict()
				hashlist, userlist, resultsTable, finishTime, numOfTestsRan =  dictAttack(hashlist, userlist, resultsTable, dictionary, numOfTestsRan)
				dictionary.close()
				printResults(hashlist, userlist, resultsTable, finishTime)
			elif choice == 2:
				hashlist, userlist, resultsTable, finishTime, numOfTestsRan = maskAttack(hashlist, userlist, resultsTable, numOfTestsRan)
				printResults(hashlist, userlist, resultsTable, finishTime)
			elif choice == 3:
				if numOfTestsRan >= 1:
					printResults(hashlist, userlist, resultsTable, finishTime)
				else:
					print("+-----------------------------------+")
					print("No results to print! Please select an option...")
					print("+-----------------------------------+")
			elif choice == 4:
				saveToFile(hashlist, userlist, resultsTable)
			elif choice == 5:
				print("Goodbye")
				exit()

def initialiseProgram():
	numOfTestsRan = 0
	print("+-----------------------------------+")
	print("              Group 5")
	print("+-----------------------------------+")
	passwdFileName = raw_input("Please enter the name of the .txt target password file (excluding file extension): ")
	print("+-----------------------------------+")
	while(os.path.exists(passwdFileName + ".txt") == 0):
		print("File does not exist")
		print("Ensure the target password file is written correctly and within the same directory as cracker.py") 
		print("+-----------------------------------+")
		passwdFileName = raw_input("Please enter the name of the .txt target password file (excluding file extension): ")
		print("+-----------------------------------+")
	passwdFile = open(passwdFileName + ".txt", "r") 	# open group password list for reading
	hashlist = [] 
	userlist = []					# create an empty list
	for line in passwdFile: 			# for every line in the password file...
		if line.isspace() == 0: 		# if the line does not contain only spaces...
			# split the line into groups at the points where there are semi-colons
			# and add the 2nd group (the passsword section) to the hashlist
			hashlist.append((line.split(":",2))[1])
			userlist.append((line.split(":",2))[0])

	# initialise empty table ready to fill wih results
	initTable = []
	return hashlist, userlist, initTable, numOfTestsRan
	
def printMenu():
	print("1: Dictionary attack")
	print("2: Mask attack")
	print("3: Print current results to screen")
	print("4: Save results to .txt AND .csv file")
	print("5: Exit")
	print("+-----------------------------------+")
	
def printResults(hashlist, userlist, resultsTable, finishTime):
	print; print
	print("RESULTS TABLE")
	print("______________________________")
	print("Uncracked Hashes:")
	if (len(hashlist) == 0):
		print("All hashes cracked!")
	else:
		for i in range(len(hashlist)):
			print(hashlist[i])
	print("+-----------------------------------+")
	print("Cracked Hashes")
	for i in range(len(resultsTable)):
		print("User:     " + str(resultsTable[i][0]))
		print("Hash:     " + str(resultsTable[i][1]))
		print("Password: " + str(resultsTable[i][2]))
		print("Time:     " + str(resultsTable[i][3]))
		print("+-----------------------------------+")
	print("TOTAL PASSWORDS CRACKED: " + str(len(resultsTable)))
	print("+-----------------------------------+")
	print("TOTAL TIME ELAPSED: " + str(finishTime))
	print("+-----------------------------------+")
	
def saveToFile(hashlist, userlist, resultsTable):
	resultsFilePath = raw_input("Enter file name, excluding file extensions: ")
	# check to see if file exists6
	if os.path.exists(resultsFilePath + ".txt") == 1 or os.path.exists(resultsFilePath + ".csv")  == 1:
		overwriteResponse = raw_input("The file currently exists. Would you like to overwrite? (y/n): ")
		# check if answer is valid (y/n)
		while overwriteResponse.upper() != "Y" and overwriteResponse.upper() != "N":
			print("Please enter y or n.")
			overwriteResponse = raw_input("The file currently exists. Would you like to overwrite? (y/n): ")
		if overwriteResponse.upper() == "Y":
			writeToTxt(resultsFilePath, resultsTable, hashlist)
			writeToCsv(resultsFilePath, resultsTable, hashlist)
		elif overwriteResponse.upper() == "N":
			newFilePath = raw_input("Enter new path: ")
			writeToTxt(newFilePath, resultsTable, hashlist)
			writeToCsv(newFilePath, resultsTable, hashlist)
	else:
		# if file doesn't already exist, write file
		writeToTxt(resultsFilePath, resultsTable, hashlist)
		writeToCsv(resultsFilePath, resultsTable, hashlist)
		
def writeToTxt(filepath, resultsTable, hashlist):
	resultsTxtFile = open(filepath + ".txt", "w")
	resultsTxtFile.write("Uncracked Hashes:" + "\n")
	for i in range(len(hashlist)):
		resultsTxtFile.write(hashlist[i] + "\n")
	resultsTxtFile.write("-----------------------------------" + "\n")
	for i in range(len(resultsTable)):
		resultsTxtFile.write("User:     " + str(resultsTable[i][0]) + "\n")
		resultsTxtFile.write("Hash:     " + str(resultsTable[i][1]) + "\n")
		resultsTxtFile.write("Password: " + str(resultsTable[i][2]) + "\n")
		resultsTxtFile.write("Time:     " + str(resultsTable[i][3]) + "\n")
		resultsTxtFile.write("-----------------------------------" + "\n")
	resultsTxtFile.close()

def writeToCsv(filepath, resultsTable, hashlist):
	resultsCsvFile = open(filepath + ".csv", "w")
	for i in range(len(hashlist)):
		resultsCsvFile.write(hashlist[i] + ",")
	for i in range(len(resultsTable)):
		resultsCsvFile.write("\n")
		for j in range(len(resultsTable[0])):
			resultsCsvFile.write(str(resultsTable[i][j]) + ",")
			
	resultsCsvFile.close()
		
def getDict():
	j = 0
	while j==0:
		dictName = raw_input("Enter the .txt wordlist filename (excluding file extension): ")
		if os.path.exists("Wordlists/"+dictName+".txt") == False:
			print("File does not exist")
		else:
			dictionary = open("Wordlists/"+dictName+".txt", "r")
			j = j + 1
	return(dictionary)

def dictAttack(hashlist, userlist, resultsTable, dictionary, numOfTestsRan):
	numOfTestsRan += 1
	salt = "aa"
	startTime = datetime.datetime.now()
	# for every entry in the dictionary
	for entry in dictionary:
		entry = entry.strip() # remove leading/trailing spaces
		entryhash = crypt(entry, salt) # hash the entry
		for i in range(len(hashlist) -1, -1, -1): # for every hash in the hashfile...
			if entryhash == hashlist[i]: # if the dictionary hash is the same as the hashfile hash...
				# create new row/list to store in results table
				finishTime = datetime.datetime.now() - startTime
				newPasswordEntry = [userlist[i], hashlist[i], entry, finishTime]
				resultsTable.append(newPasswordEntry)
				# remove hash from list so it won't be searched again
				del hashlist[i]
	dictionary.close()
	finishTime = datetime.datetime.now() - startTime
	return hashlist, userlist, resultsTable, finishTime, numOfTestsRan

def maskAttack(hashlist, userlist, resultsTable, numOfTestsRan):
	numOfTestsRan += 1
	mask = list(raw_input("Enter the mask: "))
	while (len(mask) % 2) > 0 or (mask.count('%')) != (len(mask) / 2):
		print("+-----------------------------------+")
		print("Please enter a valid mask option, ensure you are including a '%' per mask")
		print("Valid mask options:")
		print("\t%a = alphanumeric\n\t%d = digits\n\t%l = lowercase\n\t%u = uppercase\n\t%p = punctuation\n\t%e = all")
		print("+-----------------------------------+")
		mask = list(raw_input("Enter the mask: "))
	increment = raw_input("Increment from zero to length of input mask (" + str((len(mask)) / 2) +")? (y/n) : ")
	while increment.upper() != "Y" and increment.upper() != "N":
		print("+-----------------------------------+")
		print("Please enter y or n")
		print("+-----------------------------------+")
		increment = raw_input("Increment from zero to length of input mask (" + str((len(mask)) / 2) +")? (y/n) : ")
	n = raw_input("How many hours do you wish to execute this attack mode for (0 for until the end): ")
	while n.isdigit() == False:
		print("+-----------------------------------+")
		print("Please enter a digit")
		print("+-----------------------------------+")
		n = raw_input("How many hours do you wish to execute this attack mode for (0 for until the end): ")
	global timeToFinish
	startTime = datetime.datetime.now()
	timeToFinish = startTime + datetime.timedelta(hours=eval(n))
	hashlist, userlist, resultsTable = maskRecurse(mask, hashlist, userlist, resultsTable, startTime, increment)
	finishTime = datetime.datetime.now() - startTime
	return hashlist, userlist, resultsTable, finishTime, numOfTestsRan
	
def maskRecurse(mask, hashlist, userlist, resultsTable, startTime, increment):
	if timeToFinish != startTime:
		if datetime.datetime.now() >= timeToFinish:
			return hashlist, userlist, resultsTable
	if increment.upper() == "Y":
		every = ["NULL"]
		alphanumeric  = ["NULL"]
		punctuation = ["NULL"]
		digits = ["NULL"]
		lower = ["NULL"]
		upper = ["NULL"]
	else:
		every = []
		alphanumeric  = []
		punctuation = []
		digits = []
		lower = []
		upper = []
	alphanumeric.extend(string.digits)
	alphanumeric.extend(string.ascii_letters)
	lower.extend(string.ascii_lowercase)
	upper.extend(string.ascii_uppercase)
	punctuation.extend(string.punctuation)
	punctuation[punctuation.index("%")] = "PC"
	every.extend(alphanumeric)
	every.extend(punctuation)
	digits.extend(string.digits)
	if mask.count("%") > 0:
		replace = mask.index("%")	
		del mask[replace]
		if mask[replace] == "%":
			mask[replace] == "RR"
			maskRecurse(mask, hashlist, userlist, resultsTable, startTime)
		elif mask[replace] == "a":
			for char in alphanumeric:
				newMask = list(mask)
				newMask[replace] = char
				maskRecurse(newMask, hashlist, userlist, resultsTable, startTime, increment)
		elif mask[replace] == "d":
			for char in digits:
				newMask = list(mask)
				newMask[replace] = char
				maskRecurse(newMask, hashlist, userlist, resultsTable, startTime, increment)
		elif mask[replace] == "l":
			for char in lower:
				newMask = list(mask)
				newMask[replace] = char
				maskRecurse(newMask, hashlist, userlist, resultsTable, startTime, increment)
		elif mask[replace] == "u":
			for char in upper:
				newMask = list(mask)
				newMask[replace] = char
				maskRecurse(newMask, hashlist, userlist, resultsTable, startTime, increment)
		elif mask[replace] == "p":
			for char in punctuation:
				newMask = list(mask)
				newMask[replace] = char
				maskRecurse(newMask, hashlist, userlist, resultsTable, startTime, increment)
		elif mask[replace] == "e":
			for char in every:
				newMask = list(mask)
				newMask[replace] = char
				maskRecurse(newMask, hashlist, userlist, resultsTable, startTime, increment)
	else:
		hashlist, userlist, resultsTable = maskCrypt(mask, hashlist, userlist, resultsTable, startTime)
	return hashlist, userlist, resultsTable
		
def maskCrypt(mask, hashlist, userlist, resultsTable, startTime):
	while mask.count("NULL") > 0:
		mask.remove("NULL")
	for maskCharIndex in range(len(mask)):
		if mask[maskCharIndex] == "PC":
			mask[maskCharIndex] = "%"
	salt = "aa"
	mask = str("".join(mask))
	maskHash = crypt(mask, salt) # hash the entry
	for i in range(len(hashlist) -1, -1, -1): # for every hash in the hashfile...
		if maskHash == hashlist[i]: # if the dictionary hash is the same as the hashfile hash...
			# create new row/list to store in results table
			finishTime = datetime.datetime.now() - startTime
			newPasswordEntry = [userlist[i], hashlist[i], mask, finishTime]
			resultsTable.append(newPasswordEntry)
			# remove hash from list so it won't be searched again
			del hashlist[i], userlist[i]
	return hashlist, userlist, resultsTable
	
main()
