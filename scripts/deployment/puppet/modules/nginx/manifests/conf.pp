class nginx::conf {

	# Disable default nginx virtualhost
	file { 'default-nginx-disable':
    path => '/etc/nginx/sites-enabled/default',
    ensure => absent,
    require => Class['nginx::service'],
	}
	
	# Add our vhost file to sites-available
	file { "/etc/nginx/sites-available/akvo.dev":
    ensure  => present,
    mode    => 644,
    owner   => "root",
    group   => "root",
    content => template("nginx/akvo.dev.erb"),
    # require => Service['nginx'],
    require => File['default-nginx-disable']
  }

  # Enable our host file
	file { '/etc/nginx/sites-enabled/akvo.dev':
   ensure => 'link',
   target => '/etc/nginx/sites-available/akvo.dev',
   #notify => Service['nginx'],
   require => File["/etc/nginx/sites-available/akvo.dev"]
    # require => [
    # 	File['/etc/nginx/sites-available/akvo.dev'],
    # 	File['default-nginx-disable'],
    # ],
	}

}