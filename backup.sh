cd ~/.config/
git add -A -- $(cat gitdirs.txt)
git commit -m "configs"
git push origin master

cd ~/nts/
git add .
git commit -m "notes"
git push origin master

cd ~/run/
git add .
git commit -m "run"
git push origin master

#cd ~/prj/youngplanet-env/
#git add .
#git commit -m "youngplanet"
#git push origin master

cd ~/prj/college/
git add .
git commit -m "college"
git push origin master
