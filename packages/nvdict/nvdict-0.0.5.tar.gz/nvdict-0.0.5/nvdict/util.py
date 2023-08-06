from xlist.map import mapv

def kvlist2d(kl,vl):
    d = {}
    for i in range(len(kl)):
        k = kl[i]
        v = vl[i]
        d[k] = v
    return(d)


def d2kvlist(d):
    kl = list(d.keys())
    vl = list(d.values())
    return([kl,vl])


def entries_to_kvlist(entries):
    kl = mapv(entries,lambda e:e[0])
    vl = mapv(entries,lambda e:e[1])
    return([kl,vl])

def kvlist_to_entries(kl,vl):
    entries = []
    for i in range(len(kl)):
        k = kl[i]
        v = vl[i]
        entry = [k,v]
        entries.append(entry)
    return(entries)


def entries_to_dict(entries):
    kl,vl = entries_to_kvlist(entries)
    return(kvlist2d(kl,vl))



def dict_to_entries(d):
    kl,vl = d2kvlist(d)
    entries = kvlist_to_entries(kl,vl)
    return(entries)



