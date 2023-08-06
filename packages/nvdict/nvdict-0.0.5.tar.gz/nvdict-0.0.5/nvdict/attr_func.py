import copy
from xlist.map import mapv,mapiv
from xlist.slct import some as slct_some
from xlist.fltr import fltrv
from xlist.crud import concat
from nvdict.util import kvlist2d,d2kvlist,entries_to_kvlist,kvlist_to_entries,entries_to_dict,dict_to_entries
import nvdict.dict_func as dfunc

def get_via_pl(o,pl):
    #o._root    根dict
    #o._pl      绝对路径
    #pl         相对路径
    lngth = len(pl)
    ele = o
    for i in range(lngth):
        an = pl[i]
        ele = object.__getattribute__(ele,an)
    return(ele)


def set_via_pl(o,pl,*args,**kwargs):
    root = o._root
    base_pl = o._pl
    Cls = kwargs['cls']
    v = args[0] if(len(args)>0) else Cls(root=root,pl=base_pl+pl)
    if(type(v)==Cls):
        lngth = len(pl)
        ele = o
        for i in range(lngth-1):
            an = pl[i]
            ele = object.__getattribute__(ele,an)
        an = pl[len(pl)-1]
        v = Cls(root=root,pl=base_pl+pl)
        object.__setattr__(ele,an,v)
        return(o)
    else:
        raise(TypeError("value can only be <class '__main__.Orb'>")) 
 


def set_dflt_via_pl(o,pl,*args,**kwargs):
    root = o._root
    base_pl = o._pl
    Cls = kwargs['cls']
    v = args[0] if(len(args)>0) else Cls(root=root,pl=base_pl+pl) 
    lngth = len(pl)
    ele = o
    for i in range(lngth-1):
        an = pl[i]
        if(an in ele.__dict__):
            ele = object.__getattribute__(ele,an)
        else:
            set_via_pl(o,pl[0:(i+1)],Cls(root=root,pl=base_pl+pl[0:(i+1)]),cls=Cls)
            ele = object.__getattribute__(ele,an)
    set_via_pl(o,pl,v,cls=Cls)
    return(o)



def del_via_pl(o,pl):
    lngth = len(pl)
    ele = o
    for i in range(lngth-1):
        an = pl[i]
        ele = object.__getattribute__(ele,an)
    an = pl[lngth-1]
    rslt = object.__getattribute__(ele,an)
    object.__delattr__(ele,an)
    return(rslt)


def is_leaf_pl_via_orb(o,pl):
    v = dfunc.get_via_pl(o._root,pl)
    cond = dfunc.is_leafv(v)
    return(cond)


def init_orb_with_dict(o,d,**kwargs):
    Cls = kwargs['cls']
    entries = dfunc.flatten_to_leaf_entries(d)
    for i in range(len(entries)):
        pl = list(entries[i][0])
        set_dflt_via_pl(o,pl,cls=Cls)
    return(o)


