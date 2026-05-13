from utils.get_skills import get_skills
from utils.read_skill import read_skill

for skill in get_skills():
    print(read_skill(skill))