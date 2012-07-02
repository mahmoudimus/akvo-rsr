class ubuntu::deps {

  package {
    [
      "build-essential",
      "checkinstall",
      "libssl-dev",
    ]:
    ensure => "latest",
    require => Class['ubuntu::bootstrap'],
  }
  
}
