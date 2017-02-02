from dragonfly import (Grammar, AppContext, MappingRule, Dictation, IntegerRef, Key, Text)

grammar_context = AppContext(executable="powershell")
grammar = Grammar("bash", context = grammar_context)

bash_rule = MappingRule(
        name = "bash",
        mapping = {
            #Navigation
            "change directory": Text("cd "),
            "change directory to <text>": Text("cd %(text)s"),
            "go up": Text("cd ../") + Key("enter"),
            "show": Text("ls") + Key("enter"),

            #General CLI commands
            "make directory": Text("mkdir "),
            "move": Text("mv"),

            #Git
            "initialize git": Text("git init") + Key("enter"),
            "git status": Text("git status") + Key("enter"),
            "git commit": Text('git commit -m ""') + Key("left"),
            "git commit <text>": Text('git commit -m "%(text)s"'),
            "git clone": Text("git clone "),
            "git add all": Text("git add .") + Key("enter"),
            "git push": Text("git push "),
            
            #Repositories
            "laradock repository": Text("https://github.com/laradock/laradock.git"),
            
            #Composer
            "compose Laravel": Text("composer create-project --prefer-dist laravel/laravel "),

            #Docker
            "laradock start": Text("docker-compose up -d nginx mysql phpmyadmin"),
            "laradock bash": Text("docker exec -it --user=laradock laradock_workspace_1 bash") + Key("enter"),
            "docker start": Text("docker-compose up -d"),
            "docker stop": Text("docker-compose stop"),
            "exit container": Key("control:down") + Key("p") + Key("q") + Key("control:up"),
        },
        extras = [
            Dictation("text"),
            IntegerRef("n", 1, 30)
        ],
        defaults = {
            "n": 1
        }
    )
   
grammar.add_rule(bash_rule)
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
