local modules = script.Parent:WaitForChild("$modules_name")
local __require = require(modules:WaitForChild("__HathorLoader"))

__require("$entry_point")

