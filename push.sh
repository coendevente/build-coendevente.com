# Example usage: sh push.sh "Commit message"

git pull
python3 generate.py
cd site
git add -u
git commit -m "$1"
git push
cd ..
git add -u 
git add site
git commit -m "$1"
git push --recurse-submodules=check
