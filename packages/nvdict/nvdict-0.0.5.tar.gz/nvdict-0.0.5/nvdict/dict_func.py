import copy
from xlist.map import mapv,mapiv
from xlist.slct import some as slct_some
from xlist.fltr import fltrv
from xlist.crud import concat
from nvdict.util import kvlist2d,d2kvlist,entries_to_kvlist,kvlist_to_entries,entries_to_dict,dict_to_entries

def get_via_pl(d,pl):
    lngth = len(pl)
    ele = d
    for i in range(lngth):
        ele = ele[pl[i]]
    return(ele)


def set_via_pl(d,pl,v):
    lngth = len(pl)
    ele = d
    for i in range(lngth-1):
        ele = ele[pl[i]]
    ele[pl[len(pl)-1]] = v
    return(d)
    

def set_dflt_via_pl(d,pl,*args):
    v = args[0] if(len(args)>0) else {}
    lngth = len(pl)
    ele = d
    for i in range(lngth-1):
        k = pl[i]
        if(k in ele):
            ele = ele[k]
        else:
            ele[k] = {}
            ele = ele[k]
    k = pl[lngth-1]
    ele[k] = v  
    return(d)
            

def del_via_pl(d,pl):
    lngth = len(pl)
    ele = d
    for i in range(lngth-1):
        ele = ele[pl[i]]
    k = pl[lngth-1]
    rslt = ele[k]
    del ele[k]
    return(rslt)
    

def is_leaf_pl_via_dict(d,pl):
    v = get_via_pl(d,pl)
    cond = is_leafv(v)
    return(cond)


###

def get_type_str(o):
    typ = type(o)
    s = str(typ)
    return(s)


def get_kschema(d):
    sdfs_pl=get_sdfs_pl(d)[1:]
    kschema={}
    for i in range(len(sdfs_pl)):
        pl=sdfs_pl[i]
        v = get_via_pl(d,pl)
        cond = is_leafv(v)
        if(cond):
            set_dflt_via_pl(kschema,pl,get_type_str(v))
        else:
            set_dflt_via_pl(kschema,pl)
    return(kschema)


def get_kstruct(d):
    sdfs_pl=get_sdfs_pl(d)[1:]
    kstruct={}
    for i in range(len(sdfs_pl)):
        pl=sdfs_pl[i]
        set_dflt_via_pl(kstruct,pl)
    return(kstruct)

####

def get_ppl(pl):
    return(pl[0:-1])

def get_plmat(d):
    m = _get_mat(d)
    plmat = copy.deepcopy(m)
    for i in range(len(m)):
        lyr = m[i]
        for j in range(len(lyr)):
            plmat[i][j] = lyr[j]["pl"]
    return(plmat)


def get_wfs_pl(d):
    plmat = get_plmat(d)
    return(concat(*plmat))


def get_sdfs_pl(d):
    m = _get_mat(d)
    sdfs = _get_ele_sdfs(m[0][0])
    sdfs = mapv(sdfs,lambda e:e['pl'])
    return(sdfs)


def get_sdfs_leaf_pl(d):
    m = _get_mat(d)
    sdfs = _get_ele_sdfs(m[0][0])
    sdfs = fltrv(sdfs,lambda e:_is_leaf_ele(e))
    sdfs = mapv(sdfs,lambda e:e['pl'])
    return(sdfs)


def get_sdfs_nonleaf_pl(d):
    m = _get_mat(d)
    sdfs = _get_ele_sdfs(m[0][0])
    sdfs = fltrv(sdfs,lambda e:not(_is_leaf_ele(e)))
    sdfs = mapv(sdfs,lambda e:e['pl'])
    return(sdfs)


def plsdfs_to_kstruct(sdfs):
    kstruct = {}
    sdfs = fltrv(sdfs,lambda pl:len(pl)>0)
    for i in range(len(sdfs)):
        set_dflt_via_pl(kstruct,sdfs[i])
    return(kstruct)


def is_leaf_pl_via_plsdfs(sdfs_pl,pl):
    kstruct = plsdfs_to_kstruct(sdfs_pl)
    cond = is_leaf_pl_via_dict(kstruct,pl)
    return(cond)



