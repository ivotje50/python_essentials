import sys
import re
import StringIO
import contextlib
import importlib
import imp
import exception as excep

@contextlib.contextmanager
def _stdoutIO(stdout=None):
	old = sys.stdout
	if stdout is None:
		stdout = StringIO.StringIO()
	sys.stdout = stdout
	yield stdout
	sys.stdout = old

def getFunction(functionName, fileName):
	return getattr(module(fileName), functionName)
	
def outputOf(fileName):
	return outputOfSource(fileName, source(fileName))

def outputOfSource(fileName, source):
	exception = None

	_, output = moduleAndOutputFromSource(fileName, source)
	if exception:
		raise exception
	
	return output

def source(fileName):
	source = ""
	with open(fileName) as f:
		source = f.read()
	return source

def sourceOfDefinitions(fileName):
	newSource = ""
	with open(fileName) as f:
		insideDefinition = False
		for line in f.readlines():
			if not line.strip():
				continue

			if (line.startswith(" ") or line.startswith("\t")) and insideDefinition:
				newSource += line
			elif line.startswith("def ") or line.startswith("class "):
				newSource += line
				insideDefinition = True
			elif line.startswith("import ") or line.startswith("from "):
				newSource += line
			else:
				insideDefinition = False

	return newSource

def module(fileName):
	mod, _ = moduleAndOutputFromSource(fileName, sourceOfDefinitions(fileName))
	return mod

def moduleAndOutputFromSource(fileName, source, memo= {}):
	if (fileName, source) in memo:
		return memo[(fileName, source)]

	mod = None
	output = ""
	exception = None
	with _stdoutIO() as s:
		moduleName = fileName[:-3] if fileName.endswith(".py") else fileName
		try:
			mod = imp.new_module(moduleName)
			exec source in mod.__dict__
			sys.modules[moduleName] = mod

		except Exception as e:
			exception = excep.SourceException(e, "while trying to import the code")

		for name, func in [(name, f) for name, f in mod.__dict__.iteritems() if callable(f)]:
			if func.__module__ == moduleName:
				setattr(mod, name, wrapFunctionWithExceptionHandler(func))
		output = s.getvalue()
	if exception:
		raise exception

	memo[(fileName, source)] = (mod, output)
	return memo[(fileName, source)]

def neutralizeFunction(mod, functionName):
	if hasattr(mod, functionName):
		def dummy(*args, **kwargs):
			pass
		setattr(getattr(mod, functionName), "__code__", dummy.__code__)

def neutralizeFunctionFromImport(mod, functionName, importedModuleName):
	for attr in [getattr(mod, name) for name in dir(mod)]:
		if getattr(attr, "__name__", None) == importedModuleName:
			neutralizeFunction(attr, functionName)
		if getattr(attr, "__name__", None) == functionName and getattr(attr, "__module__", None) == importedModuleName:
			neutralizeFunction(mod, functionName)
	
def wrapFunctionWithExceptionHandler(func):
	def exceptionWrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except Exception as e:
			argListRepr = reduce(lambda xs, x : xs + ", " + x, ["%s=%s" %(func.__code__.co_varnames[i], args[i]) for i in range(len(args))])
			for kwargName in func.__code__.co_varnames[len(args):func.func_code.co_argcount]:
				argListRepr += ", %s=%s" %(kwargName, kwargs[kwargName])
			raise excep.SourceException(e, "while trying to execute the function %s with arguments \"%s\"" %(func.__name__, argListRepr))
	return exceptionWrapper

def removeWhiteSpace(s):
	return re.sub(r"\s+", "", s, flags=re.UNICODE)

def getPositiveIntegersFromString(s):
	return [int(i) for i in re.findall(r"\d+", s)]
