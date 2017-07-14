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
pkg_build_deps=(core/virtualenv core/glibc core/gcc core/make core/gcc-libs)
pkg_deps=(core/python core/coreutils core/openssl)
pkg_lib_dirs=(lib)
pkg_include_dirs=(include)
pkg_bin_dirs=(bin)
pkg_exports=(
    [host]=db.host
    [port]=db.port
    [ssl-port]=ssl.port
    )
pkg_exposes=(port ssl-port)

# Optional.
# An associative array representing services which you depend on and the configuration keys that
# you expect the service to export (by their `pkg_exports`). These binds *must* be set for the
# supervisor to load the service. The loaded service will wait to run until it's bind becomes
# available. If the bind does not contain the expected keys, the service will not start
# successfully.
# pkg_binds=(
#   [database]="port host"
# )

# Optional.
# Same as `pkg_binds` but these represent optional services to connect to.
# pkg_binds_optional=(
#   [storage]="port host"
# )

pkg_interpreters=(bin/bash)

# The default implementation tries to verify the checksum specified in the plan
# against the computed checksum after downloading the source tarball to disk.
# If the specified checksum doesn't match the computed checksum, then an error
# and a message specifying the mismatch will be printed to stderr. You should
# not need to override this behavior unless your package does not download
# any files.
do_verify() {
  do_default_verify
}

# The default implementation removes the HAB_CACHE_SRC_PATH/$pkg_dirname folder
# in case there was a previously-built version of your package installed on
# disk. This ensures you start with a clean build environment.
do_clean() {
  return 0
}

# The default implementation extracts your tarball source file into
# HAB_CACHE_SRC_PATH. The supported archives are: .tar, .tar.bz2, .tar.gz,
# .tar.xz, .rar, .zip, .Z, .7z. If the file archive could not be found or was
# not supported, then a message will be printed to stderr with additional
# information.
do_unpack() {
  do_default_unpack
}

# There is no default implementation of this callback. At this point in the
# build process, the tarball source has been downloaded, unpacked, and the build
# environment variables have been set, so you can use this callback to perform
# any actions before the package starts building, such as exporting variables,
# adding symlinks, and so on.
do_prepare() {
  return 0
}

# Build postgresql with PL/Python server-side language
do_build() {
  cd "${HAB_CACHE_SRC_PATH}/postgresql-${db_version}"
  ./configure --with-python --with-openssl --without-readline --without-zlib && make
}

# Run postgresql regression suite
do_check() {
  cd "${HAB_CACHE_SRC_PATH}/postgresql-${db_version}"
  make check
}

# Manually installing postgresql since habitat core
# postgres is not yet fully supported for cluster mode
do_install() {
    cd "${HAB_CACHE_SRC_PATH}/postgresql-${db_version}"
    make install
    # TODO: -explicitly set LD_LIBRARY_PATH and PATH for cross-platform compatibility
    #       -enable TCP/IP communication
}

# The default implementation is to strip any binaries in $pkg_prefix of their
# debugging symbols. You should override this behavior if you want to change
# how the binaries are stripped, which additional binaries located in
# subdirectories might also need to be stripped, or whether you do not want the
# binaries stripped at all.
do_strip() {
  return 0
}
