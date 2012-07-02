class nginx::conf {

	# Disable default nginx virtualhost
	file { 'default-nginx-disable':
    path => '/etc/nginx/sites-enabled/default',
    ensure => absent,
    # require => Package['nginx'],
    # require => Class['nginx::service'],
	}
	

	# Add our vhost file to sites-available
	file { "/etc/nginx/sites-available/akvo.dev":
    ensure  => present,
    mode    => 644,
    owner   => "root",
    group   => "root",
    content => template("nginx/akvo.dev.erb"),
    # notify  => Service['nginx'],
    # require => File['default-nginx-disable'],
    require => Class['nginx::service'],
  }

  # Enable our vhost file
  file { 'akvo.dev-nginx-enable':
    path => '/etc/nginx/sites-enabled/akvo.dev',
    target => '/etc/nginx/sites-available/akvo.dev',
    ensure => link,
    notify => Service['nginx'],
    require => [
    	File['/etc/nginx/sites-available/akvo.dev'],
    	File['default-nginx-disable'],
    ],
	}

}