from .section_reader import (
    SectionReader, 
    TrainerInfoSection, 
    TeamItemsSection, 
    GameStateSection, 
    GameSpecificDataSection,
    PCBufferSection
    )


class SaveReader:
    def __init__(self, data: bytes):
        self.data = data
        self.section_reader = SectionReader(data)
        # This is created the first so the game_code and security_key are defined
        self.trainer_info = self.get_trainer_info() 

    @classmethod
    def from_file(cls, file_path: str):
        """Creates an instance of SaveReader by reading content from a file."""
        with open(file_path, 'rb') as f:
            content = f.read()
        return cls(content)
    
    @classmethod
    def from_data(cls, data: bytes):
        """Creates an instance of SaveReader from a given bytes."""
        return cls(data)
    
    def get_trainer_info(self) -> TrainerInfoSection:
        return self.section_reader.get_section_by_id(0)

    @property
    def team_items(self) -> TeamItemsSection:
        return self.section_reader.get_section_by_id(1)

    @property
    def game_state(self) -> GameStateSection:
        return self.section_reader.get_section_by_id(2)
    
    @property
    def game_specific_data(self) -> GameSpecificDataSection:
        return self.section_reader.get_section_by_id(3)
    
    @property
    def pc_buffer(self) -> PCBufferSection:
        return self.section_reader.get_section_by_id(5)