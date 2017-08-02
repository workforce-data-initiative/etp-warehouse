# Helper variables and functions used in deployment


check_user_exists() { 
    echo $(id -u $1 > /dev/null 2>&1; echo $?) 

}

check_group_exists() {
    echo $(getent group $1 > /dev/null 2>&1; echo $?) 
}

delete_db_superuser() {
    deluser {{cfg.superuser.name}}
    delgroup {{cfg.superuser.group}}

}

create_db_superuser_group() {
    if [ $(check_group_exists "{{cfg.superuser.group}}") -ne 0 ]; then
        echo "Create database superuser group"
        addgroup {{cfg.superuser.group}}
    fi        

}

create_db_superuser() {
    create_db_superuser_group

    if [ $(check_user_exists "{{cfg.superuser.name}}") -eq 1 ]; then
        echo "Create database superuser"
        adduser -G {{cfg.superuser.group}} {{cfg.superuser.name}}
    fi

    id {{cfg.superuser.name}}

}

setup_db_datapath() {
    parent_datapath=$(dirname {{cfg.db.datapath}})
    echo "Create postgres data directories"
    mkdir -pv $parent_datapath
    chown -LRv {{cfg.superuser.name}}:{{cfg.superuser.group}} $parent_datapath
    chmod -Rv 700 $parent_datapath
    
}

set_dir_permissions() {
    echo "Set owner of var, config and data paths to postgres db superuser"
    chown -LRv {{cfg.superuser.name}}:{{cfg.superuser.group}} {{pkg.svc_var_path}} 
    chown -LRv {{cfg.superuser.name}}:{{cfg.superuser.group}} {{pkg.svc_config_path}} 
    chown -LRv {{cfg.superuser.name}}:{{cfg.superuser.group}} {{pkg.svc_data_path}}

}

calc_mem_conf() {
    return 0
}
