from devices.models import Device
from lorem.text import TextLorem
import string
import random


def create_random_data( count ):
	name_generator = TextLorem(srange=(2,4))
	description_generator = TextLorem(srange=(4,8))
	registered = True
	for i in range( count ):
		device = Device.objects.create(
			name = f'{name_generator.sentence()}_{count}', 
			serial_id=''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
			description=description_generator.sentence(), 
			address=''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
			registered=registered
			)
		if registered:
			registered = False
		else:
			registered = True

def create_sample_data():
	device = Device.objects.create(
		name = "active item 1", 
		serial_id='123',
		description="active item description", 
		address='ABC',
		registered=True
		)

	device = Device.objects.create(
		name = "active item 2", 
		serial_id='234',
		description="active item description", 
		address='DEF',
		registered=True
		)

	device = Device.objects.create(
		name = "pending item 1", 
		serial_id='345',
		description="pending item description", 
		address='GHI',
		registered=False
		)

	device = Device.objects.create(
		name = "pending item 2", 
		serial_id='456',
		description="pending item description", 
		address='JKL',
		registered=False
		)
