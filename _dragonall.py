from dragonfly import (Grammar, AppContext, MappingRule, Dictation, IntegerRef,
                       Key, Text)

grammar = Grammar("dragon")

release = Key("shift:up, ctrl:up, alt:up")
dragon_rule = MappingRule(
	name = "dragon",
	mapping = {
		#Dragon
		"snore": Key("npdiv"),

		#Windows
		"previous app [<n>]": Key("alt:down") + Key("tab:%(n)d") + release,
		"show apps": Key("alt:down") + Key("tab"),
		"select app": Key("enter") + release,
		"release keys": release,  

		#Cursor Navigation
		"slap [<n>]": Key("enter:%(n)d"),
		"tab [<n>]": Key("tab:%(n)d"),
		"bar [<n>]": Key("backspace:%(n)d"),
		"beer [<n>]": Key("del:%(n)d"),
		"pill|peel [<n>]": Key("c-backspace:%(n)d"),
		"milk [<n>]": Key("c-left:%(n)d"),
		"cheese [<n>]": Key("c-right:%(n)d"),
		"queen": Key("end"),
		"king": Key("home"),
		"up [<n>]": Key("up:%(n)d"),
   		"down [<n>]": Key("down:%(n)d"),
                "left [<n>]": Key("left:%(n)d"),
                "right [<n>]": Key("right:%(n)d"),

		#Symbols
		"attitude|Aruba": Text("@"),
		"slash": Key("slash"),
		"back up": Key("c-z"),

		#Accounts and such
		"Rangel": Text("frankjrangel"),
		"classical": Text("qlasico"),
		"some art": Text("tipearte"),
	},
	extras = [
		Dictation("text"),
		IntegerRef("n", 1, 100),
	],
	defaults = {
		"n": 1
	}
)

# TODO add formatting rules here instead of per program

grammar.add_rule(dragon_rule)
grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
