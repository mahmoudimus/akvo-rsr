# Set path
Exec {
  path => ["/usr/local/sbin", "/usr/local/bin", "/usr/sbin", "/usr/bin", "/sbin", "bin", "/opt/vagrant_ruby/bin"]
}

include ubuntu::bootstrap
include ubuntu::deps
include ubuntu::tools
include ubuntu::python

include nginx::service
include nginx::conf