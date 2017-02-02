try:
    import pkg_resources
    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r99")
except ImportError:
    pass

from dragonfly import *

release = Key("shift:up, ctrl:up, alt:up")

#Global mappings
global_rule = MappingRule(
    mapping = {
        #Chrome commands
        "new tab": Key("c-t"),
        "show links": Key("escape") + Key("f") + release,
    }
)

#Insert mode mappings
code_insert_mode_rule = MappingRule(
    mapping = {
        #Symbols
        "chuck": Text(";"),
        "quote": Key("quote"),
        "laip": Key("lparen"),
        "raip": Key("rparen"),
        "langle": Key("langle"),
        "rangle": Key("rangle"),
        "lack": Text("["),
        "rack": Text("]"),
        "lobe": Text("{"),
        "robe": Text("}"),
        "plus": Text(" + "),
        "dub plus": Text("++"),

        # "bean"
        #"monkey"
    },
    extras = [
        Dictation("text"),
        IntegerRef("n", 1, 30)
    ],
        defaults = {
        "n": 1
    }
)

#Ex mode mappings
code_ex_mode_rule = MappingRule(
    mapping = {
        #Commands
        "delete line": "dd",
        "delete [<n>] word": Text("%(n)ddw"),
        #Smbols
        # "quote": Key("quote"),
        # "laip": Key("lparen"),
        # "raip": Key("rparen"),
        # "langle": Key("langle"),
        # "rangle": Key("rangle"),
        # "lack": Text("["),
        # "rack": Text("]"),
        # "lobe": Text("{"),
        # "robe": Text("}"),
        # "plus": Text(" + "),
        # "dub plus": Text("++"),

        # # "bean"
        # #"monkey"
    },
    extras = [
        Dictation("text"),
        IntegerRef("n", 1, 30)
    ],
        defaults = {
        "n": 1
    }
)

#---------------------------------------------------------------------------
# Set up this module's configuration.

# This defines a configuration object with the name "code".
config            = Config("code")
config.cmd        = Section("Language section")


# This searches for a file with the same name as this file (code.py), but with
# the extension ".py" replaced by ".txt". In other words, it loads the
# configuration specified in the file code.txt
namespace = config.load()

#---------------------------------------------------------------------------
# Here we prepare the list of formatting functions from the config file.

# Retrieve text-formatting functions from this module's config file.
#  Each of these functions must have a name that starts with "format_".
format_functions = {}
if namespace:
    for name, function in namespace.items():
     if name.startswith("format_") and callable(function):
        spoken_form = function.__doc__.strip()

        # We wrap generation of the Function action in a function so
        #  that its *function* variable will be local.  Otherwise it
        #  would change during the next iteration of the namespace loop.
        def wrap_function(function):
            def _function(dictation):
                formatted_text = function(dictation)
                Text(formatted_text).execute()
            return Function(_function)

        action = wrap_function(function)
        format_functions[spoken_form] = action

# Here we define the text formatting rule.
# The contents of this rule were built up from the "format_*"
#  functions in this module's config file.
if format_functions:
    class FormatRule(MappingRule):
        mapping  = format_functions
        extras   = [Dictation("dictation")]
        
else:
    FormatRule = None

#Vim functionality
class ExMode(CompoundRule):
    spec = "ex buff"

    def _process_recognition(self, node, extras):
        Key("escape").execute()
        if InsertModeGrammar.enabled:
            InsertModeGrammar.disable()
        # print "Insert disabled"

class InsertMode(CompoundRule):
    spec = "insert"

    def _process_recognition(self, node, extras):
        Key("i").execute()
        if not InsertModeGrammar.enabled:
            InsertModeGrammar.enable()
        # print "Insert enabled"
        
#Load rules
grammar_context = AppContext(executable="code")

GlobalGrammar = Grammar("Global grammar", context = grammar_context)
GlobalGrammar.add_rule(global_rule)
if FormatRule:
    GlobalGrammar.add_rule(FormatRule())
GlobalGrammar.load()

ModeControllerGrammar = Grammar("Mode Controller", context = grammar_context)
ModeControllerGrammar.add_rule(InsertMode())
ModeControllerGrammar.add_rule(ExMode())
ModeControllerGrammar.load()

InsertModeGrammar = Grammar("Insert Mode", context = grammar_context)
InsertModeGrammar.add_rule(code_insert_mode_rule)
InsertModeGrammar.load()

ExModeGrammar = Grammar("Ex Mode", context = grammar_context)
ExModeGrammar.add_rule(code_ex_mode_rule)
ExModeGrammar.load()

def unload():
    global GlobalGrammar
    if GlobalGrammar: GlobalGrammar.unload()
    GlobalGrammar = None

    global InsertModeGrammar
    if InsertModeGrammar: InsertModeGrammar.unload()
    InsertModeGrammar = None

    global ModeControllerGrammar
    if ModeControllerGrammar: ModeControllerGrammar.unload()
    ModeControllerGrammar = None

    global ExModeGrammar
    if ExModeGrammar: ExModeGrammar.unload()
    ExModeGrammar = None
