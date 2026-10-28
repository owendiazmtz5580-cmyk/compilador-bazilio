import sys
 
from antlr4 import CommonTokenStream, FileStream
from antlr4.error.ErrorListener import ErrorListener
 
from BazilioLexer import BazilioLexer
from BazilioParser import BazilioParser
from BazilioVisitor import BazilioVisitor
 
 
class ErrorBazilio(Exception):
   """Error de sintaxis o de ejecución de un programa Bazilio."""
 
 
class _ListenerErrores(ErrorListener):
   def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
       raise ErrorBazilio(
           f"Error de sintaxis en la línea {line}, columna {column}: {msg}")
 
 
def parsear(flujo):
   lexer = BazilioLexer(flujo)
   lexer.removeErrorListeners()
   lexer.addErrorListener(_ListenerErrores())
   parser = BazilioParser(CommonTokenStream(lexer))
   parser.removeErrorListeners()
   parser.addErrorListener(_ListenerErrores())
   return parser.programa()
 
 
def nombre_token(lexer, tipo, texto):
   nombre = lexer.ruleNames[tipo - 1]
   # los símbolos sueltos ( [ ] { } ...) se muestran tal cual
   return texto if nombre.startswith("T__") else nombre
 
 
def listar_tokens(flujo):
   lexer = BazilioLexer(flujo)
   lexer.removeErrorListeners()
   lexer.addErrorListener(_ListenerErrores())
   tokens = CommonTokenStream(lexer)
   tokens.fill()
   return [(nombre_token(lexer, t.type, t.text), t.text)
           for t in tokens.tokens if t.type != -1]
 
 
def principal(argv):
   modo = "--revisar"
   if "--tokens" in argv:
       modo = "--tokens"
   elif "--arbol" in argv:
       modo = "--arbol"
   archivos = [a for a in argv[1:] if not a.startswith("--")]
   if not archivos:
       print("Uso: python3 analizar.py [--tokens | --arbol] programa.bzl "
             "[otro.bzl ...]")
       return 2
   estado = 0
   for ruta in archivos:
       try:
           if modo == "--tokens":
               for tipo, texto in listar_tokens(FileStream(ruta, encoding="utf-8")):
                   print(f"{tipo:<10} {texto}")
           elif modo == "--arbol":
               arbol = parsear(FileStream(ruta, encoding="utf-8"))
               print(arbol.toStringTree(ruleNames=BazilioParser.ruleNames))
           else:
               parsear(FileStream(ruta, encoding="utf-8"))
               print(f"{ruta}: sintaxis correcta")
       except ErrorBazilio as e:
           print(f"{ruta}: {e}")
           estado = 1
   return estado
 
 
if __name__ == "__main__":
   sys.exit(principal(sys.argv))