# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.
  config.vm.host_name = "akvo.dev"

  # Dev Box conf
  config.vm.box = "akvo_rsr_12.04_64_4.22"
  config.vm.box_url = "https://dl.dropbox.com/s/y2zi3ykxd71c1l4/akvo_rsr_12.04_64_4.22.box?dl=1"

  # Box config for building a base box
  # config.vm.box = "precise64"
  # config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  # config.vm.boot_mode = :gui

  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "dev-env/puppet/manifests"
    puppet.manifest_file = "dev.pp"
    puppet.module_path = "dev-env/puppet/modules"
    # puppet.options = "--verbose --debug"
    puppet.options = "--verbose"
  end

  # Assign this VM to a host-only network IP, allowing you to access it
  # via the IP. Host-only networks can talk to the host machine as well as
  # any other machines on the same network, but cannot be accessed (through this
  # network interface) by any external networks.
  # config.vm.network :hostonly, "192.168.33.10"
  config.vm.network :hostonly, "33.33.33.15"

  # Assign this VM to a bridged network, allowing you to connect directly to a
  # network using the host's network device. This makes the VM appear as another
  # physical device on your network.
  # config.vm.network :bridged

  # Forward a port from the guest to the host, which allows for outside
  # computers to access the VM, whereas host only networking does not.
  # config.vm.forward_port 80, 8080
  config.vm.forward_port 80, 4520     # Nginx
  config.vm.forward_port 1337, 4521   # Django dev server
  config.vm.forward_port 3306, 4522   # MySQL

  # Share an additional folder to the guest VM. The first argument is
  # an identifier, the second is the path on the guest to mount the
  # folder, and the third is the path on the host to the actual folder.
  # config.vm.share_folder "v-data", "/vagrant_data", "../data"
  config.vm.share_folder("v-root", "/var/akvo", ".", :nfs => true)

end