from sys import *
import os
import shutil

tokens = []
varname = ""
var = ""
completepath = ""
path = os.getcwd()
shutil.rmtree(path + "\\vars", ignore_errors=False, onerror=None)
os.mkdir(path + "\\vars\\")
def open_file(filename):
	data = ""
	data += "\n"
	data = open(filename + ".lang", "r").read()
	data += "<EOF>"
	return data
def lex(filecontents):
	state = 0
	cmdstate = 0
	wsastate = 0
	varstate = 0
	varnamestarted = 0
	dubquoteforvardatastarted = 0
	varname = ""
	completepath = ""
	var = ""
	command = ""
	tok = ""
	string = ""
	expr = ""
	n = ""
	attack = ""
	isexpr = 0
	unexpectedtok = ""
	filecontents = list(filecontents)
	for char in filecontents:
		tok += char
		if tok == "<EOF>":
			tokens.append("EOF")
			tok = ""
		if tok == " ":
			if cmdstate == 0 and wsastate == 0 and state == 0 and varstate == 0:
				if state == 0:
					tok = ""
				elif state == 1:
					tok = " "
				elif cmdstate == 0:
					tok = ""
				elif cmdstate == 1:
					tok = " "
				elif wsastate == 0:
					tok = ""
				elif wsastate == 1:
					tok = " "
				else:
					tokens.append(unexpectedtok)
		if tok == "\n" or tok == "<EOF>":
			if expr != "" and isexpr == 1:
				tokens.append("EXPR:" + expr)
				expr = ""
			elif expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			else:
				tokens.append(unexpectedtok)
			tok = ""
		elif tok == "CMD" or tok == "cmd":
			tokens.append("COMMAND")
			cmdstate = 1
			tok = ""
			command = ""
		elif tok == "PRINT" or tok == "print":
			tokens.append("PRINT")
			tok = ""
		elif tok == "VAR" or tok == "var":
			tokens.append("VAR")
			varnamestarted = 1
			tok = ""
		elif tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9":
			if state == 0 and cmdstate == 0 and varstate == 0 and wsastate == 0:
				expr += tok
				tok = ""
		elif tok == "+" or tok == "-" or tok == "*" or tok == "/":
			isexpr = 1
			expr += tok
			tok = ""
		elif tok == "\"":
			if state == 0:
				state = 1
				tok = ""
			elif state == 1:
				tokens.append("STRING:" + string + "\"")
				var = string
				string = ""
				state = 0
				tok = ""
			if dubquoteforvardatastarted == 1:
				dubquoteforvardatastarted = 0
			if varnamestarted == 1:
				varstate = 1
				varnamestarted = 0
				dubquoteforvardatastarted = 1
			if varstate == 1 and dubquoteforvardatastarted == 1:
				varstate = 0
				tokens.append("VARNAME:" + varname)
				varname = ""
		elif tok == ")":
			if cmdstate == 1:
				cmdstate = 0
				tokens.append("CMD:" + command + ")")
			tok = ""
		elif tok == "(":
			if cmdstate == 1 or wsastate == 1 or state == 1:
				tok = "("
		elif tok == "=":
			tokens.append("EQL")
			tok = ""
		elif state == 1:
			string += tok
			tok = ""
			state = 1
		elif cmdstate == 1:
			command += tok
			tok = ""
			cmdstate = 1
		elif wsastate == 1:
			attack += tok
			tok = ""
		elif varstate == 1:
			var += tok
			tok = ""
		elif varnamestarted == 1:
			varname += tok
			tok = ""
		unexpectedtok += tok
		tok = ""
	#print (expr)
	print(tokens)
	return tokens
def runCommand(commandforparse):
	os.system('cmd /c ' + commandforparse)
	f.write(wsaforparse)
def makeVar(varname, var):
	completepath = path + "\\" + "vars\\" + varname + ".txt"
	f = open(completepath, "w")
	f.write(var)
	var = ""
	varname = ""
def setVar(varname, var):
	completepath = path + "\\" + "vars\\" + varname + ".txt"
	f = open(completepath, "w")
	f.write("")
	f = open(completepath, "w")
	f.write(var)
	var = ""
	varname = ""
def parse(toks):
	i = 0
	while (i < len(toks)):
		if toks [i] == "EOF":
			print ("done!")
		elif toks [i+1][0:3] == "CMD":
			commandforparse = toks[i+1][6:-1]
			print(commandforparse)
			runCommand(commandforparse)
			i += 2
		elif toks [i] == "VAR":
			varname = toks [i+3][8:]
			print (varname)
			var = toks [i+4][7:-1]
			print (var)
			makeVar(varname, var)
			i += 1
		elif toks [i] == "EQL":
			varname = ""
			if toks [i+2][0:6] == "STRING":
				varname = toks[i+1][8:]
				var = toks [i+2][7:-1]
				setVar(varname, var)
				varname = ""
			i += 1
		elif toks[i+1][0:6] == "STRING":
			if toks [i][:5] == "PRINT":
				print (toks[i+1][7:] [:-1])
			i += 2
		elif toks [i+1][0:3] == "NUM":
			print(toks[i+1][4:])
			i += 2
		elif toks [i+1][0:4] == "EXPR":
			print(toks[i+1][5:])
			i += 2
		elif toks [i][:5] == "PRINT":
			varname = toks
			varname = ""
			i += 1
		else:
			if toks[i][:5] != "PRINT":
				if toks[i-1] == "PRINT":
					for filename in os.listdir(path + "//vars/"):
						print("PLEAS JUST WORK")
						continue
			i += 1
def run():
	data = open_file(argv[1])
	toks = lex(data)
	parse(toks)
run()