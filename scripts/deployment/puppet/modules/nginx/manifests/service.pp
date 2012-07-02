class nginx::service {

	package { 'nginx': 
	    ensure => present,
	    require => Exec['apt-get upgrade'],
	}

	service { 'nginx':
	    ensure => running,
	    require => Package['nginx'],
	}
	
}