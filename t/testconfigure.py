from talerbuildconfig import *

b = BuildConfig()
b.enable_prefix()
b.enable_configmk()
b.add_tool(YarnTool())
b.add_tool(BrowserTool())
b.add_tool(PyBabelTool())
b.add_tool(NodeJsTool())
b.add_tool(PythonTool())
b.add_tool(PosixTool("find"))
b.add_tool(PosixTool("xargs"))
b.add_tool(PosixTool("msgmerge"))
b.run()
