from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from djangolg import models, methods


class Command(BaseCommand):
    help = "Manage Looking Glass Configuration"
    hr = "----"
    commands = [
        "list",
        "show",
        "add",
        "modify",
        "delete",
    ]
    objects = [
        "routers",
        "credentials",
        "locations"
    ]
    credential_types = dict(models.Credential.CRED_TYPE_CHOICES)

    def add_arguments(self, parser):
        parser.add_argument(
            'CMD', choices=self.commands,
            help="Operation to perform"
        )
        parser.add_argument(
            'OBJ', choices=self.objects,
            help="Type of object to manage"
        )
        parser.add_argument(
            '--index', '-I',
            help="Index of the object to manage"
        )
        parser.add_argument(
            '--name', '--hostname', '-n',
            type=str,
            help="Name (or hostname) of object"
        )
        parser.add_argument(
            '--location', '-l',
            type=int,
            help="Index of related location"
        )
        parser.add_argument(
            '--credentials', '-c',
            type=int,
            help="Index of related credentials"
        )
        parser.add_argument(
            '--dialect', '-d',
            choices=methods.dialects(),
            help="Name of related dialect"
        )
        parser.add_argument(
            '--sitecode', '-s',
            type=str,
            help="Location site code"
        )
        parser.add_argument(
            '--type', '-t',
            type=int,
            choices=self.credential_types.keys(),
            help="Credential type"
        )
        parser.add_argument(
            '--username', '-u',
            type=str,
            help="Credential username"
        )
        parser.add_argument(
            '--password', '-p',
            type=str,
            help="Credential password"
        )
        parser.add_argument(
            '--key', '-k',
            help="Credential key - not yet implemented"
        )

    def handle(self, *args, **options):
        hr = self.hr
        obj = options['OBJ']
        if obj == 'routers':
            cls = models.Router
        elif obj == 'credentials':
            cls = models.Credential
        elif obj == 'locations':
            cls = models.Location
        else:
            raise CommandError("Invalid object type")
        cmd = options['CMD']
        if cmd == 'list':
            self.list(cls)
        elif cmd == 'add':
            inst = self.add(cls, options)
            self.show(inst)
        else:
            if 'index' in options:
                index = options['index']
            else:
                raise CommandError("Please provide object index argument (--index)")
            try:
                inst = cls.objects.get(id=index)
            except Exception:
                raise CommandError("No %s found with index %s" % (obj, index))
            if cmd == 'show':
                self.show(inst)
            elif cmd == 'modify':
                inst = self.set(inst, options)
                self.show(inst)
            elif cmd == 'delete':
                self.delete(inst)
            else:
                raise CommandError("Invalid command")

    def list(self, cls=None):
        hr = self.hr
        objects = cls.objects.all()
        count = objects.count()
        if cls == models.Router:
            self.stdout.write(hr)
            self.stdout.write("Configured Routers")
            self.stdout.write(hr)
            if count:
                for r in objects:
                    self.stdout.write("Index: %s\tHostname: %s" % (r.id, r.hostname))
            else:
                self.stdout.write("No routers configured")
            self.stdout.write(hr)
        elif cls == models.Credential:
            self.stdout.write(hr)
            self.stdout.write("Configured Credentials")
            self.stdout.write(hr)
            if count:
                for c in objects:
                    self.stdout.write("Index: %s\tName: %s" % (c.id, c.name))
            else:
                self.stdout.write("No credentials configured")
            self.stdout.write(hr)
        elif cls == models.Location:
            self.stdout.write(hr)
            self.stdout.write("Configured Locations")
            self.stdout.write(hr)
            if count:
                for l in objects:
                    self.stdout.write("Index: %s\tName: %s" % (l.id, l.name))
            else:
                self.stdout.write("No locations configured")
            self.stdout.write(hr)

    def show(self, inst=None):
        hr = self.hr
        cls = type(inst)
        if cls == models.Router:
            self.stdout.write(hr)
            self.stdout.write("Router index: %s" % inst.id)
            self.stdout.write(hr)
            self.stdout.write("Hostname: %s" % inst.hostname)
            self.stdout.write("Location: %s" % inst.location)
            self.stdout.write("Credentials: %s" % inst.credentials)
            self.stdout.write("Dialect: %s" % inst.dialect)
            self.stdout.write(hr)
        elif cls == models.Credential:
            self.stdout.write(hr)
            self.stdout.write("Credential index: %s" % inst.id)
            self.stdout.write(hr)
            self.stdout.write("Name: %s" % inst.name)
            self.stdout.write("Type: %s" % self.credential_types[inst.type])
            self.stdout.write("Username: %s" % inst.username)
            self.stdout.write(hr)
        elif cls == models.Location:
            self.stdout.write(hr)
            self.stdout.write("Location index: %s" % inst.id)
            self.stdout.write(hr)
            self.stdout.write("Name: %s" % inst.name)
            self.stdout.write("Site Code: %s" % inst.sitecode)
            self.stdout.write(hr)

    def not_implemented(self, cmd):
        msg = "Command %s is not yet implemented" % cmd
        raise CommandError(msg)

    def add(self, cls, options):
        inst = self.set(cls(), options)
        return inst

    def set(self, inst, options):
        cls = type(inst)
        if cls == models.Router:
            if options['name']:
                inst.hostname = options['name']
            if options['location']:
                location = models.Location.objects.get(id=options['location'])
                inst.location = location
            if options['credentials']:
                credentials = models.Credential.objects.get(id=options['credentials'])
                inst.credentials = credentials
            if options['dialect']:
                inst.dialect = options['dialect']
        elif cls == models.Credential:
            if options['name']:
                inst.name = options['name']
            if options['type'] in self.credential_types:
                inst.type = options['type']
            if options['username']:
                inst.username = options['username']
            if options['password']:
                inst.password = options['password']
        elif cls == models.Location:
            if options['name']:
                inst.name = options['name']
            if options['sitecode']:
                inst.sitecode = options['sitecode']
        try:
            inst.save()
        except IntegrityError:
            raise
        except Exception:
            raise CommandError("Save failed")
        return inst

    def delete(self, inst):
        try:
            inst.delete()
        except Exception:
            raise CommandError("Delete failed")
