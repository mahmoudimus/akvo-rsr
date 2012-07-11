class ubuntu::deps {

  package {
    [
      "checkinstall",
      "libssl-dev",
      "python-software-properties",
      "libxml2-dev",
      "ibxslt1-dev",
      "libmysqlclient-dev",
    ]:
    ensure => "latest",
    require => Class["ubuntu::bootstrap"],
  }
  
}
