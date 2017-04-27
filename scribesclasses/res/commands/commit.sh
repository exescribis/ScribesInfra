echo '>>> add and commit for {key} >>>>>>>>>>>>>>>>>>>>>>>>>'
git -C {local_group_repo_dir} add .
git -C {local_group_repo_dir} commit -a -m "$1"
echo