# Example usage: sh push.sh "Commit message"

python3 generate.py
cd site
git add -u
git commit -m "$0"
git push
cd ..
git add -u 
git add site
git commit -m "$0"
git push --recurse-submodules=check
