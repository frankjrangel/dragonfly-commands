try:
    import pkg_resources
    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r99")
except ImportError:
    pass

from dragonfly import *

release = Key("shift:up, ctrl:up, alt:up")

ide_commands_mappings = MappingRule(
    mapping = {
        #IDE commands
        "override method": Key("c-o"),
    }
)

idea_rule = MappingRule(
    name = "idea",
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
        "mess": Key("c-s"),

        #Ex mode
        "ex buff": Key("escape"),
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
idea_normal_mode_rule = MappingRule(
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




grammar.add_rule(idea_rule)

#---------------------------------------------------------------------------
# Set up this module's configuration.

# This defines a configuration object with the name "idea".
config            = Config("idea")
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

# Load rules
grammar_context = AppContext(executable="idea")

GlobalGrammar = Grammar("Global grammar", context = grammar_context)

if FormatRule:
    grammar.add_rule(rule=FormatRule())

grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
