try:
    import pkg_resources
    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r99")
except ImportError:
    pass

from dragonfly import *

grammar_context = AppContext(executable="idea")
grammar = Grammar("idea", context = grammar_context)

release = Key("shift:up, ctrl:up, alt:up")
idea_rule = MappingRule(
        name = "idea",
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

            #Editor commands
            "mess": Key("c-s"),

            #Ex mode
            "ex buff": Key("escape"),
            "bean": Key("i"),
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

&else:
    FormatRule = None

if FormatRule:
    grammar.add_rule(rule=FormatRule())

grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None