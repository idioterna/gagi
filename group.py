#!/usr/bin/env python

import settings

import sys, tempfile, os

import gdata.apps.groups.client

try:
    group = sys.argv[1]
except:
    print >>sys.stderr, 'usage: %s <group> [-c for create] [-e for edit]' % sys.argv[0]
    sys.exit(0)

groupClient = gdata.apps.groups.client.GroupsProvisioningClient(domain=settings.DOMAIN)
groupClient.ClientLogin(email=settings.USER, password=settings.PASS, source='apps')

if '-c' in sys.argv:
    group_name = raw_input('name: ')
    description = raw_input('description: ')
    email_permission = 'Domain'
    groupClient.CreateGroup(group, group_name, description, email_permission)
    t = tempfile.NamedTemporaryFile(delete=False)
    n = t.name
    try:
        os.system('%s %s' % (settings.EDITOR, n))
        nusers = set([x.strip() for x in open(n).readlines()])

        for user in sorted(nusers):
            print 'adding', user
            groupClient.AddMemberToGroup(group, user)
    finally:
        os.unlink(n)
        sys.exit()


elif '-e' in sys.argv:
    members = groupClient.RetrieveAllMembers(group)
    users = set([u.member_id for u in members.entry])

    t = tempfile.NamedTemporaryFile(delete=False)
    n = t.name
    for user in sorted(users):
        t.write('%s\n' % user)
    t.close()
    try:
        os.system('%s %s' % (settings.EDITOR, n))
        nusers = set([x.strip() for x in open(n).readlines()])
        remove = users.difference(nusers)
        add = nusers.difference(users)

        for user in sorted(remove):
            print 'removing', user
            groupClient.RemoveMemberFromGroup(group, user)
        for user in sorted(add):
            print 'adding', user
            groupClient.AddMemberToGroup(group, user)
    finally:
        os.unlink(n)

else: # just list
    members = groupClient.RetrieveAllMembers(group)
    users = set([u.member_id for u in members.entry])

    for u in sorted(users):
        print u

