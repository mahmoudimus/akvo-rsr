class ubuntu::bootstrap {

	group { "puppet":
		ensure => "present"
	}

	exec { 'apt-get update':
    command => 'sudo /usr/bin/apt-get update'
  }

  exec { 'apt-get upgrade':
    command => 'sudo /usr/bin/apt-get -y upgrade',
    require => [Exec["apt-get update"]],
  }	

}