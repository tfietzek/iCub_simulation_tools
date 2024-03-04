# config some useful aliases
git config alias.sdiff '!'"git diff && git submodule foreach 'git diff'"
git config alias.spush 'push --recurse-submodules=on-demand'
git config alias.supdate 'submodule update --remote --merge'
git config alias.sinit 'submodule update --init'

git submodule add https://github.com/tfietzek/iCub_Python_Lib.git
