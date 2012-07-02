class ubuntu::python {

  package {
    [
    	"python-setuptools",
    	"python-pip",
    	"python-virtualenv"
    ]:
    ensure => "latest",
    require => Class['ubuntu::tools'],
  }
  
}
