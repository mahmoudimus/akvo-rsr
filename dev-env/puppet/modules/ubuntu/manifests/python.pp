class ubuntu::python {

  package {
    [
    	"python-dev",
    	"python-setuptools",
    	"python-pip",
    	"python-virtualenv"
    ]:
    ensure => "latest",
    require => Class["ubuntu::tools"],
  }

  exec { "PyCrypto":
    command => "sudo pip install PyCrypto",
    require => Package["python-dev"],
  }

  exec { "Fabric":
    command => "sudo pip install Fabric",
    require => Exec["PyCrypto"],
  }
 
}
