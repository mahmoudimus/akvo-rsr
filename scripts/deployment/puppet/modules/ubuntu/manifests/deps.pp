class ubuntu::deps {

  package {
    [
      "checkinstall",
      "libssl-dev",
      "python-software-properties",
    ]:
    ensure => "latest",
    require => Class["ubuntu::bootstrap"],
  }
  
}
