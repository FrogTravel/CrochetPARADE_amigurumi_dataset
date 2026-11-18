#!/usr/bin/env python3
"""Build parser.mjs (an ES module usable from Node) from CrochetPARADE's browser script parse64.js.

usage: python3 make_parser.py /path/to/CrochetPARADE/parse64.js parser.mjs

Two changes are made to the upstream text:
  1. it is wrapped in `export function createParser(console, alert) { ... return {final, export_to_dot}; }`
  (plus declarations for three variables the browser script leaves as implicit globals)
  2. evaluateExpression() only evaluates plain arithmetic (digits, + - * / % ( ) .), so that
     pattern text from an untrusted dataset cannot run arbitrary JavaScript.
CrochetPARADE is GPLv3 (Copyright Svetlin Tassev); the generated file inherits that license.
"""
import sys
src=open(sys.argv[1]).read()
old="return Function(`'use strict'; return ${expression}`)();"
if old not in src: sys.exit('evaluateExpression body not found; upstream changed')
new=("const text = String(expression).trim();\n"
     "    if (!/^[0-9+\\-*\\/%().\\seE]+$/.test(text)) throw new Error('Arithmetic-only evaluator refuses expression: '+text.slice(0,80));\n"
     "    return Function(`'use strict'; return ${text}`)();")
src=src.replace(old,new)
head="// Generated from CrochetPARADE parse64.js by make_parser.py (GPLv3, Copyright (C) Svetlin Tassev).\nexport function createParser(console, alert) {\nvar Nrows, LIST, otherNodes, connections, Stitches, k;\nvar isp, i0, i1; // implicit globals in the browser script; ES modules are strict\n"
open(sys.argv[2],'w').write(head+src+"\nreturn {final, export_to_dot};\n}\n")