def get_pl_children_via_plsdfs(plsdfs,pl):
    kstruct = plsdfs_to_kstruct(sdfs_pl)    



####




########

def get_vfstch(d):
    children = get_vchildren(d)
    fstch = None if(len(children)==0) else children[0]
    return(fstch)

def get_vlstch(d):
    children = get_vchildren(d)
    lstch = None if(len(children)==0) else children[-1]
    return(lstch)



def get_which_vchild(d,which):
    children = get_vchildren(d)
    return(children[which])


def get_some_vchildren(d,*whiches):
    children = get_vchildren(d)
    children = slct_some(children,*whiches)
    return(children)


def get_vchildren(d):
    return(list(d.values()))

def get_vchild_count(d):
    ks = list(d.keys())
    return(len(ks))



def is_leafv(d):
    cond = not(isinstance(d,dict)) or (len(d)==0) 
    return(cond)

def get_wfs_vmat(d):
    m = _get_mat(d)
    vmat = copy.deepcopy(m)
    for i in range(len(m)):
        lyr = m[i]
        for j in range(len(lyr)):
            vmat[i][j] = lyr[j]["d"]
    return(vmat)

def get_wfs_vlist(d):
    wfsl = [d]
    unhandled = [{"d":d,"pl":[]}]
    while(len(unhandled)>0):
        next_unhandled = []
        for i in range(len(unhandled)):
            ele = unhandled[i]
            pd = ele["d"]
            ppl = ele["pl"]
            paths = list(pd.keys())
            d_children = list(pd.values())
            wfsl = wfsl + d_children
            children = mapiv(paths,lambda i,path:{"d":d_children[i],"pl":ppl+[path]})
            children = fltrv(children,lambda r:not(is_leafv(r["d"])))
            next_unhandled = next_unhandled + children
        unhandled = next_unhandled
    return(wfsl)


def get_sdfs_vlist(d):
    m = _get_mat(d)
    sdfs = _get_ele_sdfs(m[0][0])
    sdfs = mapv(sdfs,lambda e:e['d'])
    return(sdfs)

def get_sdfs_leaf_vlist(d):
    m = _get_mat(d)
    sdfs = _get_ele_sdfs(m[0][0])
    sdfs = fltrv(sdfs,lambda e:_is_leaf_ele(e))
    sdfs = mapv(sdfs,lambda e:e['d'])
    return(sdfs)
    



def get_vstruct(d):
    vstruct = []
    root = {"d":d,"pl":[],"v":vstruct}
    unhandled = [root]
    while(len(unhandled)>0):
        next_unhandled = []
        for i in range(len(unhandled)):
            ele = unhandled[i]
            pd = ele["d"]
            ppl = ele["pl"]
            pv = ele["v"]
            paths = list(pd.keys())
            d_children = list(pd.values())
            for i in range(len(d_children)):
                d_child = d_children[i]
                cond = is_leafv(d_child)
                if(cond):
                    pv.append(d_child)
                else:
                    pv.append([])
            children = mapiv(paths,lambda i,path:{"d":d_children[i],"pl":ppl+[path],"v":pv[i]})
            children = fltrv(children,lambda r:not(is_leafv(r["d"])))
            next_unhandled = next_unhandled + children
        unhandled = next_unhandled
    return(vstruct)


########

def get_count(d):
    wfs_pl = get_wfs_pl(d)
    return(len(wfs_pl))


def flatten_to_leaf_entries(d):
    m = _get_mat(d)
    sdfs = _get_ele_sdfs(m[0][0])
    sdfs = fltrv(sdfs,lambda e:_is_leaf_ele(e))
    entries = mapv(sdfs,lambda e:[tuple(e['pl']),e['d']])
    return(entries)

def flatten_to_leaf_dict(d):
    entries = flatten_to_leaf_entries(d)
    rslt = entries_to_dict(entries)
    return(rslt)


def flatten_to_entries(d):
    m = _get_mat(d)
    sdfs = _get_ele_sdfs(m[0][0])
    entries = mapv(sdfs,lambda e:[tuple(e['pl']),e['d']])
    return(entries)

def flatten_to_dict(d):
    entries = flatten_to_leaf_entries(d)
    rslt = entries_to_dict(entries)
    return(rslt)



