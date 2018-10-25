import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Area_Group(Base):
    __tablename__ = 'area_group'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    poly_file = Column(String(250), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    zoom = Column(Integer, nullable=False)


class Area(Base):
    __tablename__ = 'area__poly'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    poly_name = Column(String(250), nullable=False)
    color = Column(String(10), nullable=False)


class DataSource(Base):
    __tablename__ = 'datasource'
    id = Column(Integer, primary_key=True)


class Dat_Prediction(Base):
    __tablename__ = 'dat_pred_forcast'
    id = Column(Integer, primary_key=True)
    time_start = Column(DateTime, nullable=False)
    time_end = Column(DateTime, nullable=False)
    area_group_id = Column(Integer, nullable=False)
    weather_id = Column(Integer, nullable=False)
    wind_min = Column(Integer, nullable=False)
    wind_max = Column(Integer, nullable=False)
    visibility = Column(Integer, nullable=False)
    temp_min = Column(Integer, nullable=False)
    temp_max = Column(Integer, nullable=False)
    wave_min = Column(Float, nullable=False)
    wave_max = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)
    water_level_min = Column(Float, nullable=False)
    water_level_max = Column(Float, nullable=False)
    water_level_max_time = Column(DateTime, nullable=True)
    water_level_min_time = Column(DateTime, nullable=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())


class Data_Delf_3d(Base):
    __tablename__ = 'dat_pred_delf3d'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    area_group_id = Column(Integer, nullable=False)
    raster_file = Column(String(250), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())


class Param_Weather(Base):
    __tablename__ = 'par_weather'
    id = Column(Integer, primary_key=True)
    en_desc = Column(String(40), nullable=False)
    id_desc = Column(String(40), nullable=False)
    icon = Column(String(40), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())


class Instrument(Base):
    __tablename__ = 'instrument'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    lat_top_left = Column(Float, nullable=False)
    lng_top_left = Column(Float, nullable=False)
    lat_bottom_right = Column(Float, nullable=False)
    lng_bottom_right = Column(Float, nullable=False)
    Instrument_Feature_Group = Column(Integer)



class Instrument_Feature(Base):
    __tablename__ = 'instrument_feature'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)


class Data_Obs_ADCP(Base):
    __tablename__ = 'dat_obs_adcp'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    adcp_id = Column(Integer, nullable=False)
    ft_wave_hgt = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())


class Data_Obs_AWS(Base):
    __tablename__ = 'dat_obs_aws'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    area_group_id = Column(Integer, nullable=False)
    ft_air_temp = Column(Float, nullable=False)
    ft_water_temp = Column(Float, nullable=False)
    ft_wind = Column(Float, nullable=False)
    ft_wind_dir = Column(Float, nullable=False)
    ft_precipitation = Column(Float, nullable=False)
    ft_preasure = Column(Float, nullable=False)
    ft_solar_rad = Column(Float, nullable=False)
    ft_ph_cond = Column(Float, nullable=False)
    ft_water_level = Column(Float, nullable=False)
    ft_timestamp = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())


class Data_Obs_Tide_Gauge(Base):
    __tablename__ = 'dat_obs_tide_gauge'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    area_group_id = Column(Integer, nullable=False)
    ft_water_level = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())


class Data_Obs_Hf_Radar(Base):
    __tablename__ = 'dat_obs_hf_radar'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    area_group_id = Column(Integer, nullable=False)
    raster_file = Column(String(250), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())


class Params(Base):
    __tablename__ = 'param'
    id = Column(Integer, primary_key=True)
    key = Column(String(250))
    value = Column(String(250))
    desc = Column(String(250))
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())


if __name__ == '__main__':
    engine = create_engine('sqlite:///../../data_trees/_data.db')
    Base.metadata.create_all(engine)
