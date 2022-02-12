

from re import compile
from os import path, makedirs
from loguru import logger
from json import loads, dumps, decoder
import sys


# fix broken pipe
from signal import signal, SIGPIPE, SIG_DFL  
signal(SIGPIPE,SIG_DFL)

class Tools(object):

    def __init__(self, tool_loc: str = None):
        """
        Inits the object, with a check if tool_loc is defined
        """
        assert tool_loc is not None

        self.tool_loc = tool_loc

    def create_load_tools(self,):
        """
        Creates the dirs and the file to store the database

        populates the "tool" var with the json object
        """
        if not path.exists(self.tool_loc):
            # create dirs
            makedirs("/".join(list(path.split(self.tool_loc))[:-1]), exist_ok=True)
            # create tool file
            with open(self.tool_loc, "w+") as f:
                pass
        with open(self.tool_loc, "r") as f:
            try:
                content =  loads(f.read())
            except decoder.JSONDecodeError:
                content = dict()
            finally:
                self.tools = content
                self.tools.setdefault("tools", list())
                self.tools.setdefault("hacks", list())
    
    def write_tools(self,):
        """
        Writes the tool set into the backup file
        """
        with open(self.tool_loc, "w+") as f:
            try:
                f.write(dumps(self.tools, indent=4))
            except Exception as e:
                logger.error(f"Error writting tools to {self.tool_loc} because: {e}")
                exit()
    
    def add_tool(self, tool_name:str=None, description: str=None, link: str=None):
        """
        Adds a tool to the toolbox
        """
        # make sure we have the right structure for new databases

        if tool_name is None:
            logger.error("You need to specify a name for the tool !")
            return

        self.tools.setdefault("tools", list())

        if tool_name in [x["name"] for x in self.tools["tools"]]:
            logger.warning(f"Tool {tool_name} already exists, skipping")
            return
        
        structure = {
            "name": tool_name,
            "description": description or "",
            "link": link or ""
        }

        self.tools["tools"].append(structure)
    
    def del_tool(self, tool_name:str=None):
        """
        Dels a tool from the toolbox
        """
        # make sure we have the right structure for new databases

        if tool_name is None:
            logger.error("You need to specify a name for the tool !")
            return

        self.tools.setdefault("tools", list())

        if not tool_name in [x["name"] for x in self.tools["tools"]]:
            logger.warning(f"Tool '{tool_name}' does not exists, skipping")
            return
        index = [x for x in range(len(self.tools["tools"])) if self.tools["tools"][x]["name"] == tool_name][0]
        
        del self.tools["tools"][index]
    
    def print_tool(self, tool):
        """
        Takes a json defining a tool and prints it to the screen
        """
        print(f"""{tool["name"]}\t|\t{tool["description"]}\t|\t{tool["link"]}""")
    
    def print_hack(self, hack):
        """
        Takes a json defining a hack and prints it to the screen
        """
        print(f"""{hack["method_name"]}\t|\t{hack["method"]}""")

    def search_tool(self, args):
        """
        Takes a string and regex searches the database
        """
        found_names = set()
        if len(args) == 1:
            pieces = args[0].split(",")
            for index in range(len(pieces)):
                string = pieces[index]
                for tool in self.tools["tools"]:
                    regex = compile(f".*{string}.*")
                    if any([
                            regex.match(tool["name"]),
                            regex.match(tool["description"]),
                            regex.match(tool["link"]),
                        ]):
                        for elms in pieces[index-1:]:
                            regex_ = compile(f".*{elms}.*")
                            if not any([
                                    regex_.match(tool["name"]),
                                    regex_.match(tool["description"]),
                                    regex_.match(tool["link"]),
                                ]): 
                                break
                            if not tool["name"] in found_names:
                                found_names.add(tool["name"])
                                self.print_tool(tool)
        else:
            string = " ".join(args)
            for tool in self.tools["tools"]:
                regex = compile(f".*{string}.*")
                if any([
                        regex.match(tool["name"]),
                        regex.match(tool["description"]),
                        regex.match(tool["link"]),
                    ]):
                    self.print_tool(tool)

    def search_hack(self, args):
        """
        Takes a string and regex searches the database
        """
        found_names = set()
        
        string = " ".join(args)
        for hack in self.tools["hacks"]:
            hack_name, content = hack.items()
            regex = compile(f".*{string}.*")
            if regex.match(hack_name):
                for elements in content:
                    self.print_hack(elements)

                
    def add_hack(self, hack_name:str=None):
        """
        Adds a hack to the toolbox
        """
        # make sure we have the right structure for new databases
        self.tools.setdefault("hacks", list())

        structure = {
            hack_name: [

            ]
        }

        self.tools["hacks"].append(structure)
    
    def del_hack(self, hack_name:str=None):
        """
        Dels a hack from the toolbox
        """
        # make sure we have the right structure for new databases

        if hack_name is None:
            logger.error("You need to specify a name for the hack !")
            return

        self.tools.setdefault("hacks", list())
        if not hack_name in [list(x.keys())[0] for x in self.tools["hacks"]]:
            logger.warning(f"Hack '{hack_name}' does not exists, skipping")
            return
        index = [x for x in range(len(self.tools["hacks"])) if list(self.tools["hacks"][x].keys())[0] == hack_name][0]
        
        del self.tools["hacks"][index]
    
    def del_hack_method(self, hack_name:str=None, method_name: str=None):
        """
        Dels a hack method from the toolbox
        """
        # make sure we have the right structure for new databases

        if hack_name is None:
            logger.error("You need to specify a name for the hack !")
            return
        
        if method_name is None:
            logger.error("You need to specify a method for the hack !")
            return

        self.tools.setdefault("hacks", list())

        if not hack_name in [x for x in self.tools["hacks"]]:
            logger.warning(f"Hack '{hack_name}' does not exists, skipping")
            return
        
        index_hack = [x for x in range(len(self.tools["hacks"])) if self.tools["hacks"][x] == hack_name][0]
        
        content = [x for x in self.tools["hacks"][index_hack]][0]

        if not method_name in [c["method_name"] for c in content]:
            logger.warning(f"Could not find method {method_name} in {hack_name}")
            return

        index_method = [x for x in range(len(self.tools["hacks"][index_hack])) if self.tools["hacks"][index_hack][x]["method_name"] == method_name][0]

        del self.tools["hacks"][index_hack][index_method]
    
    def add_hack_method(self, hack_name:str=None, method:str=None, content:str=None):
        """
        Adds a hackmethod to a hack
        """
        index_hack = [x for x in range(len(self.tools["hacks"]))  if list(self.tools["hacks"][x].keys())[0] == hack_name]
        if not index_hack:
            index_hack = len(self.tools["hacks"])
            self.tools["hacks"].append(dict())
            self.tools["hacks"][index_hack].setdefault(hack_name, list())
        else:
            index_hack = index_hack[0]
        
        for method_index in range(len(self.tools["hacks"][index_hack][hack_name])):
            method_content = self.tools["hacks"][index_hack][hack_name][method_index]
            if method_content["method_name"] == method:
                self.tools["hacks"][index_hack][hack_name][method_index]["method"] = content
                return
                
        self.tools["hacks"][index_hack][hack_name].append(
            {
                "method_name": method,
                "method": content
            }
        )

