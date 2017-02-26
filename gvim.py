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
        "reload vim": Key("escape") + Text(":so $MYVIMRC") + Key("enter") + release,
        "go to file": Key("c-p"),
    }
)

#Insert mode mappings
gvim_insert_mode_rule = MappingRule(
    mapping = {
        #Symbols
        "chuck": Text(";"),
        "laip [<n>]": Key("lparen:%(n)d"),
        "raip [<n>]": Key("rparen:%(n)d"),
        "langle [<n>]": Key("langle:%(n)d"),
        "rangle [<n>]": Key("rangle:%(n)d"),
        "lack [<n>]": Key("lbracket:%(n)d"),
        "rack [<n>]": Key("rbracket:%(n)d"),
        "lobe [<n>]": Key("lbrace:%(n)d"),
        "robe [<n>]": Key("rbrace:%(n)d"),
        "mass": Text("+"),
        "plus": Text(" + "),
        "dub plus": Text("++"),
        "equal [<n>]": Key("equal:%(n)d"),
        "equals": Text(" = "),
        "and if [<n>]": Key("ampersand:%(n)d"),
        "percent": Key("percent"),
        "boom": Text("!"),
        "match": Text("$"),
        "arrow": Text("->"),
        "backslash": Key("backslash"),
        "quotes": Key("dquote"),
        "quote": Key("squote"),
        "minus": Text("-"),
        "underscore": Key("underscore"),
        "pound": Key('hash'),
        
        #Editor commands
        "back": Key("escape") + Key("u") + Key("i"),#Key("c-u"), TODO

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
        #Commands
        "delete line": Text("dd"),
        "late word": Key("d, w"),
        "give me line": Key("y:2, p:2"),
        "back":Key("u"),
        "line [<n>]": Text(":%(n)d") + Key("enter"),
        "yank": Key("y"),
        "yank line": Key("y, y"),
        "paste": Key("p"),
        "take me back": Key("c-o"),
        "center line": Key("z, z"),

        #Visual Mode
        "visual": Key("v"),
        "visual line": Key("s-v"),
        "visual block": Key("c-v"),

        #Splits and tabs
        "window left": Key("c-w,h"),
        "window right": Key("c-w,l"),
        "window up": Key("c-w,k"),
        "window down": Key("c-w,j"),
        "window split": Key("c-w,v"),
        "window cycle": Key("c-w,c-w"),
        "window horizontal split": Key("c-w,s"),
        "window only": Key("escape") + Text(":only") + Key("enter"),
        
    },
    extras = [
        Dictation("text"),
        IntegerRef("n", 1, 1000)
    ],
        defaults = {
        "n": 1
    }
)

#Ex mode mappings
class ExModeCommands(CompoundRule):
    spec = "execute [<command>]"

    extras = [
        Choice("command", {
            "quit": Text("q"),
            "save": Text("w"), 
            "save and quit": Text("wq"),
        })
    ]

    defaults = {
        "command": "c"
    }

    def _process_recognition(self, node, extras):
        Key("escape").execute()
        Text(":").execute()
        if extras["command"] != "c":
            extras["command"].execute()

#Plugin Mappings

#Nerdtree
class NerdTreeRule(CompoundRule):
    spec = "nerd <command>"

    extras = [
        Choice("command", {
            "tree": Text(":NERDTreeToggle") + Key("enter"),
            "open": Key("o"),
            "make root": Key("C"),
            "reload": Key("R"),
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
    spec = "insert [<command>]"
    
    extras = [
        Choice("command", {
            "i": "i",
            "end": "A",
            "beg": "I",
            "line": "o",
            "delete": "C",
            "delete line": "S",
            "delete word": "c,w",
            "delete space": "c,e",
            "delete paragraph": "c,a,p",
        })
    ]

    defaults = {
        "command": "i",
    }

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
NormalModeGrammar.add_rule(ExModeCommands())
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
