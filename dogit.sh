# Example usage: sh dogit.sh "Commit message"

cd site
git add -u
git commit -m "$0"
git push
cd ..
git add -u 
git add site
git commit -m "$0"
git push --recurse-submodules=check
