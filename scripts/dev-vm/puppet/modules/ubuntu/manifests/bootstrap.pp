class ubuntu::bootstrap {

  group { "puppet":
    ensure => "present"
	}

  exec { "apt-get update":
    command => "/usr/bin/apt-get update",
  }

  exec { "apt-get upgrade":
    command => "sudo apt-get -y upgrade",
    require => [Exec["apt-get update"]],
  }	

}