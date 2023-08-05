'''IOSXE: Image Handler Class'''

# Genie
from genie.libs.clean.stages.image_handler import ImageHandler as CommonImageHandler
from genie.metaparser.util.schemaengine import Schema, Optional



class ImageHandler(CommonImageHandler):

    def __init__(self, device, images, *args, **kwargs):
        super().__init__(device, images, *args, **kwargs)

        # Two possible formats for images are accepted.
        # One for earms (list) and the other for Xpresso (dict)

        # List format - earms
        if isinstance(images, list):
            # No further schema to validate - already checked if its a list

            # if more than one image is provided we assume the first
            # is the image and everything after is packages
            if len(images) > 1:
                self.images = images[0:1]
                self.packages = images[1:]
            else:
                self.packages = []

        # Dictionary format - Xpresso
        elif isinstance(images, dict):
            schema = {
                'image': {
                    'file': list
                },
                Optional('packages'): {
                    'file': list
                }
            }
            Schema(schema).validate(images)

            self.images = images['image']['file']
            self.packages = images.get('packages', {}).get('file', [])

        else:
            raise Exception("Expected 'images' to be either a dictionary "
                            "or list but got {}".format(type(images)))

    def update_image_references(self, section):
        # section.parameters['image_mapping'] shall be saved in any
        # stage that modifies the image name/path
        if 'image_mapping' in section.parameters:

            for index, image in enumerate(self.images):
                # change the saved image to the new image name/path
                self.images[index] = section.parameters['image_mapping'].get(image, image)

            for index, package in enumerate(self.packages):
                # change the saved package to the new package name/path
                self.packages[index] = section.parameters['image_mapping'].get(package, package)

    def update_tftp_boot(self):
        '''Update clean section 'tftp_boot' with image information'''

        tftp_boot = self.device.clean.setdefault('tftp_boot', {})
        tftp_boot.update({'image': self.images})

    def update_copy_to_linux(self):
        '''Update clean section 'copy_to_linux' with image information'''

        origin = self.device.clean.setdefault('copy_to_linux', {}).\
                                   setdefault('origin', {})
        origin.update({'files': self.images + self.packages})

    def update_copy_to_device(self):
        '''Update clean stage 'copy_to_device' with image information'''

        origin = self.device.clean.setdefault('copy_to_device', {}).\
                                   setdefault('origin', {})
        origin.update({'files': self.images + self.packages})

    def update_change_boot_variable(self):
        '''Update clean stage 'change_boot_variable' with image information'''

        change_boot_variable = self.device.clean.setdefault('change_boot_variable', {})
        change_boot_variable.update({'images': self.images})

    def update_verify_running_image(self):
        '''Update clean stage 'verify_running_image' with image information'''

        verify_running_image = self.device.clean.setdefault('verify_running_image', {})
        verify_running_image.update({'images': self.images})

    def update_install_image(self):
        '''Update clean stage 'install_image' with image information'''

        install_image = self.device.clean.setdefault('install_image', {})
        install_image.update({'images': self.images})

    def update_install_packages(self):
        '''Update clean stage 'install_packages' with package information'''

        install_packages = self.device.clean.setdefault('install_packages', {})
        install_packages.update({'packages': self.packages})