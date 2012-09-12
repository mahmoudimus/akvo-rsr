class nginx::service {

	package { "nginx":
		ensure => "installed"
	}

  # Add our nginc.conf file
  file { "/etc/nginx/nignx.conf":
    ensure  => present,
    mode    => 644,
    owner   => "root",
    group   => "root",
    content => template("nginx/nginx.conf.erb"),
    require => Package["nginx"],
  }

	file { "default-nginx-disable":
    path => "/etc/nginx/sites-enabled/default",
    ensure => absent,
    require => Package["nginx"],
  }

  # Add our vhost file to sites-available
  file { "/etc/nginx/sites-available/akvo.dev":
    ensure  => present,
    mode    => 644,
    owner   => "root",
    group   => "root",
    content => template("nginx/akvo.dev.erb"),
    require => File["default-nginx-disable"]
  }
 
  # Enable our host file
  file { "/etc/nginx/sites-enabled/akvo.dev":
    ensure => "link",
    target => "/etc/nginx/sites-available/akvo.dev",
    require =>  File["/etc/nginx/sites-available/akvo.dev"],
	}

	service { "nginx":
		ensure => "running",
		require => File["/etc/nginx/sites-enabled/akvo.dev"],
	}

	# exec { "sudo add-apt-repository ppa:nginx/stable && sudo apt-get update":
 	#    alias => "nginx_repository",
  #    require => Package["python-software-properties"],
  #    creates => "/etc/apt/sources.list.d/nginx-stable-precise.list",
	# }

	# exec { "sudo apt-get install -y nginx":
	# 	command => "sudo apt-get install -y -f nginx",
	# 	require =>  [Exec["add-apt-repository ppa:nginx/stable && apt-get update"]],
	# }
	
}