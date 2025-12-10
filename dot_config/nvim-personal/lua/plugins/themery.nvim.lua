-- Plugin: zaldih/themery.nvim
-- Installed via store.nvim

return {
    "zaldih/themery.nvim",
    lazy = false,
    config = function()
        require("themery").setup(
            {
		    themes = {"gruvbox", "vscode", "tokyonight", "cyberdream"}
	    }
        )
     end
}
