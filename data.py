from typing import List, Type
from json import loads, dumps
from pydantic import BaseModel
from dataclasses import dataclass

class Username(BaseModel):
    user: str
    full_name: str

    def __init__(self,object:dict):
        self.from_object(object)

    def from_object(self,object: dict):
        self.user = object["username"]
        self.full_name = object["full_name"]

    def to_json(self):
        return dumps(self.__dict__)

    __fields_set__ = {"user","full_name"}

class DateTime(BaseModel):
    day: int
    month: int
    year: int
    hour: int
    minute: int
    second: int

    def __init__(self,string:str):
        self.from_string(string)

    def to_string(self):
        return str(self.year)+"-"+str(self.month)+"-"+str(self.day)+"T"+str(self.hour)+":"+str(self.minute)+":"+str(self.second)+".000Z"

    def is_equal(self,other):
        return self.year == other.year and \
            self.month == other.month and \
            self.day == other.day and \
            self.hour == other.hour and \
            self.minute == other.minute and \
            self.second == other.second

    def is_later_than(self,other):
        return self.year > other.year or \
            (self.year == other.year and\
             self.month > other.month) or \
            (self.year == other.year and \
             self.month == other.month and \
             self.day > other.day) or \
            (self.year == other.year and \
             self.month == other.month and \
             self.day == other.day and \
             self.hour > other.hour) or \
            (self.year == other.year and \
             self.month == other.month and \
             self.day == other.day and \
             self.hour == other.hour and \
             self.minute > other.minute) or \
            (self.year == other.year and \
             self.month == other.month and \
             self.day == other.day and \
             self.hour == other.hour and \
             self.minute == other.minute and \
             self.second > other.second)

    def from_string(self,string:str):
        _ = string.split("T")
        __ = _[0].split("-")
        self.year = int(__[0])
        self.month = int(__[1])
        self.day = int(__[2])
        __ = _[1].split(":")
        self.hour = int(__[0])
        self.minute = int(__[1])
        self.second = int(__[2].split(".")[0])
    
    __fields_set__ = {'year', 'month', 'day', 'hour', 'minute', 'second'}

class Scan(BaseModel):
    date: DateTime
    followers: List[Username]
    following: List[Username]
    not_following_back: List[Username]

    def __init__(self,file):
        self.from_json(file)

    def from_json(self,file: str):
        res = loads(open("results/"+file,"r").read())
        self.date = DateTime(res["date"])
        self.followers = [Username(f) for f in res["followers"]]
        self.following = [Username(f) for f in res["followings"]]
        self.not_following_back = [Username(f) for f in res["dontFollowMeBack"]]

    __fields_set__  = {'date', 'followers', 'following', 'not_following_back'}
