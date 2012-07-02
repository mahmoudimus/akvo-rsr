class ubuntu::tools {

  package {
    [
      "nodejs",
      "npm",
      "node-less",
      "yui-compressor"
    ]:
    ensure => "latest",
    require => Class['ubuntu::deps'],
  }
  
}