def args_tools():
    if len(sys.argv) <= 2:
        for tool in tools.tools["tools"]:
            tools.print_tool(tool)
    elif len(sys.argv) <= 3:
        tool_name = sys.argv[2]
        if not tool_name in [x["name"] for x in tools.tools["tools"]]:
            logger.debug("Your tool does not exists :( I'm gonna create it !")
            tools.add_tool(sys.argv[2])
        tools.search_tool(sys.argv[2])
    else:
        if sys.argv[2] == "add":
            tools.add_tool(*sys.argv[3:])
        elif sys.argv[2] == "search":
            tools.search_tool(sys.argv[3:])
        elif sys.argv[2] == "del":
            tools.del_tool(sys.argv[3])
        else:
            tool_name = sys.argv[2]
            if not tool_name in [x["name"] for x in tools.tools["tools"]]:
                logger.debug("Your tool does not exists :( I'm gonna create it !")
                tools.add_tool(sys.argv[2])
            
            mode = sys.argv[3]

            if mode.lower().startswith("d"):
                mode = "description"
            elif mode.lower().startswith("l"):
                mode = "link"
            else:
                mode = None

            if len(sys.argv) <= 4:
                # dumping content of requested tool's field
                content = {"name":"", "description": "", "link": ""}
                for x in tools.tools["tools"]:
                    if x["name"] == tool_name:
                        content = x
                if mode is not None:
                    print(content[mode])
                else:
                    tools.print_tool(content)
            else:
                # adding content to the tool
                tool_index =  [x for x in range(len(tools.tools["tools"])) if tools.tools["tools"][x]["name"] == tool_name][0]
                if len(sys.argv) == 5:
                    content = "".join(sys.argv[4])
                else:
                    content = " ".join(sys.argv[4:])

                tools.tools["tools"][tool_index][mode] = content

def args_hacks():
    if len(sys.argv) <= 2:
        for elm in tools.tools["hacks"]:
            hack_name, content = list(elm.items())[0]
            print(hack_name)
            for element in content:
                tools.print_hack(element)
    else:
        if sys.argv[2] == "add":
            hack_name = str()
            found = False
            args_index = 3
            for arg in sys.argv[3:]:
                hack_name += arg
                args_index += 1
                if hack_name in [list(x.keys())[0] for x in tools.tools["hacks"]]:
                    found = True
                    break
                
                hack_name += " "
            if found:
                if len(sys.argv[args_index:]) < 2:
                    logger.error("You need to specify <tool> <method name> <method>")
                else:
                    method = sys.argv[args_index]
                    content = " ".join(sys.argv[args_index+1:])
                    tools.add_hack_method(hack_name, method, content)
                
                
            else:
                logger.debug("I can't find your hack :(")
        

        elif sys.argv[2] == "del":
            if sys.argv[3] == "method":
                hack_name = str()
                found = False
                args_index = 4
                for arg in sys.argv[4:]:
                    hack_name += arg
                    if hack_name in [list(x.keys())[0] for x in tools.tools["hacks"]]:
                        found = True
                        break
                    args_index += 1
                    hack_name += " "
                if found:
                    if len(sys.argv[args_index:]) < 1:
                        logger.error("You need to specify del <tool_name> <method name>")
                    
                    tools.del_hack_method(hack_name, sys.argv[args_index])
                else:
                    logger.debug("I can't find your hack :(")
            else:
                tools.del_hack(" ".join(sys.argv[3:]))
        elif sys.argv[2] == "search":
            pass

        else:
            hack_name = " ".join(sys.argv[2:])
            if not hack_name in [list(x.keys())[0] for x in tools.tools["hacks"]]:
                logger.debug("Your hack does not exists :( I'm gonna create it !")
                tools.add_hack(hack_name)
            
            #mode = sys.argv[3]
    

if __name__ == "__main__":
    tools = Tools("/opt/sicalab/tools")
    tools.create_load_tools()

    if sys.argv[1] == "tools":
        args_tools()
    elif sys.argv[1] == "hacks":
        args_hacks()
    
    tools.write_tools()


