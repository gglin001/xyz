mkdir -p _demos

xyz.string_splitter examples/string_splitter.txt -o _demos/string_splitter.txt.split

args=(
  examples/string_splitter.txt
  -o _demos/string_splitter.txt.split2
  -m " -"
  -m " --"
  -m " \"-D"
)
xyz.string_splitter "${args[@]}"
