# Habitat plan for deployment of PostgreSQL database server

pkg_name=pgsqldb-server
pkg_origin=brighthive
pkg_version=9.6.3
pkg_svc_data_path=/var/lib/pgsql/data
pkg_maintainer="jee@brighthive.io stanley@brighthive.io aretha@brighthive.io"
pkg_license=('Apache-2.0')
pkg_description="PostgreSQL database service for TPOT transactional database."
pkg_upstream_url=https://www.postgresql.org
pkg_source=https://ftp.postgresql.org/pub/source/v${pkg_version}/postgresql-${pkg_version}.tar.gz
pkg_shasum=df088372230b1dd21d87bb81686471508f4c42094d4f4f32b5d8e686fea69fa6
pkg_dirname=postgresql-${pkg_version}
pkg_deps=(
    core/bash
    core/python
    core/glibc
    core/libossp-uuid
    core/shadow    
    core/readline
    core/zlib
    core/openssl 
  )
pkg_build_deps=(
  core/coreutils
  core/gcc
  core/make
  )
pkg_lib_dirs=(lib)
pkg_include_dirs=(include)
pkg_bin_dirs=(bin)
pkg_exports=(
    [host]=db.host
    [port]=db.port
    [ssl-port]=ssl.port
    )
pkg_exposes=(port ssl-port)
pkg_interpreters=(bin/bash)
pkg_svc_user=root
pkg_svc_group=root


# Build postgresql with PL/Python server-side language
do_build() {
    cd "${HAB_CACHE_SRC_PATH}/${pkg_dirname}"
    ./configure --with-python \
	            --disable-rpath \
                --with-openssl \
                --with-uuid=ossp \
                --with-includes="$LD_INCLUDE_PATH" \
                --with-libraries="$LD_LIBRARY_PATH" \
                --sysconfdir="$pkg_svc_config_path" \
                --localstatedir="$pkg_svc_var_path"
    make

}

# Install built postgresql
do_install() {
  cd "${HAB_CACHE_SRC_PATH}/${pkg_dirname}"
  make install
}

