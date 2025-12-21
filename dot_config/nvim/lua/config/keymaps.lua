-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here
local set = vim.keymap.set
set("n", "<leader>ss", "<cmd>Trouble symbols<CR>")
set("n", "<leader>vr", "<cmd>VectorCode register<CR>")
set("n", "<leader>uv", "<cmd>VectorCode<CR>")
set("n", "<leader>ns", "<cmd> NoiceSnacks<CR>")
