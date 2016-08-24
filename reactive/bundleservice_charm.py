from charms.reactive import (
    hook,
    set_state,
    when,
    when_not,
)
from charmhelpers.core import host


@when_not('bundleservice-charm.installed')
def install_bundleservice_charm():
    set_state('bundleservice-charm.installed')


@when('nrpe-external-master.available')
def setup_nagios(nagios):
    config = hookenv.config()
    unit_name = hookenv.local_unit()
    nagios.add_check(['/usr/lib/nagios/plugins/check_http',
        '-I', '127.0.0.1', '-p', str(config['port']),
        '-e', " 404 Not Found", '-u', '/'],
        name="check_http",
        description="Verify bundleservice is running",
        context=config["nagios_context"],
        unit=unit_name,
    )


def restart():
    host.service_restart('bundleservice') or \
        host.service_start('bundleservice')


@hook('config-changed')
def config_changed():
    restart()