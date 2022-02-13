# swissOrgaNice
A simple tool to find your toolset n hacks

aliases:
```bash
alias tools='python3 /opt/swissOrgaNice/swissOrgaNice.py tools'
alias hacks='python3 /opt/swissOrgaNice/swissOrgaNice.py hacks'
```

bash completion:
```bash
cp tools-autocomplete.bash ~/.bash-completion.d/tools-autocomplete.bash
echo "source ~/.bash-completion.d/tools-autocomplete.bash" >> ~/.zshrc
```
then type `rehash`

## Usage for "tools"

Names for tools are without spaces

### Print tools
`tools`

### Print portion of tools
print description of a tool
`tools <name> d[escription]`

print link of a tool
`tools <name> l[ink]`

### Add tool
`tools <name>`
or
`tools add <name>`

### Del tool
`tools del <name>`

### Define properties of tool
Add description
`tools <name> d[escription] <description here (can be without quotes)>`

Add link
`tools <name> l[ink] <link>`

### Search a tool
-> Search in name, description and link  
By tags
`tools search git,secrets`

By string
`tools search gitdumper`

## Usage for "hacks"

Names of hacks can be with spaces

### Print hacks
`hacks`

### Print hack category
`hacks path traversal`

### Add new hack to list
`hacks path traversal`

### Add method to hack
Syntax:
`hacks add <hack category> <method name> <method content>

Example:
`hacks add path traversal normal ../`
`hacks add path traversal urlencoded %2E%2E%2F`

### Del a hack (and all methods associated)
`hacks del path traversal`

### Del a method of a hack 
`hacks del method path traversal normal`