# class uwsgi {

# 	exec { "add-apt-repository ppa:uwsgi/release && apt-get update":
#     alias => "nginx_repository",
#     require => Package["python-software-properties"],
#     creates => "/etc/apt/sources.list.d/uwsgi-release-precise.list",
# 	}
	
#   exec { "sudo apt-get install uwsgi":
#     command => "sudo apt-get install -y uwsgi",
#     require => Exec["add-apt-repository ppa:uwsgi/release && apt-get update"],
#   }

# }