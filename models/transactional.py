"""
    DDL and other schema creational operations for TPOT transactional tables
    holding pre-aggregated data for outcomes analysis
"""


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, Float, String, Boolean, Date
from sqlalchemy.orm import relationship


Base = declarative_base()


class Participant(Base):
    __tablename__ = 'participant'

    participant_id = Column(Integer, primary_key=True)
    wioa_participant = Column(Boolean, nullable=False, default=False)
    wioa_lta_participant = Column(Boolean, nullable=False, default=False)
    wages = relationship('Wage', backref='participant')
    programs = relationship('Program', secondary='participant_program')


class Program(Base):
    __tablename__ = 'program'

    program_cip = Column(Integer, primary_key=True)
    name = Column(String(140), nullable=False)
    potential_outcome_id = Column(Integer, ForeignKey('outcome.potential_outcome_id'))
    participants = relationship('Participant', secondary='participant_program')
    providers = relationship('Provider', secondary='program_provider')


class ParticipantProgram(Base):
    __tablename__ = 'participant_program'

    participant_id = Column(Integer, ForeignKey('participant.participant_id'), primary_key=True)
    program_cip = Column(Integer, ForeignKey('program.program_cip'), primary_key=True)
    entry_date = Column(Date, nullable=False)
    exit_date = Column(Date)
    enrolled = Column(Boolean, nullable=False, default=True)
    exit_type_id = Column(Integer, ForeignKey('exit_type.type_id'))
    obtained_credential = Column(Boolean, nullable=False, default=False)


class ProgramProvider(Base):
    __tablename__ = 'program_provider'

    program_cip = Column(Integer, ForeignKey('program.program_cip'), primary_key=True)
    provider_id = Column(Integer, ForeignKey('provider.provider_id'), primary_key=True)


class Provider(Base):
    __tablename__ = 'provider'

    provider_id = Column(Integer, primary_key=True)
    name = Column(String(140), nullable=False)
    type_id = Column(Integer, ForeignKey('entity_type.type_id'), nullable=False)
    programs = relationship('Program', secondary='program_provider')


class Outcome(Base):
    __tablename__ = 'outcome'

    potential_outcome_id = Column(Integer, primary_key=True)
    description = Column(String(250), nullable=False)
    programs = relationship('Program', backref='outcome')


class ExitType(Base):
    __tablename__ = 'exit_type'

    type_id = Column(Integer, primary_key=True)
    name = Column(String(140), nullable=False)
    description = Column(String(250))
    participant_programs = relationship('ParticipantProgram', backref='exit_type')


class Wage(Base):
    __tablename__ = 'wage'

    wage_start_date = Column(Date, primary_key=True)
    wage_end_date = Column(Date, primary_key=True)
    participant_id = Column(Integer, ForeignKey('participant.participant_id'), primary_key=True)
    wage_amt = Column(Float, nullable=False)


class EntityType(Base):
    __tablename__ = 'entity_type'

    type_id = Column(Integer, primary_key=True)
    name = Column(String(140), nullable=False)
    description = Column(String(250))
    providers = relationship('Provider', backref='entity_type')
