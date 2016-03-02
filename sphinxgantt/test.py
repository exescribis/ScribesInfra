import xml.etree.ElementTree as ET
tree = ET.parse('test.gan')
root = tree.getroot()

# TODO: task nesting + task dependency
# for task in root.iter('task'):
#    print task.attrib

for task in root.iter('task'):
    print task.get('id'), task.get('name'), task.get('start'), task.get('duration')

print '----- allocation ------------'
for allocation in root.iter('allocation'):
    print allocation.get('task-id'), allocation.get('resource-id'), allocation.get('function'), allocation.get('responsible'), allocation.get('load')

print '----- roles -----------------'
for role in root.iter('role'):
    print role.get('id'), role.get('name')

print '----- resources -------------'
for resource in root.iter('resource'):
    print resource.get('id'), resource.get('name'), resource.get('function')

print ''
print '----- ressource vacations ---'
for vacation in root.iter('vacation'):
    print vacation.get('start'), vacation.get('end'), vacation.get('resourceid')

print '----- global vacation -------'
for date in root.iter('date'):
    print date.get('date'),date.get('month'),date.get('year')
