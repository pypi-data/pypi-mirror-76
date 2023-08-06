import nvdict.dict_func as dfunc
import nvdict.attr_func as afunc 
from xlist.sarr import join



class Orb:
    def __init__(self,**kwargs):
        self._root = kwargs['root'] if('root' in kwargs) else {}
        self._pl = kwargs['pl'] if('pl' in kwargs) else []
    def _loads(self,d):
        self._root = d
        afunc.init_orb_with_dict(self,self._root,cls=Orb)
    def _dumps(self):
        selfd = dfunc.get_via_pl(self._root,self._pl)
        return(selfd)
    def _dot_path(self):
        return(join(self._pl,'.'))
    def _dir_path(self):
        return(join(self._pl,'/'))
    def __repr__(self):
        selfd = dfunc.get_via_pl(self._root,self._pl)
        return(selfd.__repr__())
    def __getattribute__(self,an):
        if(an[0]=="_"):
            return(object.__getattribute__(self,an))
        else:
            cond = (an in self.__dict__)
            if(cond):
                return(object.__getattribute__(self,an))
            else:
                npl = self._pl[:] + [an]
                self.__dict__[an] = Orb(root=self._root,pl=npl)
                dfunc.set_dflt_via_pl(self._root,npl)
                return(self.__dict__[an])
    def __setattr__(self,an,val):
        if(an[0]=="_"):
            object.__setattr__(self,an,val)
        else:
            cond = dfunc.is_leafv(val)
            if(cond):
                npl = self._pl[:] + [an]
                self.__dict__[an] =  Orb(root=self._root,pl=npl)
                dfunc.set_via_pl(self._root,npl,val)
            else:
                raise(TypeError('value can only be non-dict'))
    def __delattr__(self,an):
        if(an[0]=="_"):
            object.__delattr__(self,an)
        else:
            deleted = object.__getattribute__(self,an)
            npl = self._pl[:] + [an]
            deleted._root = dfunc.get_via_pl(self._root,npl)
            deleted._pl = []
            dfunc.del_via_pl(self._root,npl)
            object.__delattr__(self,an)
    def _parent_dict(self):
        if(len(self._pl)>0):
            ppl = self._pl[0:-1]
            return(dfunc.get_via_pl(self._root,ppl))
        else:
            return(None)
    def _children_dict(self):
        selfd = dfunc.get_via_pl(self._root,self._pl)
        return(dfunc.get_vchildren(selfd))
    def _is_root(self):
        return(len(self._pl)==0)

