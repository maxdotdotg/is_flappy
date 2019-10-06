pkg_name=is_flappy
pkg_origin=maxg
pkg_version="0.1.1"
pkg_maintainer="max g<maxdotdotg@gmail.com>"
pkg_license=("GPL-3.0")
pkg_shasum="TODO"

pkg_deps=(core/python/3.6.0)

do_download() {
  return 0
}

do_verify() {
  return 0
}

do_unpack() {
  return 0
}

do_build() {
  return 0
}


do_install() {
  # copy across the app plus requirements
  app_dir=$pkg_prefix/$pkg_name
  mkdir $app_dir
  cp service/is_flappy.py $app_dir/
  cp service/requirements.txt $app_dir/
  #install pip/virtualenv packages on top of python dependency (i.e. site packages)
  pip install --upgrade pip
  pip install virtualenv
  # create virtualenv for our dependencies & install
  virtualenv $app_dir/flappy_env
  source $app_dir/flappy_env/bin/activate
  pip install -r $app_dir/requirements.txt
  # ensure hab user can activate the virtualenv
  chown -R hab:hab $app_dir
}

