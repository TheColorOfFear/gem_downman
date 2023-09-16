import requests
import os
import readchar

def input_key(prompt: str, /, *, echo: bool = True) -> str:
    print(prompt, end='', flush=True)
    key = readchar.readkey()

    if echo:
        print(key)
    else:
        print()
    return key

escape = "\033["

downloadDir = "./download/"
urlListFile = "./url.txt"

online = True
compact = False

def refresh(online=True):
	fileListFile = "./FileList.txt" 
	if online:
		urlList = open(urlListFile, "r")
		urlListList = urlList.read().splitlines()
		urlList.close()
		for i in range(len(urlListList)):
			try:
				url = urlListList[i]
				requests.head(url)
				break
			except requests.exceptions.ConnectionError:
				printPar("error connecting to \"" + url + "\", trying next url.")
		#url = "https://www.owenrudge.net/GEM/downlist.txt"
		ListFile = open(fileListFile, "w")
		ListFile.write(requests.get(url).text)
		ListFile.close()
	ListFile = open(fileListFile, "r")
	List = ListFile.read()
	ListFile.close()
	List = List.splitlines()
	for i in range(len(List)):
		try:
			List[i] = List[i].strip()
			while List[i][0] == "#":
				List.pop(i)
			List[i] = List[i].split("<=1=>")
			List[i] += List[i].pop(1).split("<=2=>")
			List[i] += List[i].pop(2).split("<=3=>")
		except:
			pass
	return List

def printPar(string):
	strList = string.split()
	xPos = 0
	for i in range(len(strList)):
		if ((os.get_terminal_size()[0] - (xPos + len(strList[i]))) > 0):
			print(strList[i], end=" ")
			xPos += len(strList[i])
		else:
			print("")
			print(strList[i], end=" ")
			xPos = 0
			xPos += len(strList[i])
		xPos += 1
	print("")
			
def drawItem(item, compact=False):
	output = True
	if not(item[0] == " " or item[0] == ""):
		if not(item[1] == " " or item[1] == ""):
			if not((len(item[0]) + len(item[1]) + 2) > os.get_terminal_size()[0]):
				print(item[0], end=(" "))
				for i in range(os.get_terminal_size()[0] - (len(item[0]) + len(item[1]) + 2)):
					print("-", end="")
				print(" " + item[1])
			else:
				printPar(item[0])
				print(item[1])
		else:
			print(item[0])
	else:
		for i in range(os.get_terminal_size()[0]):
			print("-", end="")
		print("")
		output = False
	if not(compact):
		if not(item[2] == " " or item[2] == ""):
			printPar(item[2])
		if not(item[3] == " " or item[3] == ""):
			print(item[3], end="\n")
	return output

def navigate(item_num, options = ["Q"]):
	global FileList
	optionList = [["N","P","D","Q","C","R"],["ext", "rev","ownload","uit", "ompact","efresh"]]
	selection = ""
	print("\n" + escape + "F", end="")
	while not(selection in options):
		for i in range(len(options)):
			print("<" + options[i] + ">" + optionList[1][optionList[0].index(options[i])], end=" ")
		selection = input_key(": ").upper()[0]
		#selection = input(" : ").upper()
		print(escape + "F", end="")
		for i in range(os.get_terminal_size()[0]):
			print(" ",end='')
		print("\r", end="")
	if selection == "N" or selection == "": 
		return (item_num + 1)
	elif selection == "P":
		if FileList[item_num - 1][0] == "" or FileList[item_num - 1][0] == " ":
			return (item_num - 2)
		else:
			return (item_num - 1)
	elif selection == "D":
		try:
			downloadName = FileList[item_num][3].rsplit('/',1)[1]
			try:
				header = requests.head(FileList[item_num][3], allow_redirects=True)
				if header.status_code == 404:
					print("[Error 404: File Not Found]", end="\n\n")
					return item_num
			except:
				raise
			print("[Downloading]")
			download = requests.get(FileList[item_num][3])
			with open(downloadDir + downloadName, 'wb') as DLFile:
				DLFile.write(download.content)
			print("[File Downloaded]", end="\n\n")
		except:
			print("[Download Failed]", end="\n\n")
	elif selection == "C":
		global compact
		if compact:
			compact = False
		else:
			compact = True
	elif selection == "R":
		FileList = refresh(online=online)
		return 0
	elif selection == "Q":
		raise SystemExit(0)
	return item_num

print(escape + "2J")
if (os.get_terminal_size()[0] >= 60):
	print(" ███▀▀▀███    █████  ████████ ███     ██   █ ███████  ██      ")
	print("███     ███  ██   ██  █     █  ███   ██    █  █    ██  █      ")
	print(" ███   ███  ██      █ █ █      ███   ██   █   █     ██ █      ")
	print("  ██   ██   ██        ███      █ ██ █ █   █   █     ██ █      ")
	print("   ██ ██    ██    ███ █ █      █ ██ █ █   █   █     ██ █      ")
	print("    █ █      ██    █  █     █  █  ██  █  █    █    ██  █     █")
	print("     █        █████  ████████ ███    ███ █   ███████  ████████")
elif (os.get_terminal_size()[0] >= 40):
	print(" ███▀▀▀███    █████  ████████ ███     ██")
	print("███     ███  ██   ██  █     █  ███   ██ ")
	print(" ███   ███  ██      █ █ █      ███   ██ ")
	print("  ██   ██   ██        ███      █ ██ █ █ ")
	print("   ██ ██    ██    ███ █ █      █ ██ █ █ ")
	print("    █ █      ██    █  █     █  █  ██  █ ")
	print("     █        █████  ████████ ███    ███")
elif (os.get_terminal_size()[0] >= 12):
	print(" ███▀▀▀███ ")
	print("███     ███")
	print(" ███   ███ ")
	print("  ██   ██  ")
	print("   ██ ██   ")
	print("    █ █    ")
	print("     █     ")
	print("GEM/DL 2023")


FileList = refresh(online=online)

itemNum = 0
while 1 == 1:
	if drawItem(FileList[itemNum], compact):
		option = ["C","R","Q"]
		if FileList[itemNum][3] != "" and FileList[itemNum][3] != " ":
			option = ["D"] + option
		if itemNum != 0 and itemNum < (len(FileList) - 1):
			option = ["N","P"] + option
		elif itemNum == 0:
			option = ["N"] + option
		else:
			option = ["P"] + option
		itemNum = navigate(itemNum, options = option)
	else:
		itemNum += 1

'''
#Check all URLs
for i in range(len(FileList)):
	if FileList[i][3] != "" and FileList[i][3] != " ":
		try:
			header = requests.head(FileList[i][3])
			if not (header.status_code == 200 or header.status_code == 302):
				print(header.status_code, FileList[i][3])
		except requests.exceptions.ConnectionError:
			print("FAIL-1",FileList[i][3])
		except requests.exceptions.MissingSchema:
			print("FAIL-2",FileList[i][3])
		except Exception as e: print(e)
'''