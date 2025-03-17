from itertools import combinations
import time
class Person:
    def __init__(self, gender, limit, char):
        self.gender = gender
        self.limit = limit
        self.char = char

    def __repr__(self):
        return helper(self)
    # def have_sex(self, other):
    #     pass
        
class SexWithSis(Person):
    def have_sex(self, other):
        return True if other.limit == "sister" else False

class SexWithMale(Person):
    def have_sex(self, other):
        return True if other.gender == "male" else False

class SexWithBro(Person):
    def have_sex(self, other):
        return True if other.limit == "brother" else False

class Carrier:
    def __init__(self, entity: Person):
        self.entity = entity

    def have_sex(self):
        if len(self.entity) > 2 or len(self.entity) == 0: return False
        c = combinations(self.entity, r=2)
        for i in c:
            # print("i", helper(i[0]), helper(i[1]))
            if i[0].have_sex(i[1]) or i[1].have_sex(i[0]):
            # if i[0].have_sex(i[1]):
                return True
        return False

    def join(self, crew):
        self.entity |= crew

    def leave(self, crew):
        self.entity -= crew

    def clear(self):
        self.entity = set()

    def __str__(self):
        return ','.join([c.char for c in self.entity])

    def __repr__(self):
        return ','.join([c.char for c in self.entity])

# print(','.join([]))
# print("this?")

mother = SexWithMale('female', 'none', "mother")
father = SexWithSis('male', 'none', "father")
brother = SexWithSis('male', 'brother', "brother")
sister = SexWithBro('female', 'sister', "sister")
stranger = SexWithBro('male', 'none', "stranger")

def helper(ent):
    if ent is mother:
        return "mother"
    elif ent is father:
        return "father"
    elif ent is brother:
        return "brother"
    elif ent is sister:
        return "sister"
    elif ent is stranger:
        return "stranger"
    
source = Carrier({mother, father, brother, sister, stranger})
# source = Carrier({mother, brother, sister, father})
ferry = Carrier(set())
dest = Carrier(set())

ans_list = list()
debug = list()

import copy

def dfs(ans, source, ferry, dest):
    p = source.entity

    # if len(source.entity) == 1:
    #     ans_list.append(copy.deepcopy(ans))
    #     return

    c = combinations(p, r=2)
    for s1, s2 in c:
        crew = {s1, s2}
        ferry.clear()
        ferry.join(crew), source.leave(crew), dest.join(crew)
        if ferry.have_sex() or source.have_sex() or dest.have_sex():
            ferry.clear(), source.join(crew), dest.leave(crew)
            continue
        
        if not source.entity:
            tmp = str(source)+' -> '+str(dest)
            ans.append(tmp)
            ans_list.append(ans.copy())
            ans.pop()
            ferry.clear(), source.join(crew), dest.leave(crew)
            return
        tmp = str(source)+' -> '+ str(ferry) + ' -> ' + str(dest)
        for cr in dest.entity.copy():
            if cr is sister: continue
            cr = {cr}
            ferry.clear(), ferry.join(cr)
            # tmp = str(source)+'->'+str(dest)
            dest.leave(cr), source.join(cr)
            if not source.have_sex() and not dest.have_sex():
                tmp2 = tmp + '      back<-' + str(ferry) + f'\n next:{str(source)}    {str(dest)}'
                ans.append(tmp2)
                print(ans)
                dfs(ans, source, ferry, dest)
                ans.pop()
            dest.join(cr), source.leave(cr)
        ferry.clear(), source.join(crew), dest.leave(crew)

import sys
dfs(list(), source, ferry, dest)
print("********* end **********")
print("source", source)
print("dest", dest)
# time.sleep(2)

sys.stdout.flush()
# print(ans_list)
print(len(ans_list))
# print(debug)

# print("len", len(ans_list))

# print("len")
# print("why")
# print("whyasd")

for i, a in enumerate(ans_list):
    print(f"********* ans{i+1} ***********")
    for aa in a:
        print(aa)
    print(f"******* ans{i+1} end *********")
    print()

sys.stdout.flush()

# print("len", ans_list[0])
# print(ans_list[1])