def deflatten_from_leaf_entries(leaf_entries):
    d = {}
    for i in range(len(leaf_entries)):
        entry = leaf_entries[i]
        pl = entry[0]
        v = entry[1]
        set_dflt_via_pl(d,pl,v)
    return(d)



def get_flatvl_via_kstruct(d,kstruct):
    sdfs_leaf_pl = get_sdfs_leaf_pl(kstruct)
    flat_vl =  mapv(sdfs_leaf_pl,lambda pl:get_via_pl(d,pl))
    return(flat_vl)


def unzip(d):
    kstruct = {}
    root = {"d":d,"pl":[],"k":kstruct}
    unhandled = [root]
    while(len(unhandled)>0):
        next_unhandled = []
        for i in range(len(unhandled)):
            ele = unhandled[i]
            pd = ele["d"]
            ppl = ele["pl"]
            pk = ele["k"]
            paths = list(pd.keys())
            for i in range(len(paths)):
                pk[paths[i]] = {}
            d_children = list(pd.values())
            children = mapiv(paths,lambda i,path:{"d":d_children[i],"pl":ppl+[path],"k":pk[path]})
            children = fltrv(children,lambda r:not(is_leafv(r["d"])))
            next_unhandled = next_unhandled + children
        unhandled = next_unhandled
    sdfs_leaf_pl = get_sdfs_leaf_pl(kstruct)
    flat_vl =  mapv(sdfs_leaf_pl,lambda pl:get_via_pl(d,pl))
    return([kstruct,flat_vl])
    


def zip(kstruct,flat_vl):
    d = {}
    pls = get_sdfs_leaf_pl(kstruct) 
    for i in range(len(flat_vl)):
        pl = pls[i]
        v = flat_vl[i]
        set_dflt_via_pl(d,pl,v)
    return(d)


#########

def _get_mat(d):
    root = {"d":d,"pl":[],"parent":None,"sibseq":0}
    mat = []
    unhandled = [root]
    mat.append(unhandled)
    while(len(unhandled)>0):
        next_unhandled = []
        lyr = []
        for i in range(len(unhandled)):
            ele = unhandled[i]
            pd = ele["d"]
            ppl = ele["pl"]
            paths = list(pd.keys())
            d_children = list(pd.values())
            children = mapiv(paths,lambda i,path:{"d":d_children[i],"pl":ppl+[path],"parent":ele,"children":[],"sibseq":i})
            ele['children'] = children
            lyr = lyr +children
            children = fltrv(children,lambda r:not(is_leafv(r["d"])))
            next_unhandled = next_unhandled + children
        mat.append(lyr)
        unhandled = next_unhandled
    return(mat)



def _is_leaf_ele(ele):
    return(len(ele["children"])==0)

def _get_wfs_elist(d):
    m = _get_mat(d)
    return(concat(*m))




def _get_eparent(ele):
    return(ele["parent"]) 

def _get_efstch(ele):
    children = ele["children"]
    efstch = None if(len(children)==0) else children[0]
    return(efstch) 

def _get_ersib(ele):
    pele = _get_eparent(ele)
    if(pele != None):
        sibs = pele["children"]
        rsib_seq = ele["sibseq"] + 1
        if(rsib_seq<len(sibs)):
            return(sibs[rsib_seq])
        else:
            return(None)
    else:
        return(None)


def _get_ersib_of_fst_ance_having_rsib(ele):
    parent = _get_eparent(ele)
    while(parent != None):
        rsib = _get_ersib(parent)
        if(rsib != None):
            return(rsib)
        else:
            parent = _get_eparent(parent)
    return(None) 



def _get_ele_sdfs_next(ele):
    fstch = _get_efstch(ele)
    if(fstch != None):
        return(fstch)
    else:
        rsib = _get_ersib(ele)
        if(rsib != None):
            return(rsib)
        else:
            return(_get_ersib_of_fst_ance_having_rsib(ele))


def _get_ele_sdfs(ele):
    sdfs = []
    while(ele!=None):
        sdfs.append(ele)
        ele = _get_ele_sdfs_next(ele)
    return(sdfs)


#############
