class nginx::service {

	exec { 'ppa:nginx/stable':
    command => 'sudo add-apt-repository ppa:nginx/stable',
    require => Exec['apt-get upgrade'],
  }

	package { 'nginx': 
	    ensure => present,
	    require => [Exec["ppa:nginx/stable"]],
	}

	service { 'nginx':
	    ensure => running,
	    require => Package['nginx'],
	}
	
}