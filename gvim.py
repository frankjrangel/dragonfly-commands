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
        #Global commands
        "mess": Key("escape") + Text(":w") + Key("enter") + release,
    }
)

#Insert mode mappings
gvim_insert_mode_rule = MappingRule(
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
        "equals": Text(" = "),
        "minus": Text("-"),
        "percent": Key("percent"),
        "Aruba": Text("@"),

        #Editor commands
        "back": Key("escape") + Key("u") + Key("i"),#Key("c-u"), TODO
        "pill": Key("c-backspace"),

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

#Normal mode mappings
gvim_normal_mode_rule = MappingRule(
    mapping = {
        "delete line": Text("dd"),
        "late word": Key("d, w"),
        "give me line": Key("d:2, k, p:2"),
        "back":Key("u"),
        "line [<n>]": Text(":%(n)d") + Key("enter"),

        #Visual Mode
        "visual": Key("v"),
        "visual line": Key("s-v"),
        "visual block": Key("c-v"),

        #Splits and tabs
        "window left": Key("c-w,h"),
        "window right": Key("c-w,l"),
        "window up": Key("c-w,k"),
        "window down": Key("c-w,j"),
        "window split": Key("c-w,s"),
        "window cycle": Key("c-w,c-w"),
        "window vertical split": Key("c-w,v"),

        
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
class ExModeCommands(CompoundRule):
    spec = "execute <command>"

    extras = [
        Choice("command", {
            "quit": Text("q"),
            "save and quit": Text("wq"),
        })
    ]

gvim_ex_mode_rule = MappingRule(
    mapping = {
        #Commands
        

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

#Plugin Mappings

#Nerdtree
class NerdTreeRule(CompoundRule):
    spec = "nerd <command>"

    extras = [
        Choice("command", {
            "tree": Text(":NERDTreeToggle") + Key("enter"),
            "open": Key("o"),
            "make root": Key("C"),
        })
    ]

    def _process_recognition(self, node, extras):
        Key("escape").execute()
        extras["command"].execute()

#Language specifics

#Blade template engine

#Normal mode compound rules
class IndentRule(CompoundRule):
    spec = "[<n>] indent [<m>] <direction>"
    
    extras = [
        Choice("direction", {
            "left": "langle",
            "right": "rangle"
        }),
        IntegerRef("n", 1, 30),
        IntegerRef("m", 1, 30),
    ]
    
    defaults = {
        "n": 1,
        "m": 1,
    }

    def _process_recognition(self, node, extras):
        direction = extras["direction"]
        times = extras["m"]
        Key("shift").execute()
        while times > 0:
            if extras["n"] > 1:
                Text(str(extras["n"])).execute()
            Key(direction + ":2").execute()
            times -= 1
        release.execute()

#End -- Normal mode compound rules -- End

#Vim functionality
class NormalMode(CompoundRule):
    spec = "ex buff"

    def _process_recognition(self, node, extras):
        Key("escape").execute()
        if InsertModeGrammar.enabled:
            InsertModeGrammar.disable()
        if not NormalModeGrammar.enabled:
            NormalModeGrammar.enable()

class InsertMode(CompoundRule):
    spec = "<command>"
    
    extras = [
        Choice("command", {
            "insert": "i",
            "insert end": "A",
            "insert beg": "I",
            "insert line": "o",
            "insert delete": "C",
            "insert delete line": "S",
            "insert delete word": "c,w",
            "insert delete space": "c,e",
            "insert delete paragraph": "c,a,p",
        })
    ]

    def _process_recognition(self, node, extras):
        for string in extras["command"].split(','):
            key = Key(string)
            key.execute()
        if not InsertModeGrammar.enabled:
            InsertModeGrammar.enable()
        if NormalModeGrammar.enabled:
            NormalModeGrammar.disable()

#---------------------------------------------------------------------------
# Set up this module's configuration.

# This defines a configuration object with the name "gvim".
config            = Config("gvim")
config.cmd        = Section("Language section")


# This searches for a file with the same name as this file (gvim.py), but with
# the extension ".py" replaced by ".txt". In other words, it loads the
# configuration specified in the file gvim.txt
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
        
#Load rules
grammar_context = AppContext(executable="gvim")

GlobalGrammar = Grammar("Global grammar", context = grammar_context)
GlobalGrammar.add_rule(global_rule)
if FormatRule:
    GlobalGrammar.add_rule(FormatRule())
GlobalGrammar.add_rule(NerdTreeRule())
GlobalGrammar.load()

ModeControllerGrammar = Grammar("Mode Controller", context = grammar_context)
ModeControllerGrammar.add_rule(InsertMode())
ModeControllerGrammar.add_rule(NormalMode())
ModeControllerGrammar.load()

InsertModeGrammar = Grammar("Insert Mode", context = grammar_context)
InsertModeGrammar.add_rule(gvim_insert_mode_rule)
InsertModeGrammar.load()

NormalModeGrammar = Grammar("Normal Mode", context = grammar_context)
NormalModeGrammar.add_rule(gvim_normal_mode_rule)
NormalModeGrammar.add_rule(IndentRule())
NormalModeGrammar.load()

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

    global NormalModeGrammar
    if NormalModeGrammar: NormalModeGrammar.unload()
    NormalModeGrammar = None
