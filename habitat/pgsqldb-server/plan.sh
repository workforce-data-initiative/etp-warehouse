# Habitat plan for deployment of PostgreSQL database server

pkg_name=pgsqldb-server
pkg_origin=brighthive
pkg_version=0.1.0
db_version="9.6.3"
pkg_svc_user = "tpotdb"
pkg_maintainer="jee@brighthive.io stanley@brighthive.io aretha@brighthive.io"
pkg_license=('Apache-2.0')
pkg_description="PostgreSQL database service for TPOT transactional database."
pkg_upstream_url="https://github.com/workforce-data-initiative/tpot-warehouse"
# will this syntax pick db.ver from default.toml?
pkg_source="https://ftp.postgresql.org/pub/source/v$db_version/postgresql-$db_version.tar.gz"
pkg_filename="postgresql-${db_version}.tar.gz"
pkg_shasum="df088372230b1dd21d87bb81686471508f4c42094d4f4f32b5d8e686fea69fa6"
pkg_build_deps=(
  core/coreutils
  core/virtualenv
  core/gcc
  core/make)
pkg_deps=(
  core/bash
  core/envdir
  core/glibc
  core/openssl
  core/perl
  core/readline
  core/zlib
  core/libossp-uuid
  core/wal-e
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

# Build postgresql with PL/Python server-side language
do_build() {
  cd "${HAB_CACHE_SRC_PATH}/postgresql-${db_version}"
  ./configure --disable-rpath \
              --with-openssl \
              --prefix="$pkg_prefix" \
              --with-uuid=ossp \
              --with-includes="$LD_INCLUDE_PATH" \
              --with-libraries="$LD_LIBRARY_PATH" \
              --sysconfdir="$pkg_svc_config_path" \
              --localstatedir="$pkg_svc_var_path"
  make world
  # ./configure --with-python --with-openssl --with-includes=/usr/local/include/openssl --with-libraries=/usr/local/lib
}

# Manually installing postgresql since habitat core
# postgres is not yet fully supported for cluster mode
do_install() {
    cd "${HAB_CACHE_SRC_PATH}/postgresql-${db_version}"
    make install-world
    # TODO: -explicitly set LD_LIBRARY_PATH and PATH for cross-platform compatibility
    #       -enable TCP/IP communication
}
