class akvo-rsr {

  # Setup a log file
  file { "/var/log/akvo":
      ensure => "directory",
      owner  => "vagrant",
      group  => "vagrant",
      mode   => 750,
  }

  file { "/var/log/akvo/akvo.log":
      ensure => "/var/log/akvo/akvo.log",
      owner  => "vagrant",
      group  => "vagrant",
      mode   => 750,
  }

  file { "/var/akvo/akvo/settings/60-local.conf":
    ensure  => present,
    content => template("akvo-rsr/60-local.conf.erb")
  }

}