

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

    def search_tool(self, string):
        """
        Takes a string and regex searches the database
        """
        for tool in self.tools["tools"]:
            regex = compile(f".*{string}.*")
            if any([
                    regex.match(tool["name"]),
                    regex.match(tool["description"]),
                    regex.match(tool["link"]),
                ]):
                self.print_tool(tool)
                
    def add_hack(self, hack_name:str=None, description: str=None):
        """
        Adds a hack to the toolbox
        """
        # make sure we have the right structure for new databases
        self.tools.setdefault("hacks", dict())

        self.tools["hacks"]


if __name__ == "__main__":
    tools = Tools("/tmp/tools")
    tools.create_load_tools()
    logger.debug(sys.argv)
    if len(sys.argv) <= 1:
        for tool in tools.tools["tools"]:
            tools.print_tool(tool)
    elif len(sys.argv) <= 2:
        tool_name = sys.argv[1]
        if not tool_name in [x["name"] for x in tools.tools["tools"]]:
            logger.debug("Your tool does not exists :( I'm gonna create it !")
            tools.add_tool(sys.argv[1])
        tools.search_tool(sys.argv[1])
    else:
        if sys.argv[1] == "add":
            tools.add_tool(*sys.argv[2:])
        elif sys.argv[1] == "search":
            tools.search_tool(" ".join(sys.argv[2:]))
        elif sys.argv[1] == "del":
            tools.del_tool(sys.argv[2])
        else:
            tool_name = sys.argv[1]
            if not tool_name in [x["name"] for x in tools.tools["tools"]]:
                logger.debug("Your tool does not exists :( I'm gonna create it !")
                tools.add_tool(sys.argv[1])
            
            mode = sys.argv[2]

            if mode.lower().startswith("d"):
                mode = "description"
            elif mode.lower().startswith("l"):
                mode = "link"
            else:
                mode = None

            if len(sys.argv) < 3:
                # dumping content of requested tool's field
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
                if len(sys.argv) == 4:
                    content = "".join(sys.argv[3])
                else:
                    content = " ".join(sys.argv[3:])

                tools.tools["tools"][tool_index][mode] = content
    
    tools.write_tools()


