local HATHOR_ROOT = script.Parent
local HATHOR_CACHE = {}
local function __require(require_str)
    if HATHOR_CACHE[require_str] then
        return HATHOR_CACHE[require_str]
    end

    local instance = HATHOR_ROOT:WaitForChild(require_str, 3)
    assert(instance, "Did not find a module in time")

    local loaded = require(instance)
    HATHOR_CACHE[require_str] = loaded

    instance.Name = instance.ClassName
    instance:Destroy()

    return loaded
end

return __require
