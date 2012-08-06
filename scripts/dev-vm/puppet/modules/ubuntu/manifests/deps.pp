class ubuntu::deps {

  package {
    [
      "checkinstall",
      "libssl-dev",
      "python-software-properties",
      "libxml2-dev",
      "ibxslt1-dev",
      "libmysqlclient-dev",
      "build-dep",
      "python-imaging",
      "libjpeg62-dev",
      "zlib1g-dev",
      "libfreetype6-dev"
    ]:
    ensure => "latest",
    require => Class["ubuntu::bootstrap"],
  }
  
}
