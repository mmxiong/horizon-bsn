pwd
echo 'git commit is' ${GIT_COMMIT}
git clean -fxd
sudo pip install --upgrade 'tox==2.3.1'
tox -e pep8
setup_cfg_modified=`git log -m -1 --name-only --pretty="format:" | grep setup.cfg | wc -l`
if [ ${setup_cfg_modified} -ne 1 ];
  then echo "Update setup.cfg with new version number. Build FAILED";
  exit 1;
else
  echo "setup.cfg updated"; fi
# check the new_version > old_version
echo 'checking if version bump is correct'
git log -m -1 ${GIT_COMMIT} -p setup.cfg | grep version | python build/is_version_bumped.py
