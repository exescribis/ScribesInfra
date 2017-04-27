mkdir -p {local_groups_dir}

echo '>>> Cloning group {key} and adding root remote'
git -C {local_groups_dir} clone --quiet {group_repo_account_url}
git -C {local_group_repo_dir} remote add root {root_repo_account_url}
echo
