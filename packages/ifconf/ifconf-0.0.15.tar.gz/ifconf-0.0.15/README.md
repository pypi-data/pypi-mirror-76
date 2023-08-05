# Integrated Framework for Configuration

Alternative configuration framework using argparse and configparser.
Designed for the following purposes.

* Integration of command line args and configuration files
* Generation of default configuration files
* Class initialization procedure using parameter object pattern

## SAMPLE

* main.py 

        from ifconf import configure_main
        if __name__ == "__main__":
                configure_main()

* server.py
        
        from ifconf import configure_module, config_callback
        
        @config_callback
        def conf(loader):
            loader.add_attr('server_addr', '0.0.0.0', help='server inet addr to bind')
                loader.add_attr_int('server_port', 8080, help='server inet port to bind')
                loader.add_attr_boolean('udp', False, help='True if use UDP otherwise TCP is used.')
                loader.add_attr_float('val_float', 0.8, help='float test value')
                loader.add_attr_dict('val_dict', {'a':1,'b':2,'c':3}, help='dict test value')
                loader.add_attr_list('val_list', [1,2,3], help='list test value')
                loader.add_attr_path('home', '../', help='path test value')
        
        class MyClass:
                def __init__(self):
                        self.conf = configure_module(conf)
                        self.addr = self.conf.addr
                        self.port = self.conf.port
                        self.conf.logger.info(self.conf)
        
* config.ini

        [server_conf]
        #addr = 0.0.0.0
        port = 8888


## config file generation

You can print config.ini template

        python -m ifconf server.config

## Install

You can install this package by pip

        pip3 install ifconf

If you need to use 'mutable' option, install 'recordclass' as well.

        pip3 install ifconf recordclass
	
If you got an error such as 'error: command 'x86_64-linux-gnu-gcc' failed with exit status 1', you need to install build essentials.

        sudo apt-get install build-essential libssl-dev libffi-dev python3-dev



