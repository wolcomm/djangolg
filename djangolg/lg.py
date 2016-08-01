import paramiko


class LookingGlass(object):
    def __init__(self, router=None, port=22):
        self.router = router
        self.credentials = router.credentials
        self.syntax = router.syntax
        self.defaults = {
            'ssh_host_key_policy': paramiko.WarningPolicy(),
            'ssh_port': port,
        }

    def _connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(
            self.defaults['ssh_host_key_policy']
        )
        try:
            self.ssh.connect(
                hostname=self.router.hostname,
                port=self.defaults['ssh_port'],
                username=self.credentials.username,
                password=self.credentials.password,
            )
        except Exception:
            raise
        return self

    def _disconnect(self):
        if self.ssh:
            try:
                self.ssh.close()
            except Exception:
                raise
            del self.ssh
        else:
            raise ValueError
        return self

    def _exec(self, cmd=None):
        if self.ssh:
            try:
                stdin, stdout, stderr = self.ssh.exec_command(cmd)
                output = stdout.read()
            except Exception:
                raise
        else:
            raise ValueError
        return output

    def _build_cmd(self, method, target=None):
        cmd = method.cmd(target)
        return cmd

    def execute(self, method=None, target=None, options=None):
        cmd = self._build_cmd(method, target=target)
        try:
            output = self._connect()._exec(cmd)
        except Exception:
            raise
        finally:
            self._disconnect()
        return output

    # TODO: Remove
    def bgp_prefix(self, prefix=None, longer_prefixes=None, bestpath_only=None):
        af = "ipv%s" % prefix.version
        addr = str(prefix)
        if longer_prefixes:
            cmd = "show bgp %s unicast %s longer-prefixes | begin Network" % (af, addr)
        elif bestpath_only:
            cmd = "show bgp %s unicast %s bestpath" % (af, addr)
        else:
            cmd = "show bgp %s unicast %s" % (af, addr)
        try:
            output = self._connect()._exec(cmd)
        except Exception:
            raise
        finally:
            self._disconnect()
        return output
