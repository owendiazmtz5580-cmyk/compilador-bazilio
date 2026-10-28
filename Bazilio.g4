grammar Bazilio;

programa : procedimiento+ EOF ;
 
procedimiento : PROC_ID VAR* bloque ;
 
bloque : INICIO instruccion* FIN ;
 
instruccion
   : VAR ASIGNA expr                       # Asignacion
   | LEE VAR                               # Lectura
   | ESCRIBE (TEXTO | expr)*               # Escritura
   | TOCA expr                             # Reproduccion
   | PROC_ID expr*                         # Invocacion
   | SI expr bloque (SINO bloque)?         # Condicional
   | MIENTRAS expr bloque                  # Iteracion
   | VAR AGREGA expr                       # Agregado
   | CORTA VAR '[' expr ']'                # Corte
   ;
 
/* Prioridades como en C: índice > longitud > * / % > + - > relacionales > = /= */
expr
   : expr '[' expr ']'                                         # Indice
   | LONG expr                                                 # Longitud
   | expr op=(POR | ENTRE | MODULO) expr                       # MulDiv
   | expr op=(MAS | MENOS) expr                                # SumaResta
   | expr op=(MENOR | MAYOR | MENORIGUAL | MAYORIGUAL) expr    # Relacional
   | expr op=(IGUAL | DISTINTO) expr                           # Igualdad
   | '(' expr ')'                                              # Parentesis
   | '{' expr* '}'                                             # Lista
   | ENTERO                                                    # Entero
   | NOTA                                                      # Nota
   | VAR                                                       # Variable
   ;
   
/* ---------- Símbolos ---------- */
INICIO : '|:' ;
FIN    : ':|' ;
ASIGNA : '<-' ;
LEE    : '<?>' ;
ESCRIBE: '<w>' ;
TOCA   : '(:)' | '<:>' ;      // el enunciado usa las dos escrituras
AGREGA : '<<' ;
CORTA  : '8<' ;
LONG   : '#' ;
 
MAS : '+' ;  MENOS : '-' ;  POR : '*' ;  ENTRE : '/' ;  MODULO : '%' ;
IGUAL : '=' ;  DISTINTO : '/=' ;
MENOR : '<' ;  MAYOR : '>' ;  MENORIGUAL : '<=' ;  MAYORIGUAL : '>=' ;
 
/* ---------- Palabras reservadas (antes que VAR) ---------- */
SI      : 'if' ;
SINO    : 'else' ;
MIENTRAS: 'while' ;
 
/* ---------- Valores e identificadores ---------- */
// comillas rectas o tipográficas
TEXTO   : '"' ~["\r\n]* '"' | '\u201C' ~[\u201D\r\n]* '\u201D' ;
ENTERO  : [0-9]+ ;
NOTA    : [A-G] [0-8]? ;                  // se valida el rango (A0..C8) al ejecutar
PROC_ID : [A-Z] [a-zA-Z0-9_]* ;           // procedimientos: empiezan con mayúscula
VAR     : [a-z] [a-zA-Z0-9_]* ;           // variables: empiezan con minúscula
 
COMENTARIO : ( '###' .*? '###' | '~~~' .*? '~~~' ) -> skip ;
ESPACIOS   : [ \t\r\n]+ -> skip ;