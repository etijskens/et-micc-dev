#!/bin/bash
# this is for et-micc[-build] development only
# micc users do not need this

# commit and push et-micc
cd ../et-micc
git commit -a -u -m "publish to PyPI"
git push -u origin master
echo "If there are untracked files that need to be published,"
echo " 1. stop the script (by entering 'n')"
echo " 2. 'git add' the files"
echo " 3. rerun this script."

read -p "Continue? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
	# commit and push et-micc-build
	cd ../et-micc-build
	git commit -a -u -m "publish to PyPI"
	git push -u origin master
	echo "If there are untracked files that need to be published,"
	echo " 1. stop the script (by entering 'n')"
	echo " 2. 'git add' the files"
	echo " 3. rerun this script."

	read -p "Continue? " -n 1 -r
	echo    # (optional) move to a new line
	if [[ $REPLY =~ ^[Yy]$ ]]
		echo "git add untracked files"
	then
		#bump versions
		cd ../et-micc
		micc version -p
		git commit -a -u -m "publish to PyPI"
		git push -u origin master
		
		cd ../et-micc-build
		micc version -p
		git commit -a -u -m "publish to PyPI"
		git push -u origin master
		
		./align_versions.py
		
		cd ../et-micc       && poetry publish --build
		cd ../et-micc-build && poetry publish --build
	fi
fi
