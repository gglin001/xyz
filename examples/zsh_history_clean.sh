mkdir -p _demos

xyz.zsh_history_clean \
  --n_lines 2 \
  -i examples/dot.zsh_history \
  -o _demos/dot.zsh_history.2

xyz.zsh_history_clean \
  --n_lines 3 \
  -i examples/dot.zsh_history \
  -o _demos/dot.zsh_history.3

xyz.zsh_history_clean \
  --n_lines 20 \
  -i examples/dot.zsh_history \
  -o _demos/dot.zsh_history.20
