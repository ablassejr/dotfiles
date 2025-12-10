-- Plugin: 2KAbhishek/octohub.nvim
-- Installed via store.nvim

return {
    "2kabhishek/octohub.nvim",
    cmd = {"Octohub"},
    keys = {"<leader>goo"}, -- Add more bindings as needed
    dependencies = {
        "2kabhishek/utils.nvim",
        "2kabhishek/pickme.nvim"
    },
    -- Add your custom configs here, keep it blank for default configs (required)
    opts = {}
}