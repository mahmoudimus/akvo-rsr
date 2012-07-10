class uwsgi {

  package { "uwsgi":
    ensure => "latest",
  }

  file { "/etc/init/uwsgi.conf":
    ensure  => present,
    mode    => 644,
    owner   => "root",
    group   => "root",
    content => template("uwsgi/uwsgi.conf.erb"),
    require => Package["uwsgi"],
  }

  service { "uwsgi":
    ensure => "running",
    require => File["/etc/init/uwsgi.conf"],
  }

  file { "/etc/uwsgi/apps-available/djangoapp.ini":
    ensure  => present,
    mode    => 644,
    owner   => "root",
    group   => "root",
    content => template("uwsgi/djangoapp.ini.erb"),
    require => Service["uwsgi"],
  }

  # Enable our host file
  file { "/etc/uwsgi/apps-enabled/djangoapp.ini":
    ensure => "link",
    target => "/etc/uwsgi/apps-available/djangoapp.ini",
    #notify => Service["nginx"],
    require => File["/etc/uwsgi/apps-available/djangoapp.ini"],
  }
  
}