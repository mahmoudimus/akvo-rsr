class ubuntu::tools {

  package {
    [
      "git-core",
      "mercurial",
      "nodejs",
      "npm",
      "node-less",
      "yui-compressor",
    ]:
    ensure => "latest",
    require => Class["ubuntu::deps"],
  }
  
}
