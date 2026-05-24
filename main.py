from AlokeCore.UseCases.SectionManager.SectionManager import SectionManager, SECTION_RESULT
from AlokeCore.UseCases.Config.Port.ConfigHandler import IConfigHandler
from AlokeCore.Adapter.ConfigHandler import ConfigHandler
from AlokeCore.UseCases.Config.ConfigManager import ConfigManager

config_handler = ConfigHandler()
config_manager = ConfigManager(config_handler)
section_manager = SectionManager( config_manager)

result = section_manager.new_section("Section 1")

print(f"Create Section Result: {result.name()} with ID: {result.id()}")
