from djangolg.methods.base import BaseMethod
from django import forms
from djangolg import fields


class BGPPrefixMethod(BaseMethod):
    name = "bgp_prefix"
    title = "BGP Prefix"
    description = """
    Look up BGP RIB entries for the target IP prefix. The prefix field accepts
    both IPv4 and IPv6 address families. Options are provided to search for all
    exact-match paths, the BGP bestpath only, or all longer-match paths.
    """
    target_field = fields.IPPrefixField(
        required=True,
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': "Prefix",
            'data-toggle': 'tooltip',
            'title': "IP address or prefix"
        }),
        label='Prefix'
    )
    options = ["All paths", "Bestpath Only", "Longer Prefixes"]


class BGPASPathMethod(BaseMethod):
    name = "bgp_as_path"
    title = "BGP AS Path"
    description = """
    Look up BGP RIB entries with an AS_PATH attribute matching the target
    regular expression. The AS Path Regex field accepts Cisco IOS style regular
    expressions. Options are provided to select either the IPv4 or the IPv6
    address family.
    """
    target_field = forms.CharField(
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': "AS Path Regex",
            'data-toggle': 'tooltip',
            'title': "AS path regular expression"
        }),
    )
    options = ["IPv4", "IPv6"]


class BGPCommunityMethod(BaseMethod):
    name = "bgp_community"
    title = "BGP Community"
    new = True
    description = """
    Look up BGP RIB entries with a COMMUNITIES attribute that contains the
    target value. The Community Value field accepts a pair of colon-seperated
    16-bit decimal numbers. Some platforms may also support named "well known"
    community values such as 'no-export', etc. Options are provided to select
    either the IPv4 or the IPv6 address family.
    """
    target_field = forms.CharField(
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': "Community Value",
            'data-toggle': 'tooltip',
            'title': "RFC1997 Community Value"
        }),
    )
    options = ["IPv4", "IPv6"]


class PingMethod(BaseMethod):
    name = "ping"
    title = "Ping"
    description = """
    Send a series of ICMP echo requests to the target IP address, and report
    whether responses were received. Target Address field accepts both IPv4 and
    IPv6 addresses, but not DNS names. The source address of the generated
    requests will default to the address on the first loopback interface of the
    selected router.
    """
    target_field = fields.IPAddressField(
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': "Target Address",
            'data-toggle': 'tooltip',
            'title': "Target IP address"
        }),
    )


class TracerouteMethod(BaseMethod):
    name = "trace_route"
    title = "Traceroute"
    description = """
    Perform a traceroute from the selected router to the target IP address.
    Target Address field accepts both IPv4 and IPv6 addresses, but not DNS
    names.
    """
    target_field = fields.IPAddressField(
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': "Target Address",
            'data-toggle': 'tooltip',
            'title': "Target IP address"
        }),
    )
