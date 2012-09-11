# Set path
Exec {
  path => ["/usr/local/sbin", "/usr/local/bin", "/usr/sbin", "/usr/bin", "/sbin", "bin", "/opt/vagrant_ruby/bin"]
}

include ubuntu::bootstrap
include ubuntu::deps
include ubuntu::tools
include ubuntu::python

include nginx::service
# include nginx::conf

class { 'mysql': }
class { 'mysql::python': }
class { 'mysql::server':
	config_hash => { 'root_password' => 'ocean' }
}
mysql::db { 'rsr':
  user     => 'rsr-user',
  password => 'lake',
  host     => 'localhost',
  grant    => ['all'],
}

#include uwsgi