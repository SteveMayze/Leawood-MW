from django.test import TestCase
from devices.models import Device, Location, Log_Entry
from django.core.exceptions import ValidationError
import json

# The Devices application will also track the data to be recorded 
# the units of measure and also the deployed location of the device.

class DevicesModelTest( TestCase ):

	def test_cannot_save_with_blank_columns(self):
		device = Device(name = "device_a", description="device description")
		with self.assertRaises(ValidationError):
			device.save()
			device.full_clean()


	def test_registered_is_false_by_default( self ):
		device = Device(
				name="device_a", 
				description="device description",
				serial_id = "abc",
				address = "abc"
			)
		self.assertFalse( device.registered )

	def test_device_is_related_to_location( self ):
		## 38°09'56.7"S+146°41'56.0"E
		# West and South are negative. North and East are positive
		location_ = Location.objects.create(
			name="Field A", 
			longitude=-38.1665936, 
			latitude=146.6989864,
			altitude=80.00
		)
		device = Device(
				name="device_a", 
				description="device description",
				serial_id = "abc",
				address = "abc"			
			)
		device.location = location_
		device.save()
		self.assertIn(device, location_.device_set.all())

class LogEntryTest( TestCase ):
	def test_device_is_related_to_device( self ):
		device_ = Device.objects.create(
				name="device_a", 
				description="device description",
				serial_id = "abc",
				address = "abc"			
			)
		log_entry = Log_Entry(
				log_data = { 
					"field1": 45.6,
					"field2": 34.4,
				}
			)
		log_entry.device = device_
		log_entry.save()
		self.assertIn(log_entry, device_.log_entry_set.all())

	def test_can_read_the_log_data( self ):
		device_ = Device.objects.create(
				name="device_a", 
				description="device description",
				serial_id = "abc",
				address = "abc"			
			)
		json_data = { 
					"field1": 45.6,
					"field2": 34.4,
				}
		log_entry = Log_Entry(
				log_data = json_data
			)
		log_entry.device = device_
		log_entry.save()
		self.assertEquals(json_data, Log_Entry.objects.all()[0].log_data)

	def test_can_read_data_as_json( self ):
		device_ = Device.objects.create(
				name="device_a", 
				description="device description",
				serial_id = "abc",
				address = "abc"			
			)
		json_data = { 
					"field1": 45.6,
					"field2": 34.4,
				}
		log_entry = Log_Entry(
				log_data = json_data
			)
		log_entry.device = device_
		log_entry.save()

		self.assertEquals(json_data, Log_Entry.objects.all()[0].log_data)


	def test_can_read_data_json_value( self ):
		device_ = Device.objects.create(
				name="device_a", 
				description="device description",
				serial_id = "abc",
				address = "abc"			
			)
		json_data = { 
					"field1": 45.6,
					"field2": 34.4,
				}
		log_entry = Log_Entry(
				log_data = json_data
			)
		log_entry.device = device_
		log_entry.save()

		self.assertEquals(json_data["field1"], Log_Entry.objects.all()[0].log_data["field1"])



## ========== Tables to be yet defined ... Don't clutter the tests =========
# class UnitsTest( TestCase ):
# 	def test_unit_is_created( self ):
# 		pass

# class DeviceMetadataTest( TestCase ):
# 	def test_deviceMetadata_is_created( self ):
# 		pass


