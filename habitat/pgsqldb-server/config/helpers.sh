# Helper functions used in deployment

check_user_exists() { 
    echo $(id -u $1 > /dev/null 2>&1; echo $?) 

}

check_group_exists() {
    echo $(getent group $1 > /dev/null 2>&1; echo $?) 
}

delete_db_superuser() {
    userdel {{cfg.superuser.name}}
    groupdel {{cfg.superuser.group}}

}

create_db_superuser_group() {
    if [ $(check_group_exists "{{cfg.superuser.group}}") -ne 0 ]; then
        echo "Create database superuser group"
        groupadd {{cfg.superuser.group}}
    fi        

}
create_db_superuser() {
    if [ $(check_user_exists "{{cfg.superuser.name}}") -eq 1 ]; then
        echo "Create database superuser"
        useradd -g {{cfg.superuser.group}} {{cfg.superuser.name}}
    fi

}

set_dir_permissions() {
    echo "Set owner of var, config and data paths to postgres db superuser"
    chown -Rv {{cfg.superuser.name}}:{{cfg.superuser.group}} {{pkg.svc_var_path}} 
    chown -Rv {{cfg.superuser.name}}:{{cfg.superuser.group}} {{pkg.svc_config_path}} 
    chown -Rv {{cfg.superuser.name}}:{{cfg.superuser.group}} {{pkg.svc_data_path}} 

}
