class ubuntu::deps {

  package {
    [
      "checkinstall",
      "libssl-dev",
      "python-software-properties",
      "libxml2-dev",
      "libxslt1-dev",
      "libmysqlclient-dev",
      "build-essential", 
      "python-imaging",
      "libjpeg62-dev",
      "zlib1g-dev",
      "libfreetype6-dev",
      "gettext"
    ]:
    ensure => "latest",
    require => Class["ubuntu::bootstrap"],
  }
  
}
