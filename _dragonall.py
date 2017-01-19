from dragonfly import (Grammar, AppContext, MappingRule, Dictation, IntegerRef,
                       Key, Text)

grammar = Grammar("dragon")

dragon_rule = MappingRule(
	name = "dragon",
	mapping = {
		#Dragon
		"snore": Key("npdiv"),

		#Cursor Navigation
		"[<n>] slap": Key("enter:%(n)d"),
		"[<n>] tab": Key("tab:%(n)d"),
		"[<n>] bar": Key("backspace:%(n)d"),
		"[<n>] pill": Key("c-backspace:%(n)d"),
		"[<n>] milk": Key("c-left:%(n)d"),
		"[<n>] cheese": Key("c-right:%(n)d"),
		"queen": Key("end"),
		"king": Key("home"),
		"[<n>] up": Key("up:%(n)d"),
   		"[<n>] down": Key("down:%(n)d"),
    	"[<n>] left": Key("left:%(n)d"),
    	"[<n>] right": Key("right:%(n)d"),

		#Symbols
		"at": Text("@"),
		"slash": Key("slash"),
		"back up": Key("c-z"),

		#Accounts
		"Rangel": Text("frankjrangel"),
		"classical": Text("qlasico"),
	},
	extras = [
		Dictation("text"),
		IntegerRef("n", 1, 30),
	],
	defaults = {
		"n": 1
	}
)


grammar.add_rule(dragon_rule)
grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None

